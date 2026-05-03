from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Author, Book, Loan, UserProfile


# Define como o perfil será exibido dentro da página do Usuário no Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Informações de Contato'

# Define um novo UserAdmin que inclui o Inline do Perfil
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-registra o UserAdmin padrão do Django para usar a nossa versão personalizada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'total_quantity', 'available_quantity', 'isbn')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'loan_date', 'return_deadline', 'actual_return_date')
    list_filter = ('loan_date', 'return_deadline', 'actual_return_date')
    search_fields = ('book__title', 'user__username')
    date_hierarchy = 'loan_date'
    ordering = ('-loan_date',)
    readonly_fields = ('loan_date',)
    actions = ['mark_as_returned']
