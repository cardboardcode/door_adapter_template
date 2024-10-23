# Copyright 2024 Bey Hao Yun, Gary.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import socket
import urllib3
import requests
from rmf_door_msgs.msg import DoorMode


class DoorClientAPI:
    def __init__(self, node, config):
        self.name = 'rmf_door_adapter'
        self.timeout = 5  # seconds
        self.debug = False
        self.connected = False
        self.node = node
        self.config = config  # use this config to establish connection

        self.header = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"}
        self.data = {}

        count = 0
        self.connected = True
        while not self.check_connection():
            if count >= self.timeout:
                print("Unable to connect to door client API.")
                self.connected = False
                break
            else:
                print("Unable to connect to door client API. Attempting to reconnect...")
                count += 1
            time.sleep(1)

    def check_connection(self):
        # Test connectivity
        try:
            res = requests.post(
                url=self.config["api_endpoint"]+"/system/ping",
                headers=self.header,
                json=self.data,
                timeout=1.0)
            res.raise_for_status()
            if res.status_code == 200:
                return True
            else:
                return False
        except (
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as e:
            print(f"Connection Error: {e}")
            return False

    def open_door(self, door_id):

        path = self.config["api_endpoint"]+f"/door/{door_id}/remoteopen"

        try:
            response = requests.post(
                url=path,
                headers=self.header,
                timeout=1.0)
            if response:
                result = response.json()["body"]
                if (result.get("result") is not None):
                    return True
                else:
                    print("door could not perform open")
                    return False
            else:
                print("Invalid response received")
                return False
        except (
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as e:
            print("Connection Error. "+str(e))
            return False

    def get_mode(self, door_id):

        path = self.config["api_endpoint"]+f"/door/{door_id}/status"

        try:
            response = requests.post(
                url=path,
                headers=self.header,
                timeout=1.0)
            if response:
                state = response.json().get("body").get("doorState")
                if state is None:
                    return DoorMode.MODE_UNKNOWN
                elif state == "closed":
                    return DoorMode.MODE_CLOSED
                elif state == "betweenOpenandClosed":
                    return DoorMode.MODE_MOVING
                elif state == "open":
                    return DoorMode.MODE_OPEN
                elif state == "OFFLINE":
                    return DoorMode.MODE_OFFLINE
            else:
                return 4
        except (
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as e:
            print("Connection Error. "+str(e))
            return DoorMode.MODE_UNKNOWN
