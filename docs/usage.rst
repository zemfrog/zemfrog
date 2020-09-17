=====
Usage
=====

Membuat project dengan ``zemfrog``::

    $ zemfrog create frog


Dan sekarang jalankan::

    $ cd frog
    $ flask run


Blueprints
^^^^^^^^^^

Membuat blueprint boilerplate::

    $ flask blueprint new account

Struktur blueprint akan terlihat seperti ini::

    account
    ├── __init__.py
    ├── routes.py
    ├── urls.py
    └── views.py

+---------------+---------------------------------+
| Filename      | Description                     |
+===============+=================================+
| ``routes.py`` | objek blueprint kamu disini     |
+---------------+---------------------------------+
| ``urls.py``   | semua API enpoints kamu disini  |
+---------------+---------------------------------+
| ``views.py``  | semua fungsi view kamu disini   |
+---------------+---------------------------------+

Mari kita membuat 2 fungsi view::

    # account/views.py

    def login():
        return "login cuk"

    def logout():
        return "logout cuk"

Daftarkan fungsi view ke blueprint.

.. note::

    Format route akan terlihat seperti ini ``(url, view, methods)``.

.. code-block:: python

    # account/urls.py

    routes = [
        ('/login', views.login, ['POST']),
        ('/logout', views.logout, ['POST'])
    ]

Sekarang kamu dapat menambahkan blueprint ke aplikasi flask kamu, bagaimana??
Masukin nama blueprint kamu ke config ``BLUEPRINTS``, e.g.::

    BLUEPRINTS = ['account']

Dan, sekarang kamu bisa melihat blueprint ``account`` telah terdaftar di aplikasi flask::

    $ flask routes


API
^^^

Di zemfrog kamu dapat membuat base API nya saja atau dengan (CRUD).
Contoh, membuat base API (tanpa CRUD)::

    $ flask api new article

Cara diatas akan membuat module article.py di direktori ``api`` dan itu adalah sumberdaya API untuk article.

Sekarang, membuat API dengan (CRUD) !

.. note::

    Kamu tidak dapat membuat API (CRUD) jika kamu tidak mempunyai model ORM untuk 
    API tersebut.

Mari membuat model ``Product``. Model ini nantinya, yang akan kita buatkan API (CRUD) nya.

Rubah, file ``models/__init__.py`` menjadi seperti ini::

    from extensions.sqlalchemy import db
    from sqlalchemy import Column, String, Integer

    class Product(db.Model):
        id = Column(Integer, primary_key=True)
        name = Column(String)

Sekarang, kita membuatkan API (CRUD) untuk model ``Product``.

.. warning::

    Perlu dicatat, kamu harus membuat API dengan nama yang sama dengan model ORM kamu.
    Dan jangan lupa tambahkan opsi ``--crud``.

Contoh::

    $ flask api new Product --crud

API ini tidak akan bekerja jika kamu belum menambahkan nya pada config ``APIS``.
Mari kita tambahkan ke config::

    APIS = ['api.product']
