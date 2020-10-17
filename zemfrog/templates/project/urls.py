{% if main_app -%}
    import views
{% else -%}
    from . import views
{% endif %}

docs = {"tags": ["root"]}
routes = [("/", views.index, ["GET"])]
