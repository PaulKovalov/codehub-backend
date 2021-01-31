docker tag codehub-backend:latest code-hub.org:5000/codehub-backend:latest
docker tag codehub-nginx:latest code-hub.org:5000/codehub-nginx:latest
docker tag codehub-postgres:latest code-hub.org:5000/codehub-postgres:latest
docker tag codehub-frontend:latest code-hub.org:5000/codehub-frontend:latest
docker tag codehub-celery:latest code-hub.org:5000/codehub-celery:latest
docker tag codehub-celery-beat:latest code-hub.org:5000/codehub-celery-beat:latest

docker push code-hub.org:5000/codehub-backend:latest
docker push code-hub.org:5000/codehub-frontend:latest
docker push code-hub.org:5000/codehub-nginx:latest
docker push code-hub.org:5000/codehub-postgres:latest
docker push code-hub.org:5000/codehub-celery:latest
docker push code-hub.org:5000/codehub-celery-beat:latest
