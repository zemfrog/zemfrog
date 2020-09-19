${name}
=======

Project ini menggunakan `zemfrog <https://github.com/zemfrog/zemfrog>`_


Usage
=====

Jalankan aplikasi::

    $ pip install -r requirements.txt
    $ flask run

Jalankan smtp server::

    $ python -m smtpd -n -d -c DebuggingServer

Jalankan celery worker::

    $ celery -A wsgi:celery worker

Dan semuanya sudah siap, sekarang pergi ke http://127.0.0.1:5000/docs.


Credits
=======

* `zemfrog <https://github.com/zemfrog/zemfrog>`_
