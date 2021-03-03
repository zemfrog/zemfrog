File Upload
===========

For now, uploading files with flask-apispec is a little tricky.
However, you can still upload files via swagger-ui.


All you need is to import ``FileField`` from ``extensions.apispec``. For example::

    from extensions.apispec import FileField
    from flask_apispec import use_kwargs

    @use_kwargs({"image": FileField()}, location="files")
    def view_function(**kwds):
        image = kwds.get("image")
        print("Image:", image)
