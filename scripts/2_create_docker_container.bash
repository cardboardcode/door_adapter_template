#!/usr/bin/env bash

CONFIG_FILE_PATH="/door_adapter_mock_ws/src/door_adapter_mock/configs/config.yaml"

docker run -it --rm \
    --name door_adapter_mock_c \
    --network host \
    -v /dev/shm:/dev/shm \
    -v ./door_adapter_mock/configs/config.yaml:$CONFIG_FILE_PATH \
door_adapter_mock:humble /bin/bash -c \
"source /ros_entrypoint.sh && ros2 launch door_adapter_mock run.launch.xml config_file:=$CONFIG_FILE_PATH"