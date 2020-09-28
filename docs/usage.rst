=====
Usage
=====

First, you have to create a project with ``zemfrog``::

    $ zemfrog create frog


Application structure
---------------------

The application structure is as follows::

    frog (root directory)
    ├── api
    ├── auth
    ├── commands
    ├── extensions
    ├── mail
    ├── models
    ├── schema
    ├── services
    ├── config.py
    ├── Procfile
    ├── README.rst
    ├── requirements.txt
    └── wsgi.py

* ``api`` - This directory is for all REST API resources.
* ``auth`` - This directory is the default JWT authentication.
* ``commands`` - This directory is for the commands that will be registered in the flask command.
* ``extensions`` - This directory is for a list of flask extensions.
* ``mail`` - This directory is for the list of mail templates.
* ``models`` - This directory is for a list of sqlalchemy ORM models.
* ``schema`` - This directory is for the list of marshmallow schema models.
* ``services`` - This directory is for the celery task list.
* ``config.py`` - Flask application configuration file.
* ``Procfile`` - Configuration file for deploying on heroku.
* ``README.rst`` - A short description of how to run zemfrog applications.
* ``requirements.txt`` - List of application dependencies.
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
* ``APIS`` - List your REST API resources here.
* ``API_DOCS`` - Configuration for automation creates REST API documentation using ``flask-apispec``. Default value is ``True``.
* ``CREATE_DB`` - Configuration for automation creates tables of all models. Default value is ``True``, but I will remove this configuration in the future.

Yep! that's all the configuration for the zemfrog application.
However, you can also add configurations for celery and other flask extensions in config.py :)


Commands
--------

In the flask application there is a feature to add "own commands" to flask commands. However, these are not automatically added by flask. 
Don't worry, this behavior will be handled by zemfrog automatically.

Let's create a boilerplate command::

    $ flask command new foo

Now you have ``foo.py`` in the commands directory and you will see the ``command`` variable in the file ``foo.py``. 
This variable will be imported and added to the flask command by zemfrog automatically.

Then add a command to the ``COMMANDS`` configuration in config.py::

    COMMANDS = ['commands.foo']

Now you can see the command foo is registered in the application::

    $ flask foo


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

.. note::

    The route format will look like this ``(url, view, methods)``.

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
    Keep in mind, at this time the command to create a schema model will overwrite all previous schemas.
    See this `issue <https://github.com/zemfrog/zemfrog/issues/12>`_ for details.

Then create a schema for your ORM model::

    flask schema load

.. warning::

    Keep in mind, you have to create an API with the same name as your ORM model.
    And don't forget to add the ``--crud`` option.

And we can create a REST API::

    $ flask api new Product --crud

This REST API will not work if you haven't added it to the ``APIS`` config.
Let's add it to the config::

    APIS = ['api.product']
