=====
Usage
=====

Untuk membuat project dengan ``zemfrog``::

    $ zemfrog create frog


Jalan dan coba jika ini bekerja!::

    $ cd frog
    $ flask run



Blueprints
^^^^^^^^^^

    $ flask blueprint new account

Sekarang anda dapat menambahkan blueprint ke aplikasi flask mu, bagaimana??
Masukin nama blueprint mu ke config ``BLUEPRINTS``, e.g.::

    BLUEPRINTS = ['account']

Dan, sekarang anda bisa melihat blueprint ``account`` telah terdaftar di aplikasi flask::

    $ flask routes


API
^^^

Di zemfrog anda dapat membuat base API nya saja atau dengan (CRUD).
Contoh, membuat base API (tanpa CRUD)::

    $ flask api new article

Cara diatas akan membuat module article.py di direktori ``api`` dan itu adalah sumberdaya API untuk article.

Sekarang, membuat API (CRUD) !

.. note::

    Anda tidak dapat membuat API (CRUD) jika anda tidak mempunyai model ORM untuk 
    API tersebut.

Mari membuat model ``Product``. Model ini nantinya, yang akan kita buat API (CRUD) nya.

Rubah, file ``models/__init__.py`` menjadi seperti ini::

    from extensions.sqlalchemy import db
    from sqlalchemy import Column, String, Integer

    class Product(db.Model):
        id = Column(Integer, primary_key=True)
        name = Column(String)

Sekarang, kita membuatkan API (CRUD) untuk model ``Product``.

.. warning::

    Perlu dicatat, anda harus membuat API dengan nama yang sama dengan model ORM anda.
    Dan jangan lupa tambahkan opsi ``--crud``.

Contoh::

    $ flask api new Product --crud

API ini tidak akan bekerja jika anda belum menambahkan nya pada config ``APIS``.
Mari kita tambahkan ke config::

    APIS = ['api.product.ProductResource']
