from django.db import models
from django.contrib.auth.models import User
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, verbose_name="Telefone/WhatsApp", blank=True)
    address = models.CharField(max_length=255, verbose_name="Endereço", blank=True)
    notes = models.TextField(verbose_name="Observações Internas", blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True) # novo campo para indicar se o livro está em estoque
    isbn = models.CharField(max_length=13, unique=True)
    is_available = models.BooleanField(default=True) # novo campo para indicar se o livro está disponível para empréstimo
    synopsis = models.TextField(blank=True, null=True, verbose_name="Sinopse")
    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_deadline = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        if self.return_date is None and date.today() > self.loan_date:
            return True
        return False

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
