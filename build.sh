echo "Started building backend ..."
docker build -t codehub-backend:latest -f dockerfiles/django .
echo "Started building nginx image ..."
docker build -t codehub-nginx:latest -f dockerfiles/nginx .
echo "Started building postgres image ..."
docker build -t codehub-postgres:latest -f dockerfiles/postgres .
echo "Started building celery image ..."
docker build -t codehub-celery:latest -f dockerfiles/celery .
echo "Started building celery-beat image ..."
docker build -t codehub-celery-beat:latest -f dockerfiles/celery-beat .