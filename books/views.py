from django.urls import reverse_lazy
from django.db import models
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.db import transaction
from .models import Loan, Book
from datetime import date, timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q



class LoanCreateView(CreateView):
    model = Loan
    fields = ['user', 'book', 'return_deadline']
    template_name = 'books/loan_create.html'
    success_url = reverse_lazy('loan_list')

    def get_form(self, form_class=None):
        """ Filtra o dropdown para mostrar apenas livros com estoque > 0 """
        form = super().get_form(form_class)
        form.fields['book'].queryset = Book.objects.filter(available_quantity__gt=0)
        return form

    def form_valid(self, form):
        book = form.cleaned_data['book']

        # 1. Verificação de Segurança (caso o usuário tente burlar o form)
        if book.available_quantity <= 0:
            form.add_error('book', "Este livro está sem exemplares disponíveis no momento.")
            return self.form_invalid(form)

        # 2. Transação Atômica: Ou faz tudo, ou não faz nada
        try:
            with transaction.atomic():
                # Diminui uma unidade do estoque disponível
                book.available_quantity -= 1
                
                # Se você ainda usa o campo is_available, atualizamos ele se chegar a zero
                if book.available_quantity == 0:
                    book.is_available = False
                
                book.save()

                # Salva o empréstimo de fato
                response = super().form_valid(form)
                messages.success(self.request, f"Empréstimo do livro '{book.title}' realizado!")
                return response

        except Exception as e:
            form.add_error(None, f"Erro crítico no banco de dados: {e}")
            return self.form_invalid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Mostra apenas livros que tenham pelo menos 1 unidade no estoque
        form.fields['book'].queryset = Book.objects.filter(in_stock__gt=0)
        return form

    def get_initial(self):
        # Sugestão: define o prazo de entrega padrão para 7 dias a partir de hoje
        initial = super().get_initial()
        initial['return_deadline'] = date.today() + timedelta(days=7)
        return initial


class DevolucaoUpdateView(UpdateView):
    model = Loan
    fields = [] # Não precisamos de campos do form, só do clique no botão
    template_name = 'books/devolucao_confirm.html'
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        loan = self.get_object()
        
        if loan.actual_return_date:
            messages.warning(self.request, "Este livro já foi devolvido.")
            return redirect(self.success_url)

        try:
            with transaction.atomic():
                # Atualiza o empréstimo
                loan.actual_return_date = date.today()
                loan.save()
                
                # Devolve ao estoque
                book = loan.book
                book.available_quantity += 1
                book.save()
                
                messages.success(self.request, f"Livro '{book.title}' devolvido!")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro: {e}")
            return self.form_invalid(form)


### 1. Listagem de Livros
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10  # Adiciona paginação para não sobrecarregar a página


### 2. Listagem de Empréstimos (Foco no Bibliotecário)
class LoanListView(ListView):
    model = Loan
    template_name = 'books/loan_list.html'
    context_object_name = 'object_list'
    ordering = ['-loan_date']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        status_filter = self.request.GET.get('status')
        agora = timezone.now()

        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) | 
                Q(book__title__icontains=search_query)
            )
        
        if status_filter == 'open':
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif status_filter == 'closed':
            queryset = queryset.filter(actual_return_date__isnull=False)
        elif status_filter == 'delayed':
            queryset = queryset.filter(
                actual_return_date__isnull=True, 
                return_deadline__lt=agora
            )
        elif status_filter == 'all':
            pass 
        else:
            # Padrão: mostra abertos
            queryset = queryset.filter(actual_return_date__isnull=True)
            
        return queryset

    # ESTE É O MÉTODO QUE PRECISAMOS ADICIONAR:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa a data atual para o HTML conseguir pintar as linhas de vermelho
        context['agora'] = timezone.now()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona o histórico de empréstimos deste livro específico ao contexto
        context['history'] = Loan.objects.filter(book=self.object).order_by('-loan_date')
        return context

def return_book(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    
    if not loan.actual_return_date:
        loan.actual_return_date = timezone.now()
        loan.save()

        book = loan.book
        # Incrementa a quantidade numérica
        book.available_quantity += 1
        
        # CORREÇÃO: Usamos uma comparação para definir os campos booleanos
        # Se a quantidade for maior que 0, o resultado é True. Caso contrário, False.
        status_disponivel = book.available_quantity > 0
        
        book.in_stock = status_disponivel
        book.is_available = status_disponivel
        
        book.save() # O erro acontecia aqui na linha 144
        
        messages.success(request, f"O livro '{book.title}' foi devolvido.")
    
    return redirect('loan_list')


def dashboard(request):
    agora = timezone.now()
    
    dados = {
        'total_livros': Book.objects.count(),
        'emprestimos_ativos': Loan.objects.filter(actual_return_date__isnull=True).count(),
        'livros_atrasados': Loan.objects.filter(
            actual_return_date__isnull=True, 
            return_deadline__lt=agora
        ).count(),
        'total_exemplares': Book.objects.aggregate(models.Sum('total_quantity'))['total_quantity__sum'] or 0,
    }
    
    return render(request, 'books/dashboard.html', dados)