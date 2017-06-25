# API Gateway for Docker

### Run

This is api gateway for docker, you can go to compose folder and run with

```bash
docker-compose up -d
```

if you wonder run alone, run with

```bash
docker run -d -p 9011:9011 -v /var/run/docker.sock:/var/run/docker.sock playniuniu/docker-api-gateway
```
