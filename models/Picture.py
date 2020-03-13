import peewee
import datetime
from models.BaseModel import BaseModel


class Picture(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    uuid = peewee.CharField(unique=True, index=True, max_length=36)
    owner = peewee.CharField(max_length=36)

    class Meta:
        table_name = 'pictures'
