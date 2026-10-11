# Shop Ledger (Django)

Setup
1. python -m venv venv  &&  venv\Scripts\activate   (Windows)
2. pip install django
3. python manage.py migrate
4. python manage.py createsuperuser   (this account is the Admin)
5. python manage.py runserver  ->  open http://127.0.0.1:8000

Admin logs in, registers products, then adds cashiers on the Cashiers page.
Set SECRET_KEY and DEBUG=0 in the environment before putting it online.
