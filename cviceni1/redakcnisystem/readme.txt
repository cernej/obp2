Jak zprovoznit projekt "redakcnisystem":

> virtualenv -p python3 .virtualenv
> source .venv/bin/activate
(.venv) > pip install -r requirements.txt
(.venv) > ./manage.py migrate
(.venv) > ./manage.py runserver