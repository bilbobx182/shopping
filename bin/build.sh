docker kill $(docker ps -q)

docker build -t grocer_back -f backend.Dockerfile .
docker tag grocer_back:latest 325853407188.dkr.ecr.eu-west-1.amazonaws.com/grocer_back:latest
docker push 325853407188.dkr.ecr.eu-west-1.amazonaws.com/grocer_back:latest
#docker run -v /etc/ssl/taifu:/ssl  -p 8000:8000 grocer_back:latest

docker build -t grocer_front -f frontend.Dockerfile .
#docker run -d -v /etc/ssl/taifu:/ssl  -p 443:443  grocer_front:latest
