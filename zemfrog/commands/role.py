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


@click.group("role")
def group():
    """
    Access role manager.
    """


@group.command()
@with_appcontext
@click.argument("name")
@click.option("-d", "--description", required=True, help="Role description.")
@click.option("-p", "--permissions", help="Role permissions.")
def new(name, description, permissions):
    """
    Create role.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    perm_model = import_attr(
        import_name
        + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
    )
    role = model.query.filter_by(name=name).first()
    if not role:
        role = model(name=name, description=description)
        if permissions:
            for perm_name in permissions.split(","):
                perm = perm_model.query.filter_by(name=perm_name).first()
                if perm:
                    success = role.add_perm(perm)
                    if success:
                        msg = "Successfully added %r permission" % perm_name
                    else:
                        msg = "%r permission already exists" % perm_name
                else:
                    msg = "%r permission does not exist" % perm_name

                print(msg)

        db_add(role)
        print("Successfully added %r role" % name)
    else:
        print("%r role already exists" % name)


@group.command()
@with_appcontext
@click.argument("name")
def remove(name):
    """
    Remove role.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    role = model.query.filter_by(name=name).first()
    if role:
        db_delete(role)
        print("Successfully deleted %r role" % name)
    else:
        print("%r role doesn't exist" % name)


@group.command()
@with_appcontext
@click.argument("name")
def update(name):
    """
    Update role.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    role = model.query.filter_by(name=name).first()
    if role:
        cols = {}
        new_name = input("Enter a new role name: ").strip()
        description = input("Enter a new role description: ").strip()
        permissions = input("Enter new permissions: ").strip()
        if not new_name:
            new_name = role.name
        cols["name"] = new_name

        if not description:
            description = role.description
        cols["description"] = description

        if permissions:
            perm_model = import_attr(
                import_name
                + current_app.config.get("PERMISSION_MODEL", "models.user.Permission")
            )
            for perm_name in permissions.split(","):
                perm = perm_model.query.filter_by(name=perm_name).first()
                if perm:
                    success = role.add_perm(perm)
                    if success:
                        msg = "Successfully added %r permission" % perm_name
                    else:
                        msg = "%r permission already exists" % perm_name
                else:
                    msg = "%r permission does not exist" % perm_name

                print(msg)

        db_update(role, **cols)
        print("Successfully updated the %r role to %r" % (name, new_name))
    else:
        print("%r role doesn't exist" % name)


@group.command()
@with_appcontext
def list():
    """
    Show roles.
    """

    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    roles = model.query.all()
    print("Total roles: %d" % len(roles))
    for role in roles:
        perms = [perm.name for perm in role.permissions]
        print("* %s - %s (%s)" % (role.name, role.description, ", ".join(perms)))


@group.command()
@with_appcontext
def drop():
    """
    Drop roles.
    """

    print("Dropping all roles... ", end="")
    import_name = get_import_name(current_app)
    model = import_attr(
        import_name + current_app.config.get("ROLE_MODEL", "models.user.Role")
    )
    model.query.delete()
    db_commit()
    print("(done)")


command = group
