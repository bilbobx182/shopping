docker build -t grocer_front -f frontend.Dockerfile .
docker tag grocer_front:latest 325853407188.dkr.ecr.eu-west-1.amazonaws.com/grocer_front:latest
docker push 325853407188.dkr.ecr.eu-west-1.amazonaws.com/grocer_front:latest