#!/bin/sh

echo "#############################################"
echo "### Killing all containers.               ###"
echo "#############################################"
docker ps -a | awk '(NR != 1) && ($2 == "mb_flask_app") {print $1}' | \
    xargs docker rm -f

echo "\n"
echo "#############################################"
echo "### Removing docker images.               ###"
echo "#############################################"
docker images -a | awk '{if (NR!=1) {print $1}}' | xargs docker rmi

echo "\n"
echo "#############################################"
echo "### Building docker image and subnet...   ###"
echo "#############################################"
docker build -t mb_flask_app .
docker network rm mb_subnet && docker network create --subnet=10.0.0.0/16 mb_subnet

echo "\n"
echo "#############################################"
echo "### Starting UDS cluster...               ###"
echo "#############################################"
docker run -d -p 8081:8080 --ip=10.0.0.20 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20:8080" \
    -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10.0.0.24:8080,10.0.0.25:8080" mb_flask_app
docker run -d -p 8082:8080 --ip=10.0.0.21 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="WORKER" -e COORDINATOR="10.0.0.20:8080" mb_flask_app
docker run -d -p 8083:8080 --ip=10.0.0.22 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="WORKER" -e COORDINATOR="10.0.0.20:8080" mb_flask_app
docker run -d -p 8084:8080 --ip=10.0.0.23 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="WORKER" -e COORDINATOR="10.0.0.20:8080" mb_flask_app
docker run -d -p 8085:8080 --ip=10.0.0.24 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="WORKER" -e COORDINATOR="10.0.0.20:8080" mb_flask_app
docker run -d -p 8086:8080 --ip=10.0.0.25 --network=mb_subnet -e N=5 \
    -e NODE_TYPE="WORKER" -e COORDINATOR="10.0.0.20:8080" mb_flask_app
