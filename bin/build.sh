docker kill $(docker ps -q)

docker build -t grocer_back -f backend.Dockerfile .
docker run -v /etc/ssl/taifu:/ssl  -p 8000:8000 grocer_back:latest

docker build -t grocer_front -f frontend.Dockerfile .
docker run -d -v /etc/ssl/taifu:/ssl  -p 443:443  grocer_front:latest
