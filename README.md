# distributed-microblog
CS6650 Final Project - Distributed Microblogging Application



## Starting the User Directory Service (UDS)

From the `user_directory_service` run:
```shell script
docker build -t mbnode .
```

Next, create a subnet with
```shell script
docker network create --subnet=10.0.0.0/16 microblognet
```

Start the UDS with
```shell script
./launch.sh
```
