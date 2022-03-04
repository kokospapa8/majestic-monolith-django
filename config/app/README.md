#build base image
## Xray
```
docker build -t 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/xray:latest config/docker/Dockerfile_xray
#v2
aws ecr get-login-password --profile=<profile_name> --region ap-northeast-2 | docker login  --username AWS --password-stdin 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com

aws ecr get-login-password --profile=daas_dev_kokospapa --region ap-northeast-2 | docker login  --username AWS --password-stdin 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com

docker push 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/xray:latest

```

----

## App
```
docker build -t 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/daas-server:latest -f config/docker/Dockerfile_local .
docker push 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/daas-server:latest


```

## Nginx
```
docker build -t 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/daas-nginx:latest -f config/docker/Dockerfile_nginx .
docker push 399932611745.dkr.ecr.ap-northeast-2.amazonaws.com/nginx:latest
```
