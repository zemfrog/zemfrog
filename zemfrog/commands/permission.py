import click
from flask import current_app
from flask.cli import with_appcontext

from ..helper import (
    db_commit,
    import_attr,
    get_import_name,
    db_add,
    db_delete,
    db_update,
)


@click.group("permission")
def group():
    """
    Role permission manager.
    """


@group.command()
@with_appcontext
@click.argument("name")
@click.option("-d", "--description", required=True, help="Permission description.")
def new(name, description):
    """
    Create permission.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    perm = model.query.filter_by(name=name).first()
    if not perm:
        perm = model(name=name, description=description)
        db_add(perm)
        print("Successfully added %r permission" % name)
    else:
        print("%r permission already exists" % name)


@group.command()
@with_appcontext
@click.argument("name")
def remove(name):
    """
    Remove permission.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    perm = model.query.filter_by(name=name).first()
    if perm:
        db_delete(perm)
        print("Successfully deleted %r permission" % name)
    else:
        print("%r permission doesn't exist" % name)


@group.command()
@with_appcontext
@click.argument("name")
def update(name):
    """
    Update permission.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    perm = model.query.filter_by(name=name).first()
    if perm:
        new_name = input("Enter a new permission name: ").strip()
        description = input("Enter a new permission description: ").strip()
        if new_name and description:
            db_update(perm, name=new_name, description=description)
            print("Successfully updated the %r permission to %r" % (name, new_name))
        else:
            print("Please enter the name and description of the permission correctly!")
    else:
        print("%r permission doesn't exist" % name)


@group.command()
@with_appcontext
def list():
    """
    Show permissions.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    perms = model.query.all()
    print("Total permissions: %d" % len(perms))
    for perm in perms:
        print("* %s - %s" % (perm.name, perm.description))


@group.command()
@with_appcontext
def drop():
    """
    Drop permissions.
    """

    print("Dropping all permissions... ", end="")
    import_name = get_import_name(current_app)
    model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    model.query.delete()
    db_commit()
    print("(done)")


command = group
