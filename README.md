# 🧰 Sistema de Agendamento de Manutenção — Oficina

Este projeto é um sistema web desenvolvido em **Django** para gerenciar **clientes, veículos, serviços e agendamentos** de uma oficina mecânica.  
O objetivo é facilitar o controle de manutenções, horários e status dos serviços realizados.


## 🚀 Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [Django 5+](https://www.djangoproject.com/)
- SQLite

## ⚙️ Funcionalidades Principais

- Cadastro de **clientes**
- Cadastro de **veículos** associados a clientes
- **Agendamento de manutenção** com data e hora
- Associação de **serviços** a cada agendamento
- Controle de **status**: Pendente, Em andamento, Concluído, Cancelado
- Acesso administrativo via `/admin`

## 🧩 Instalação e Execução

1. **Clonar o repositório**
   ```bash
   git clone git@github.com:cesarapires/projeto-web.git
   cd projeto-web
    ```

2. **Criar e ativar o ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar django**

   ```bash
   pip install django
   ```

4. **Aplicar migrações**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Criar usuário administrador**

   ```bash
   python manage.py createsuperuser
   ```

6. **Executar o servidor**

   ```bash
   python manage.py runserver
   ```

7. **Acessar o sistema**

   ```
   http://127.0.0.1:8000/admin/
   ```
