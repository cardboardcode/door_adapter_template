#!/usr/bin/env bash


docker run -it --rm \
    --name door_adapter_mock_test_c \
door_adapter_mock:humble /bin/bash -c \
"source /ros_entrypoint.sh && colcon test --packages-select door_adapter_mock --event-handlers console_cohesion+"
