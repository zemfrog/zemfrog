from flask import Flask, send_from_directory


def loader(app: Flask):
    """
    This function is to create multiple static files based on the ``STATICFILES`` configuration.
    """

    staticfiles = app.config.get("STATICFILES", [])
    for static in staticfiles:
        path, endpoint, static_folder = static
        static_host = None
        if len(static) == 4:
            static_host = static[-1]

        def serve_static(filename):
            cache_timeout = app.get_send_file_max_age(filename)
            return send_from_directory(
                static_folder, filename, cache_timeout=cache_timeout
            )

        app.add_url_rule(
            path.rstrip("/") + "/<path:filename>",
            endpoint=endpoint,
            host=static_host,
            view_func=serve_static,
        )
