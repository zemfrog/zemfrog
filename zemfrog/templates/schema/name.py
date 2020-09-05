from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from ${src_model} import ${name}

class ${name}Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = ${name}
