# praktikum_new_diplom

ip: ```158.160.75.146```

domen: https://foodgramrugma.zapto.org

login: example@example.ru

pass: ```jhkjdhaskdKASHDKASDK```

Не забудьте создать ```.env```, пример есть в ```env_example```
Для запуска проекта на проде:
```
docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Для загрузки ингредиентов:
```
docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients
```

Для создания супер пользователя:
```
docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

Для запуска сервера разработки:
```
cd backend
python -m venv env
. env/bin/activate
python manage.py migrate
python manage.py runserver
```
