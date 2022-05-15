import logging.config
import os
import random
import time
from http.client import BAD_REQUEST, NOT_FOUND

from flask import Flask, request, Response

from RequestError import RequestError
from logger import log_settings
from response import BaseResponse, ResponseCode
from wrapper import catch_and_respond

app = Flask(__name__)

logging.config.dictConfig(log_settings)
DOGGY_PATH = "static/dogs/"

files = os.listdir(DOGGY_PATH)
logging.info(f"{files}")
random.seed(time.time())
doggy_length = len(files)
logging.info("There are {} doggy in database XD".format(doggy_length))


@app.route('/api/rand-doggy', methods=['GET'])
@catch_and_respond
def rand_doggy():
    index = random.randint(1, doggy_length) - 1
    results = {"name": files[index], "comment": "祝你天天开心！"}
    return BaseResponse(code=ResponseCode.OK, msg="ok", results=results).to_json()


@app.route('/api/get-doggy', methods=['GET'])
@catch_and_respond
def get_doggy():
    name = request.args.get("name", "", type=str) + '.gif'
    if name == "":
        raise RequestError(code=ResponseCode.BAD_REQUEST, message="No doggy name found.", http_code=BAD_REQUEST)
    doggy_file = os.path.join(DOGGY_PATH, name)
    if not os.path.exists(doggy_file):
        raise RequestError(code=ResponseCode.NOT_FOUND, message="No doggy named {}".format(name), http_code=NOT_FOUND)

    return Response(open(doggy_file, 'rb'), mimetype="image/jpeg")


if __name__ == '__main__':
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080)
