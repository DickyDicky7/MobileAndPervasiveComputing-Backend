# MobileAndPervasiveComputing-Backend

A simple hello world express server. Run it in the terminal with

```
npm run start
```

and cmd+click (or ctrl+click) on "http://localhost:3000" to access the server.

```
https://waseminarcnpm2.azurewebsites.net/
```

```
docker-compose up --build
```

```
docker stop $(docker ps -a -q)
```

```
docker tag redis/redis-stack:7.0.6-RC9 rnseminarcnpm2.azurecr.io/redis-stack:7.0.6-RC9
docker tag mongodb/mongodb-atlas-local:latest rnseminarcnpm2.azurecr.io/mongodb-atlas-local:latest
docker login rnseminarcnpm2.azurecr.io
docker push rnseminarcnpm2.azurecr.io/seminarcnpmbackendnodejsserver:latest
docker push rnseminarcnpm2.azurecr.io/seminarcnpmbackendpythonserver:latest
docker push rnseminarcnpm2.azurecr.io/redis-stack:7.0.6-RC9
docker push rnseminarcnpm2.azurecr.io/mongodb-atlas-local:latest
```

```
docker-compose up --build
docker ps     #get container id of rtsp/mongosh
docker exec   -it <container id of rtsp/mongosh> bash
$ mongosh $MONGO_URL 
```

```
docker system prune -a
docker volume prune -a
```

'''
snake_case -> camelCase
'''













