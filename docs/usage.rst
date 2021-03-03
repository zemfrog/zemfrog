=====
Usage
=====

First, you have to create a project with ``zemfrog``::

    $ zemfrog create frog


Project Layouts
---------------

The application structure is as follows::

    frog (root directory)
    ├── api
    ├── auth
    ├── commands
    ├── extensions
    ├── middlewares
    ├── models
    ├── tasks
    ├── static
    ├── templates
    ├── templates/emails
    ├── config.py
    ├── Procfile
    ├── README.rst
    ├── requirements.txt
    ├── urls.py
    ├── views.py
    └── wsgi.py

* ``api`` - This directory is for all REST API resources.
* ``auth`` - This directory is the default JWT authentication.
* ``commands`` - This directory is for the commands that will be registered in the flask command.
* ``extensions`` - This directory is for a list of flask extensions.
* ``handlers`` - This directory is for error handlers.
* ``middlewares`` - This directory is a list of middleware.
* ``models`` - This directory is for a list of sqlalchemy ORM models.
* ``tasks`` - This directory is for the celery task list.
* ``static`` - Static files.
* ``templates`` - Templates folder.
* ``templates/emails`` - This directory is for the list of email templates.
* ``config.py`` - Flask application configuration file.
* ``Procfile`` - Configuration file for deploying on heroku.
* ``README.rst`` - A short description of how to run zemfrog applications.
* ``requirements.txt`` - List of application dependencies.
* ``urls.py`` - List your application endpoints.
* ``views.py`` - List of your app view functions.
* ``wsgi.py`` - Flask application here.

Assume if you already installed virtualenv and go run the application::

    $ cd frog
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ flask run


Configuration
-------------

There are several configurations in the zemfrog application, including:

* ``EXTENSIONS`` - List your flask extensions here.
* ``COMMANDS`` - List your commands here.
* ``BLUEPRINTS`` - List your blueprint here.
* ``ERROR_HANDLERS`` - List of error handlers.
* ``MIDDLEWARES`` - List of middleware here.
* ``APIS`` - List your REST API resources here.
* ``API_DOCS`` - Configuration for automation creates REST API documentation using ``flask-apispec``. Default value is ``True``.
* ``CREATE_DB`` - Configuration for automation creates tables of all models. Default value is ``True``, but I will remove this configuration in the future.
* ``APISPEC_SECURITY_DEFINITIONS`` - Follow this https://swagger.io/docs/specification/authentication/.
* ``APISPEC_SECURITY_PARAMS`` - Follow this https://swagger.io/docs/specification/authentication/
* ``APPS`` - List of sub applications.
* ``TASKS`` - Celery task list.
* ``STATICFILES`` - List of static files to serve.

Yep! that's all the configuration for the zemfrog application.
However, you can also add configurations for celery and other flask extensions in config.py :)


Routes
------

.. note::

    The route format specification is ``(url, view, methods)``.

Example::

    # urls.py

    routes = [
        ('/', views.index, ['GET']),
    ]

Commands
--------

In the flask application there is a feature to add "own commands" to flask commands. However, these are not automatically added by flask.
Don't worry, this behavior will be handled by zemfrog automatically.

Let's create a boilerplate command::

    $ flask command new foo

Now you have ``foo.py`` in the commands directory and you will see the ``command`` variable in the file ``foo.py``.
This variable will be imported and added to the flask command by zemfrog automatically.

Then add a command to the ``COMMANDS`` configuration in config.py::

    COMMANDS = ['foo']

Now you can see the command foo is registered in the application::

    $ flask foo


Error Handling
--------------

In zemfrog you can handle errors easily, you just need to make a boilerplate handler. Like this::

    $ flask handler new not_found

And in the ``handlers/not_found.py`` module there is a ``handler`` function which zemfrog will import automatically.

Now register to the ``ERROR_HANDLERS`` configuration. Like this::

    ERROR_HANDLERS = {
        404: "not_found"
    }

.. note::

    The format of the error handler is ``{code_or_exception: "error handler"}``


Multiple Static Files
---------------------

You can add more static files to serve via the ``STATICFILES`` configuration, like this::

    STATICFILES = [
        ("/assets", "assets", "assets")
    ]

Static file format values ​​are (``path``, ``endpoint``, ``static_folder``, ``static_host``).

.. note::

    the ``static_host`` value is optional


Background Tasks
----------------

In zemfrog, it is integrated with Celery for background tasks.
So you need to understand about celery. See here https://docs.celeryproject.org/en/stable/getting-started/introduction.html for more details.

And how do I make a background task?

All background tasks are in the ``tasks`` directory of the project layouts.
And in the ``tasks`` directory, a sample background task is also available.

.. code-block:: python

    from extensions.celery import celery
    from extensions.mail import mail


    @celery.task
    def send_email(*args, **kwds):
        mail.send_message(*args, **kwds)


.. note::
    If you want to create a background task, you have to use the ``celery`` app from the ``extensions`` directory.
    Like the sample above.


Blueprints
----------

Make a boilerplate blueprint::

    $ flask blueprint new account

The blueprint structure will look like this::

    account
    ├── __init__.py
    ├── routes.py
    ├── urls.py
    └── views.py

* ``routes.py`` - Your blueprint is here.
* ``urls.py``   - All your endpoints are here.
* ``views.py``  - All your view functions here.

Let's create 2 view functions::

    # account/views.py

    def login():
        return "login cuk"

    def logout():
        return "logout cuk"

Register the view function to the blueprint, otherwise your view function will not be in the blueprint.

.. code-block:: python

    # account/urls.py

    routes = [
        ('/login', views.login, ['POST']),
        ('/logout', views.logout, ['POST'])
    ]

Now all views will be listed on the blueprint. However, you need to register your blueprints in the flask app.
Add your blueprint name to the ``BLUEPRINTS`` configuration in config.py::

    BLUEPRINTS = ['account']

And, now you can see the blueprint ``account`` has been registered in the flask application::

    $ flask routes


Middlewares
-----------

In this section, I will explain how easy it is to create middleware.
Let's start by creating the boilerplate middleware::

    $ flask middleware new auth

The above command will create an auth.py file to the ``middlewares`` directory and in the auth.py file there is a function ``init_middleware``.
This function is to register your middleware in the flask application.

And register your middleware to config file::

    MIDDLEWARES = ["auth"]

API
---

zemfrog is specially designed for building REST APIs quickly.
In zemfrog you can create a basic CRUD or just boilerplate API.

All API resources are located in the ``api`` directory.

Let's start by creating an API resource::

    $ flask api new article

Now you have the article API resource::

    api
    ├── article.py
    ├── __init__.py

In the article API resource there are variables ``docs``, ``endpoint``, ``url_prefix`` and ``routes``.


* ``docs`` - For your REST API documentation, see `here <https://flask-apispec.readthedocs.io/en/latest/api_reference.html#flask_apispec.annotations.doc>`_.
* ``endpoint`` - For naming your view function. So if the view name is ``add`` then it will become ``article_add``.
* ``url_prefix`` - URL prefix for the API resource.
* ``routes`` - All of your API endpoints.

Now, we will create a basic REST API.

.. note::

    You cannot create a REST API if you don't have an ORM model for that API.

Let's create a ``Product`` model.

Change the file ``models/__init__.py`` to be like this::

    from extensions.sqlalchemy import db
    from sqlalchemy import Column, String, Integer

    class Product(db.Model):
        id = Column(Integer, primary_key=True)
        name = Column(String)

.. warning::

    Keep in mind, you have to create an API with the same name as your ORM model.
    And don't forget to add the ``--crud`` option.

And we can create a REST API::

    $ flask api new Product --crud

This REST API will not work if you haven't added it to the ``APIS`` config.
Let's add it to the config::

    APIS = ['product']


JWT Authentication
------------------

One of my favorite features is this.

Why? with this you are very easy and clear how you interact with the REST API which is protected with JWT authentication.

This feature is inspired by the `FastAPI framework <https://github.com/tiangolo/fastapi>`_ and adopted from the project https://github.com/tiangolo/full-stack-flask-couchdb.

All REST APIs are protected with JWT authentication by default. However, if you wish to disable it, you only need to commenting ``authenticate`` decorators.


Multiple Application
--------------------

In zemfrog you can easily create sub applications.

Let's start by creating a sub application as below::

    $ flask app new sub

And add your sub-application to the ``APPS`` configuration in the config.py file::

    APPS = ["sub"]

You can also add sub-applications using a dictionary::

    APPS = [
        {
            "name": "sub", # Your application name.
            "path": "/sub-app", # Application URL prefix. (optional)
            "help": "Sub app command" # Help messages for your app commands. (optional)
        }
    ]

To manage nested applications you just need to use the ``sub`` command::

    $ flask sub
