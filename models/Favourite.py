import peewee
import datetime
from models.BaseModel import BaseModel


class Favourite(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    user = peewee.CharField(index=True, max_length=36)
    cat = peewee.CharField(max_length=36)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'favourites'
