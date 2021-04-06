from flask import Flask


class Scaffold(Flask):
    # a place to store all the existing ORM models in the project.
    models = {}
