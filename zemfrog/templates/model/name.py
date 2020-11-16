from {{ "" if main_app else ".." }}extensions.sqlalchemy import db
from sqlalchemy import Column, Integer

class {{model_name}}(db.Model):
    id = Column(Integer, primary_key=True)
