from flask_apispec import FlaskApiSpec

docs = FlaskApiSpec(document_options=False)
init_app = docs.init_app
