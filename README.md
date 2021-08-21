# distributed-microblog
#### CS6650 Final Project - Distributed Microblogging Application
###### Austin Chow, Jean Ruggiero, Phillip Vo

To run the distributed microblog application, first start the User Directory Service by following the instructions below. Once the UDS is up and
 running, any number of client application instances may be started in separate terminal windows to communicate with one another.

## Starting the User Directory Service (UDS)

### Automatically with docker-compose (recommended)

Start the UDS from within the `distributed-microblog/user_directory_service` directory.

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


### Manually with docker commands (as a backup in case the above doesn't work)

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


## Running the Peer Application

Run the client application from the `distributed-microblog` directory with:
```
microblog_client.py u p
```

positional arguments:
```
  u           The username to connect with.
  p           The port on which to run the application.
```

optional arguments:
```
  -h, --help  show this help message and exit
```

example:
```
microblog_client.py jean 8111
```

When the client application has started successfully, it will print a menu of options. The user has the option to write a new post, like an
 existing post, or repost an existing post. In addition, the user can query his or her own posts, likes, and reposts by selecting the option to get
  posts, likes, or reposts and entering their own username. The user can get the posts, reposts, or likes for any other user who is actively running
   the microblogging application at the time of the request.
   
*Note*: to run multiple peer application instances on the same machine, each must be run on a unique port.



