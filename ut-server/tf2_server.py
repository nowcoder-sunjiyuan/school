import argparse
import time

from flask import Flask, request, Response

from home_rec import home_rec_server_A
from register import LifeCycle
from utils import logger
# from utils import middleware
from utils import multi_proc_service_v3

app = Flask(__name__)
# app.wsgi_app = middleware.Middleware(app.wsgi_app, logger, tokens=20)

print(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World!"

@app.route("/home/rank/v8/esmm", methods=["POST"])
def home_rank_v8():
    return Response(home_rank_v8_handler.communicate_with_worker(request.get_data()),
                    mimetype='application/x-protobuf')


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()

    parser.add_argument('--service', type=str, default='ut-tf2-rank', help='consul service name')
    parser.add_argument('--port', type=int, default=9092, help='service port')
    parser.add_argument('--env', type=str, default='local', help='local, dev, prod')
    FLAGS, unparsed = parser.parse_known_args()

    fine_rank_num = 5 if FLAGS.env == 'prod' else 2
    rough_rank_num = 4 if FLAGS.env == 'prod' else 2

    home_rank_v8_handler = multi_proc_service_v3.BaseHandler(home_rec_server_A.HomeRecServerA,
                                                             process_num=fine_rank_num)

    end_time = time.time()
    elapsed_time = 1000 * (end_time - start_time)
    logger.info('Starting the server... (cost: %dms)', elapsed_time)
    lc = LifeCycle(f'{FLAGS.service}', FLAGS.port)
    # 注册，参数是上面parser一堆
    lc.register(cost=elapsed_time)
    app.run(host='0.0.0.0', port=FLAGS.port, debug=False)