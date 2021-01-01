bind = "unix:stereo-tuning.sock"
umask = 7
workers = 3
# Access log - records incoming HTTP requests
accesslog = "/home/rudy/log/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/home/rudy/log/gunicorn.error.log"
# Whether to send Django output to the error log 
capture_output = True
# How verbose the Gunicorn error logs should be 
loglevel = "info"
