from __init__ import app
import logging
'''
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
'''



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9941)
