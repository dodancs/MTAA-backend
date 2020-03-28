import peewee
import datetime
from models.BaseModel import BaseModel


class Comment(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    uuid = peewee.CharField(unique=True, index=True, max_length=36)
    author = peewee.CharField(index=True, max_length=36, null=True)
    cat = peewee.CharField(index=True, max_length=36, null=True)
    text = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'comments'
