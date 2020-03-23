echo "Started building backend ..."
docker build -t codehub-backend:latest -f dockerfiles/django .
echo "Started building nginx image ..."
docker build -t codehub-nginx:latest -f dockerfiles/nginx .
echo "Started building postgres image ..."
docker build -t codehub-postgres:latest -f dockerfiles/postgres .