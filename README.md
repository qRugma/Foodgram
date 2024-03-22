# praktikum_new_diplom

ip: 158.160.75.146
domen: https://foodgramrugma.zapto.org
pass: jhkjdhaskdKASHDKASDK
login: example@example.ru

Для запуска проекта на проде:
```
docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Для загрузки ингредиентов:
```
docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients
```
