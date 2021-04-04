Authentication
==============

As of version >= 4.0.5, zemfrog splits blueprint ``auth`` to extensions. And currently it only supports JWT authentication.


JWT
---

This feature is inspired by the `FastAPI framework <https://github.com/tiangolo/fastapi>`_ and adopted from the project https://github.com/tiangolo/full-stack-flask-couchdb.

All REST APIs are protected with JWT authentication by default. However, if you wish to disable it, you only need to commenting ``authenticate`` decorators.

You can now install JWT authentication via this extension https://github.com/zemfrog/zemfrog-auth
