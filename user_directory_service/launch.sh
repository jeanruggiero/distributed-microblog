#!/bin/sh

docker run -p 8081:8080 --ip=10.0.0.20 --network=microblognet -e N=5 \
    -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
    -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
docker run -p 8082:8080 --ip=10.0.0.21 --network=microblognet -e N=5 \
    -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
    -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
# docker run -p 8082:8080 --ip=10.0.0.22 --network=microblognet -e N=5 \
#     -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
#     -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
# docker run -p 8082:8080 --ip=10.0.0.23 --network=microblognet -e N=5 \
#     -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
#     -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
# docker run -p 8082:8080 --ip=10.0.0.24 --network=microblognet -e N=5 \
#     -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
#     -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
# docker run -p 8082:8080 --ip=10.0.0.25 --network=microblognet -e N=5 \
#     -e NODE_TYPE="COORDINATOR" -e COORDINATOR="10.0.0.20" \
#     -e NODES="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10 .0.0.24:8080,10.0.0.25:8080" mbnode
