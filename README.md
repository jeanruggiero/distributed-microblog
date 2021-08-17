# distributed-microblog
CS6650 Final Project - Distributed Microblogging Application



## Starting the User Directory Service (UDS)

### Manually with docker commands

Prepare your environment with:
```shell script
docker network prune
```

From the `user_directory_service` run:
```shell script
./launch.sh
```

If there are issues with any of docker containers, images, or networks, you can
nuke all docker objects with the `clean.sh` script.

**Note**: UDS will be accessible on _localhost_ at any port from _8080_ to _8084_

### Automatically with docker-compose

* Make sure docker containers, images, and networks are cleaned
```shell script
docker system prune -a
```

Start up UDS cluster
```shell script
docker-compose up -d
```

Shut down UDS
```shell script
docker-compose down
```

To force rebuilding docker images, you can add a flag when calling
docker-compose
```shell script
docker-compose up --build -d
```

**Note**: UDS will be accessible at _localhost:8080_
