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
import yaml
import flask
import threading
from flask import jsonify

# TODO(cardboardcode): Create Door class that mimicks behaviour of real doors.
curr_doorState = "closed"
door_obj_array = []


class Door():
    def __init__(
            self, door_name: str,
            door_auto_closes: bool,
            continuous_status_polling: bool,
            door_signal_period=3,
            curr_doorState="closed"):
        self.door_name = door_name
        self.door_auto_closes = door_auto_closes
        self.continuous_status_polling = continuous_status_polling
        self.door_signal_period = door_signal_period
        self.curr_doorState = curr_doorState


def load_config(file_path):
    """

        Load the YAML configuration file.

    :param file_path: Path to the YAML file
    :return: Parsed YAML data as a dictionary
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)  # Load YAML file safely
        return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None


def main():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    config_filepath = "/door_adapter_mock_ws/src/door_adapter_mock/configs/config.yaml"
    config = load_config(config_filepath)

    global door_obj_array
    doors = config.get('doors')
    for door_id in doors:
        door_id = door_id
        door_auto_closes = doors[door_id]['door_auto_closes']
        continuous_status_polling = doors[door_id]['continuous_status_polling']
        door_signal_period = doors[door_id]['door_signal_period']
        door_obj = Door(
            door_name=door_id,
            door_auto_closes=door_auto_closes,
            continuous_status_polling=continuous_status_polling,
            door_signal_period=door_signal_period
        )
        door_obj_array.append(door_obj)

    for door_obj in door_obj_array:
        print(f"[door_obj_array] door_id = {door_obj.door_name}")

    def simulate_opening(door_id):
        # Update doorState immediately to moving:

        sel_door_obj = None
        global door_obj_array
        for door_obj in door_obj_array:
            if door_obj.door_name == door_id:
                sel_door_obj = door_obj
                break

        if sel_door_obj is None:
            print(f"[ERROR] - Unable to find door_obj: {door_id}. Ignoring...")
            print(f"Available door_objs: {door_obj_array}")
            return
        sel_door_obj.curr_doorState = "betweenOpenandClosed"
        time.sleep(2)
        sel_door_obj.curr_doorState = "open"

        if sel_door_obj.door_auto_closes:
            time.sleep(10)
            sel_door_obj.curr_doorState = "betweenOpenandClosed"
            time.sleep(2)
            sel_door_obj.curr_doorState = "closed"

    def simulate_closing(door_id):
        # Update doorState immediately to moving:

        sel_door_obj = None
        global door_obj_array
        for door_obj in door_obj_array:
            if door_obj.door_name == door_id:
                sel_door_obj = door_obj
                break

        if sel_door_obj is None:
            print(f"[ERROR] - Unable to find door_obj: {door_id}. Ignoring...")
            print(f"Available door_objs: {door_obj_array}")
            return

        sel_door_obj.curr_doorState = "betweenOpenandClosed"

        time.sleep(2)

        sel_door_obj.curr_doorState = "closed"

    @app.route('/system/ping', methods=['POST'])
    def connection_status():
        data = {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
                },
            "body": {"isSuccess": True}}
        return jsonify(data)

    @app.route('/door/<door_id>/status', methods=['POST'])
    def device_status(door_id):

        curr_doorState = None
        global door_obj_array
        for door_obj in door_obj_array:
            if door_obj.door_name == door_id:
                curr_doorState = door_obj.curr_doorState
                break

        if curr_doorState is None:
            print("[ERROR] - Unable to find door_obj:"
                  f" {door_id}. Setting default OFFLINE...")
            print(f"Available door_objs: {door_obj_array}")
            curr_doorState = "OFFLINE"

        data = {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
                },
            "body": {"doorState": curr_doorState}}
        return jsonify(data)

    @app.route('/door/<door_id>/remoteopen', methods=['POST'])
    def door_open_command(door_id):
        global curr_doorState
        if curr_doorState == "open":
            data = {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                "body": {"result": "Door already closed. Ignoring..."}}
        else:
            data = {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                "body": {"result": "open command sent"}}

            t = threading.Thread(target=simulate_opening, args=[door_id])
            t.start()

        return jsonify(data)

    @app.route('/door/<door_id>/remoteclose', methods=['POST'])
    def door_close_command(door_id):
        global curr_doorState
        if curr_doorState == "closed":
            data = {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                "body": {"result": "Door already closed. Ignoring..."}}
        else:
            data = {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                "body": {"result": "close command sent"}}

            t = threading.Thread(target=simulate_closing)
            t.start()

        return jsonify(data)

    app.run(port=8888)


if __name__ == '__main__':
    main()
