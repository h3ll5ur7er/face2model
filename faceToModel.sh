#! /bin/bash

docker run --rm -v $PWD/data:/data:Z asjackson/vrn /runner/run.sh /data/$1

