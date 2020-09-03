from flask_marshmallow.sqla import SQLAlchemyAutoSchema
import models

class {{name}}Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.{{name}}
