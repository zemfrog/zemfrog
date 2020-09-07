from extensions.marshmallow import ma
from ${src_model} import ${name}

class ${name}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ${name}
        load_instance = True
