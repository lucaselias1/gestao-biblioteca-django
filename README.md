# 📚 Sistema de Gestão de Biblioteca

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema web completo para gerenciamento de acervo bibliográfico e controle de empréstimos, focado em automação de prazos e facilidade de comunicação.

## 🚀 Funcionalidades Principais

- **Gestão de Acervo:** Cadastro completo de livros com controle de estoque dinâmico.
- **Controle de Empréstimos:** Registro de saídas com cálculo automático da data de devolução.
- **Painel de Atrasos:** Identificação visual imediata (linhas em destaque vermelho) para livros com prazo vencido, comparando data atual com o prazo de devolução.
- **Busca e Filtros Avançados:** Filtros por status (Em Aberto, Em Atraso, Devolvidos) e busca global por nome de usuário ou título.
- **Integração com WhatsApp:** Botão de notificação rápida que gera uma mensagem personalizada de cobrança para usuários com livros atrasados.
- **Interface Moderna:** Desenvolvida com Bootstrap 5, ícones interativos e Select2 para busca de livros nos formulários.

## 🛠️ Tecnologias Utilizadas

- **Back-end:** Python, Django (MVT)
- **Front-end:** Bootstrap 5, Bi-Icons, Select2
- **Banco de Dados:** SQLite (Desenvolvimento)

## ⚙️ Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/lucaselias1/gestao-biblioteca-django.git](https://github.com/lucaselias1/gestao-biblioteca-django.git)
   cd gestao-biblioteca-django

2. Crie e ative um ambiente virtual:
python -m venv venv
# No Windows:
venv\Scripts\activate

3.Instale as dependências:
Bash

pip install -r requirements.txt

4.Execute as migrações e inicie o servidor:
    Bash

    python manage.py migrate
    python manage.py runserver

    Acesse no navegador: http://127.0.0.1:8000

Desenvolvido por Lucas Elias 🚀
