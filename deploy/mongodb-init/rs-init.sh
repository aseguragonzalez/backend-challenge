#!/bin/bash

delay=10
host=db
replica=dbrs

while getopts h:d:r: flag
do
    case "${flag}" in
        h) host=${OPTARG};;
        d) delay=${OPTARG};;
        r) replica=${OPTARG};;
    esac
done

echo "****** Waiting for ${delay} seconds for replicaset configuration ******"

sleep $delay

echo "****** Set node ${host} as primary ******"

mongo --host $host <<EOF
var config = {
    "_id": "${replica}",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "${host}:27017",
            "priority": 2
        }
    ]
};
rs.initiate(config, { force: true });
EOF

echo "****** Waiting for ${delay} seconds for replicaset configuration to be applied ******"

sleep $delay

echo "****** end primary node setup ******"
