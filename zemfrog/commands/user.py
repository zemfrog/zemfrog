import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from datetime import datetime

from ..helper import (
    db_commit,
    import_attr,
    get_import_name,
    db_add,
    db_delete,
    db_update,
)
from ..validators import validate_email, validate_username


@click.group("user")
def group():
    """
    User manager.
    """


@group.command()
@with_appcontext
@click.argument("email")
@click.option("-f", "--first-name", required=True, help="First name.", prompt=True)
@click.option("-l", "--last-name", required=True, help="Last name.", prompt=True)
@click.option("-p", "--password", required=True, help="Password.", prompt=True)
@click.option(
    "-r",
    "--roles",
    help="User roles (separated by ,).",
    prompt="User roles (separated by ,)",
)
def new(email, first_name, last_name, password, roles):
    """
    Create user.
    """

    validate_email(email)
    validate_username(first_name)
    validate_username(last_name)
    import_name = get_import_name(current_app)
    role_model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    roles = (roles or "").strip()
    user_roles = []
    for role in roles.split(","):
        role = role_model.query.filter_by(name=role.strip()).first()
        if role:
            user_roles.append(role)

    model = import_attr(
        import_name + current_app.config.get("USER_MODEL", "models.user.User")
    )
    user = model.query.filter_by(email=email).first()
    if not user:
        username = first_name + " " + last_name
        passw = generate_password_hash(password)
        user = model(
            first_name=first_name,
            last_name=last_name,
            name=username,
            email=email,
            password=passw,
            register_at=datetime.utcnow(),
            confirmed=True,
            confirmed_at=datetime.utcnow(),
            roles=user_roles,
        )
        db_add(user)
        print("Successfully added user %r" % email)
    else:
        print("Email %r already exists" % email)


@group.command()
@with_appcontext
@click.argument("email")
def remove(email):
    """
    Remove user.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("USER_MODEL", "models.user.User")
    )
    user = model.query.filter_by(email=email).first()
    if user:
        db_delete(user)
        print("Successfully deleted user %r" % email)
    else:
        print("User %r doesn't exist" % email)


@group.command()
@with_appcontext
@click.argument("email")
def update(email):
    """
    Update user.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("USER_MODEL", "models.user.User")
    )
    role_model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    user = model.query.filter_by(email=email).first()
    if user:
        cols = {}
        first_name = input("First name: ").strip()
        if not validate_username(first_name, silently=True):
            first_name = user.first_name
        cols["first_name"] = first_name

        last_name = input("Last name: ").strip()
        if not validate_username(last_name, silently=True):
            last_name = user.last_name
        cols["last_name"] = last_name

        new_email = input("New email: ").strip()
        if not validate_email(new_email, silently=True):
            new_email = user.email
        cols["email"] = new_email

        password = input("Password: ").strip()
        if password:
            password = generate_password_hash(password)
        else:
            password = user.password
        cols["password"] = password
        cols["name"] = cols["first_name"] + " " + cols["last_name"]
        roles = input("Enter a new user role (separated by ,): ")
        user_roles = []
        for role in roles.split(","):
            role = role_model.query.filter_by(name=role.strip()).first()
            if role:
                user_roles.append(role)

        if user_roles:
            cols["roles"] = user_roles

        db_update(user, **cols)
        print("User %r updated successfully" % email)

    else:
        print("User %r doesn't exist" % email)


@group.command()
@with_appcontext
def list():
    """
    Show users.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("USER_MODEL", "models.user.User")
    )
    users = model.query.all()
    print("Total users: %d" % len(users))
    for user in users:
        roles = []
        for role in user.roles:
            roles.append(role.name)

        print("* %s (%s) [%s]" % (user.name, user.email, ", ".join(roles)))


@group.command()
@with_appcontext
def drop():
    """
    Drop users.
    """

    print("Dropping all users... ", end="")
    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("USER_MODEL", "models.user.User")
    )
    model.query.delete()
    db_commit()
    print("(done)")


command = group
