=======
History
=======

1.0.0 (2020-09-03)
------------------

* First release on PyPI.

1.0.1 (2020-09-07)
------------------

* Automation create (CRUD) API
* Update template API
* Update zemfrog release information.

1.0.2 (2020-09-08)
------------------

* Update API structure

1.0.3 (2020-09-08)
------------------

* re-upload

1.0.4 (2020-09-09)
------------------

* fix manifest file

1.0.5 (2020-09-10)
------------------

* add command boilerplate
* add schema command

1.0.6 (2020-09-15)
------------------

* add jwt authentication
* refactor blueprint boilerplate
* add send async email
* fix celery

1.0.7 (2020-09-19)
------------------

* Fix: `#8 <https://github.com/zemfrog/zemfrog/issues/8>`_
* flask-apispec integration.
* improve authentication.
* add default schema models.
* Fix: rest api boilerplate
* IMPROVE: Added a prompt if a schema model exists.
* IMPROVE: add zemfrgo to requirements
* DOC: add README to project boilerplate

1.0.8 (2020-10-03)
------------------

* Fix: `#12 <https://github.com/zemfrog/zemfrog/issues/12>`_, `#13 <https://github.com/zemfrog/zemfrog/issues/13>`_, `#14 <https://github.com/zemfrog/zemfrog/issues/14>`_
* IMPROVE: import the orm model in the schema generator.
* General Update:  update development status

1.0.9 (2020-10-05)
------------------

* Fix: `#16 <https://github.com/zemfrog/zemfrog/issues/16>`_, `#14 <https://github.com/zemfrog/zemfrog/issues/14>`_, `#17 <https://github.com/zemfrog/zemfrog/issues/17>`_
* NEW: add version option

1.2.0 (2020-10-19)
------------------

* NEW: add load urls
* NEW: add load middlewares
* NEW: middleware boilerplate.
* NEW: multiple apps support
* Fix minor bugs

1.2.1 (2020-10-27)
------------------

* New Feature: added prompt to manage the app.
* moved mail dir to templates/emails
* add ``api_doc`` & ``authenticate`` decorator.
* NEW: add swagger oauth2.
* NEW: add first_name & last_name column.
* IMPROVE: Support creating REST API descriptions via function documents.
* Refactor Code: Rename and add field validation.
* Code Change: update REST API structure.

1.2.2 (2020-10-28)
------------------

* Refactor generator
* New Feature: add error handler


1.2.3 (2020-11-13)
------------------

* Adding: current_db local proxy
* rename services directory to tasks


1.2.4 (2020-11-14)
------------------

* support multiple static files
* Add an endpoint to validate the password reset token
* fix `#37 <https://github.com/zemfrog/zemfrog/issues/37>`_


1.2.5 (2020-11-18)
------------------

* NEW: add extension, model, task generator
* Refactor Code: add model mixin
* add command user, role & permission
* FIX: auth logs
* New Feature: supports role-based access control


1.2.6 (2020-11-21)
------------------

* IMPROVE: commands to manage nested applications
* Added endpoint for checking token jwt
* Add an endpoint to retrieve one data from the model
* Add schema to limit results
* Added a handler for handling API errors


1.2.7 (2020-11-24)
------------------

* FIX: user checks in the test token endpoint
* NEW: support for creating your own app loader
* FIX: Make user roles optional
* FIX: `#49 <https://github.com/zemfrog/zemfrog/issues/49>`_

2.0.1 (2020-12-20)
------------------

* Refactoring app loaders
* IMPROVE: REST API, models & validators
* IMPROVE: added template checks
* IMPROVE: add password validator
* IMPROVE: Compatible with frontend nuxtjs
* NEW: add flask-cors extension

2.0.2 (2020-12-20)
------------------

* fix: missing flask-cors dependency

2.0.3 (2020-12-20)
------------------

* IMPROVE: clean up dependencies

3.0.1 (2020-12-20)
------------------

* add command secretkey
* Fix: varchar length
* Added db migration based on environment
* Stable release

4.0.1 (2021-03-04)
------------------

* IMPROVE: Move extensions to global
* NEW: add pre-commit tool
* IMPROVE: refactor json response
* Refactor Code: run pre-commit
* IMPROVE: Change 'SystemExit' to 'ValidationError'
* IMPROVE: Rename the api directory to apis
* NEW: add autoflake hook
* Changed the stable version status to BETA

4.0.2 (2021-03-05)
------------------

* FIX: response message in jwt & error handler boilerplate
* FIX: update zemfrog version in requirements.txt
