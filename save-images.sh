echo "Saving codehub-backend ... "
docker save -o codehub-backend.tar codehub-backend
echo "Saving codehub-nginx ... "
docker save -o codehub-nginx.tar codehub-nginx
echo "Saving codehub-postgres ... "
docker save -o codehub-postgres.tar codehub-postgres
echo "Saving codehub-frontend ... "
docker save -o codehub-frontend.tar codehub-frontend
