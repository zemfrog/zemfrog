{{name}}
=======

This project uses `zemfrog <https://github.com/zemfrog/zemfrog>`_


Usage
=====

Assume if you already installed virtualenv and go run the application::

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ flask run

Run the smtp server::

    $ python -m smtpd -n -d -c DebuggingServer


.. note::
    Before running Celery worker, you need to have redis installed on your device.

Run the celery worker::

    $ celery -A wsgi:celery worker

And everything is ready, now go to http://127.0.0.1:5000/docs.


Credits
=======

* `zemfrog <https://github.com/zemfrog/zemfrog>`_
