
python3 -m venv env
// activate env
pip install -r requirements.txt
python3 manage.py migrate

# pierwsza inicjacja bazy danych wraz z wypełnieniem bazy danych oraz utworzenie superusera

# email="admin@admin.io",
# password="admin",

# email="user@mail.pl",
# passowrd ="user",

python3 manage.py initdata

python3 manage.py runserver 

# http://127.0.0.1:8000/swagger/
# http://127.0.0.1:8000/login/
