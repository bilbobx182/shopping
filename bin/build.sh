docker kill $(docker ps -q)

docker build -t grocer_back -f backend.Dockerfile .
docker run -p 8000:8000 grocer_back:latest
#docker run -d -p 8080:8080 grocer_back:latest
#docker build -t grocer_front -f frontend.Dockerfile .
#docker run -d --rm -p 80:80 grocer_front:latest
