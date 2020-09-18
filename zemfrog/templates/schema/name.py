from extensions.marshmallow import ma
from {{src_model}} import {{ model_list|join(', ') }}

{% for name in model_list %}
class {{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}
{% endfor %}