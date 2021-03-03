=======
zemfrog
=======

.. image:: https://raw.githubusercontent.com/zemfrog/zemfrog/master/docs/_static/logo.png
    :target: https://zemfrog.readthedocs.io
    :alt: zemfrog logo

.. image:: https://img.shields.io/pypi/v/zemfrog.svg?style=for-the-badge
    :target: https://pypi.python.org/pypi/zemfrog

.. image:: https://img.shields.io/pypi/status/zemfrog.svg?style=for-the-badge
    :target: https://pypi.python.org/pypi/zemfrog/

.. image:: https://img.shields.io/pypi/dm/zemfrog?logo=python&style=for-the-badge
    :target: https://pypi.python.org/pypi/zemfrog/

.. image:: https://img.shields.io/travis/zemfrog/zemfrog.svg?style=for-the-badge
    :target: https://travis-ci.com/zemfrog/zemfrog

.. image:: https://readthedocs.org/projects/zemfrog/badge/?version=latest&style=for-the-badge
    :target: https://zemfrog.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status



Zemfrog is a simple framework based on flask for building a REST API quickly.
Which focuses on building a customizable, flexible and manageable REST API!


Motivation
----------

Since 2019 I have studied backend development. And I know exactly, development on the backend is very difficult and complex.
For example when a user requests a password reset, the user has to wait for the process on the backend to finish to send an email. That's because the process isn't asynchronous.
And also we have to test the REST API with tools like `Postman <https://www.postman.com/>`_, `Insomnia <https://insomnia.rest/>`_, etc. If we use that tool it will take a long time, because we have to set up endpoints, etc.

Zemfrog came up with simplifying this behavior by adding background jobs with `celery <https://docs.celeryproject.org/en/stable/>`_ and also integrating with swagger-ui using `flask-apispec <https://github.com/jmcarp/flask-apispec>`_ to test the REST API.
This project is heavily inspired by `FastAPI <https://fastapi.tiangolo.com/>`_ and `Django <https://www.djangoproject.com/>`_ Framework.


Why zemfrog?
------------

Zemfrog is equipped with advanced features including:

* Solid application structure.
* Automatically generate REST API.
* Built-in JWT authentication.
* RBAC support.
* Automatically generate API documentation (swagger-ui).
* Background jobs support.
* Database migration based on application environment.
* And much more...


Donate & Support
----------------

Keep in mind that donations are very important to me, because currently I am working alone to develop this project.
It takes a lot of time and energy. If this project is useful, please give me any support. I really appreciate it.

You can donate to me via:

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/aprilahijriyan

.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
    :target: https://www.paypal.me/aprilahijriyan


.. image:: https://c5.patreon.com/external/logo/become_a_patron_button.png
    :target: https://www.patreon.com/bePatron?u=20603237


Links
-----

* Homepage: https://github.com/zemfrog/zemfrog
* Documentation: https://zemfrog.readthedocs.io
* License: `MIT <https://github.com/zemfrog/zemfrog/blob/master/LICENSE>`_


Credits
-------

* `Flask <https://github.com/pallets/flask>`_
* `Cookie Cutter <https://github.com/cookiecutter/cookiecutter>`_
