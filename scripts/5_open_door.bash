#!/usr/bin/env bash

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{}' \
  http://127.0.0.1:8888/door/door_1/remoteopen
