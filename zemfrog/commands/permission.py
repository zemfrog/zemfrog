import click
from flask.cli import with_appcontext

from ..helper import db_add, db_commit, db_delete, db_update, get_object_model


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

    model = get_object_model("permission")
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

    model = get_object_model("permission")
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

    model = get_object_model("permission")
    perm = model.query.filter_by(name=name).first()
    if perm:
        cols = {}
        new_name = input("Enter a new permission name: ").strip()
        description = input("Enter a new permission description: ").strip()
        if not new_name:
            new_name = perm.name
        cols["name"] = new_name

        if not description:
            description = perm.description
        cols["description"] = description

        db_update(perm, **cols)
        print("Successfully updated the %r permission to %r" % (name, new_name))
    else:
        print("%r permission doesn't exist" % name)


@group.command()
@with_appcontext
def list():
    """
    Show permissions.
    """

    model = get_object_model("permission")
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
    model = get_object_model("permission")
    model.query.delete()
    db_commit()
    print("(done)")


command = group
