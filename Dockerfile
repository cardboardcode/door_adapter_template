FROM ros:humble-ros-base

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-rmf-door-msgs \
        python3-pip && \
        pip3 install flask-socketio websockets websocket-client requests && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
WORKDIR /door_adapter_mock_ws/src
COPY ./door_adapter_mock door_adapter_mock/

# Setup the workspace
WORKDIR /door_adapter_mock_ws
RUN apt-get update && rosdep install --from-paths src --ignore-src --rosdistro=$ROS_DISTRO -y \
  && rm -rf /var/lib/apt/lists/*

# # Build the workspace
RUN . /opt/ros/$ROS_DISTRO/setup.sh \
  && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release

# # Ensure the entrypoint script sources the ROS setup
RUN echo 'source /door_adapter_mock_ws/install/setup.bash' >> /ros_entrypoint.sh

# # Ensure proper permissions for entrypoint
RUN chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]

