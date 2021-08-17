#!/bin/sh

echo "#############################################"
echo "### Killing all containers.               ###"
echo "#############################################"
docker rm -f $(docker ps -a -q)
    

echo "\n"
echo "#############################################"
echo "### Removing docker images.               ###"
echo "#############################################"
docker rmi -f $(docker images -a -q)

echo "\n"
echo "######################################"
echo "### Taking down docker subnet...   ###"
echo "######################################"
docker network prune
