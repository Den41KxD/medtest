pipenv run alembic upgrade head

pipenv run flask run --host=0.0.0.0

pipenv cd tests
pipenv python pytest tests.py
pipenv cd ..
