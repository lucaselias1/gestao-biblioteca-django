
from django.contrib import admin
from django.urls import path
from books import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('loan/create/', views.LoanCreateView.as_view(), name='loan_create'),
    path('loan/<int:pk>/devolucao/', views.DevolucaoUpdateView.as_view(), name='loan_devolucao'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('loans/', views.LoanListView.as_view(), name='loan_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('loan/return/<int:pk>/', views.return_book, name='return_book'),
    # Adicione outras URLs conforme necessário
]
