from __init__ import app
from gevent.pywsgi import WSGIServer
import logging


app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True



if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 80), app, log=app.logger) #, log=app.logger
    http_server.serve_forever()
    #app.run(debug=True, host='0.0.0.0', port=80)
