#  скопировал с foodgram'а. Нужно переделать.
docker compose stop
docker container rm -f foodgram-backend-1
docker image rm foodgram-backend
docker compose -f docker-compose.yml up --build -d
docker compose -f docker-compose.yml exec backend python manage.py makemigrations api
docker compose -f docker-compose.yml exec backend python manage.py makemigrations food
docker compose -f docker-compose.yml exec backend python manage.py makemigrations users
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
