Role Based Access Control
=========================

Sometimes we need to protect endpoints with role access and role permissions.
What for? to grant access to specific users.

Let's get started...


First Step
----------

We have to create a REST API first.
Let's create::

    $ flask api new User --crud


Create User
-----------

First we need to create a role for the user::

    $ flask role new admin -d "Admin Role"

Now we create an admin user::

    $ flask user new admin@email.com -r admin

And input the required data which appears at the terminal.

What if I create a user without role access? of course you can!


Protect Endpoints With Roles
----------------------------

All you need is to add an authenticate decorator with a roles to the view, like this::

    @authenticate(roles={"admin": []})
    # your view here...

For example, edit the ``get`` view decorator in the ``api/user.py`` file, as follows::

    @authenticate(roles={"admin": []})
    @marshal_with(ReadUserSchema(many=True), 200)
    def get():
        """
        Read all data.
        """

        data = User.query.all()
        return data

Now the ``/api/user/get`` endpoint can be accessed by admin only!


Protect Endpoint With Role Permissions
--------------------------------------

First you have to create role permissions first::

    $ flask permission new can_all -d "Permission to do anything"

And add permission to the ``authenticate`` decorator, for example::

    @authenticate(roles={"admin": ["can_all"]})
    @marshal_with(ReadUserSchema(many=True), 200)
    def get():
        """
        Read all data.
        """

        data = User.query.all()
        return data


Now the ``/api/user/get`` endpoint can only be accessed by admins who have the permission ``can_all``!
