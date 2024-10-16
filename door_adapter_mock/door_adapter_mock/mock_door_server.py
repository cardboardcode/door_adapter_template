#! /usr/bin/env python3

import time
import flask
import threading
from flask import request, jsonify

# TODO(cardboardcode): Create Door class that mimicks behaviour of real doors.
curr_doorState = "closed"

def main():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    # TODO(cardboardcode): Read config.yaml and determine number of doors with their corresponding names.
    # Start them all off closed.

    # TODO(cardboardcode): Create a thread that spins off and instantiates Door objects.

    def simulate_opening():
        # Update doorState immediately to moving:
        global curr_doorState
        curr_doorState = "betweenOpenandClosed"

        time.sleep(2)

        curr_doorState = "open"

        time.sleep(10)

        curr_doorState = "betweenOpenandClosed"

        time.sleep(2)

        curr_doorState = "closed"

    def simulate_closing():
        # Update doorState immediately to moving:
        global curr_doorState
        curr_doorState = "betweenOpenandClosed"

        time.sleep(2)

        curr_doorState = "closed"
    

    @app.route('/door/status', methods=['POST'])
    def device_status():
        global curr_doorState
        data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"doorState": curr_doorState}}
        return jsonify(data)

    @app.route('/door/remoteopen', methods=['POST'])
    def door_open_command():
        global curr_doorState
        if curr_doorState == "open":
            data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"Door already closed. Ignoring..."}}
        else:
            data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"open command sent"}}

            t = threading.Thread(target=simulate_opening)
            t.start()

        return jsonify(data)
    
    @app.route('/door/remoteclose', methods=['POST'])
    def door_close_command():
        global curr_doorState
        if curr_doorState == "closed":
            data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"Door already closed. Ignoring..."}}
        else:
            data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"close command sent"}}

            t = threading.Thread(target=simulate_closing)
            t.start()

        return jsonify(data)


    app.run(port=8888)

if __name__ == '__main__':
    main()    
