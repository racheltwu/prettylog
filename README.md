PrettyLog
================

About
-----
PrettyLog is a pluggable Django app that uses Django's logging interface to log your project's errors with full trace 
to a text file. It creates a view for you to view this text file in a nicely formatted html file with similar errors 
grouped and counted (much like Sentry does), sorted from newest to oldest. Staff users can view the errors at 
*http://yourdomain/errors*. This app is useful for simple applications where Sentry installation is difficult or 
impossible (I needed it for use on Dreamhost).


Installation
------------

1. Pip install from GitHub:

        pip install git+git://github.com/racheltwu/prettylog

2. Add `prettylog` to your `INSTALLED_APPS` in your settings file:

        INSTALLED_APPS = (
            ...
            'prettylog',
            ...
        )

3. Set the `LOG_DIR` variable in your settings file where you want your logs to be located. Make sure that folder 
   exists.

        LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

5. Create or update the `LOGGING` variable in your settings file. Prettylog requires this specific formatter and 
   handler, but you can define a specific logger to log only specific errors instead of catching all of them.

        LOGGING = {
            'version': 1,
            'formatters': {
                'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}
            },
            'handlers': {
                'catchall': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'verbose',
                    'filename': os.path.join(LOG_DIR, 'prettylog.txt'),
                    'maxBytes': 5 * 2 ** 20,  # 5 MiB
                    'backupCount': 3,
                },
            },
            'loggers': {
                '': {
                    'handlers': ['catchall'],
                    'level': 'INFO',
                }
            }
        }

4. Add this url to your `urls.py` to make your error log available at *http://yourdomain.com/errors*:

        (r'^errors/$', 'prettylog.views.error_log', {}, 'errors'),


Usage
-----

You can change the default CSS if desired by creating a CSS file at `STATIC_URL/css/prettylog.css`. If your CSS lives 
in a different location, you can change this location by setting `LOG_CSS_PATH` in your settings.

        LOG_CSS_PATH = os.path.join(STATIC_URL, 'css', 'prettylog', 'style.css')

Just delete your `prettylog.txt` file to clear the error list and it will be regenerated when new errors arise.

Screenshot
----------

![](https://github.com/racheltwu/prettylog/raw/master/screenshot.jpg "PrettyLog Screenshot")
