User Management
===============

We provide commands to make it easier to manage users, roles and role permissions.


User command
-------------

.. code-block::

    Usage: flask user [OPTIONS] COMMAND [ARGS]...

        User manager.

    Options:
        --help  Show this message and exit.

    Commands:
        drop    Drop users.
        list    Show users.
        new     Create user.
        remove  Remove user.
        update  Update user.


new
^^^

Create new users::

    $ flask user new user@email.com

And enter user data, such as first name, last name and password.



remove
^^^^^^

Delete user::

    $ flask user remove user@email.com


update
^^^^^^

Update user::

    $ flask user update user@email.com


list
^^^^

Show users::

    $ flask user list


drop
^^^^

Drop users::

    $ flask user drop



Role command
-------------

.. code-block::

    Usage: flask role [OPTIONS] COMMAND [ARGS]...

        Access role manager.

    Options:
        --help  Show this message and exit.

    Commands:
        drop    Drop roles.
        list    Show roles.
        new     Create role.
        remove  Remove role.
        update  Update role.

new
^^^

Create new roles::

    $ flask role new admin -d "Admin Role"

You can also add permissions to roles::

    $ flask role new admin -d "Admin Role" -p "can_post,can_update"

.. note::

    Keep in mind, you must first create permissions on the database.
    Before you reference permissions to the role.


remove
^^^^^^

Delete role::

    $ flask role remove admin


update
^^^^^^

Update role::

    $ flask role update admin


list
^^^^

Show roles::

    $ flask role list


drop
^^^^

Drop roles::

    $ flask role drop


Permission command
------------------

.. code-block::

    Usage: flask permission [OPTIONS] COMMAND [ARGS]...

        Role permission manager.

    Options:
        --help  Show this message and exit.

    Commands:
        drop    Drop permissions.
        list    Show permissions.
        new     Create permission.
        remove  Remove permission.
        update  Update permission.

new
^^^

Create new role permission::

    $ flask permission new can_post -d "Post permission"


remove
^^^^^^

Delete permission::

    $ flask permission remove can_post


update
^^^^^^

Update permission::

    $ flask permission update can_post


list
^^^^

Show permissions::

    $ flask permission list


drop
^^^^

Drop permissions::

    $ flask permission drop
