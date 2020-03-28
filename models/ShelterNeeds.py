import peewee
import datetime
from models.BaseModel import BaseModel


class ShelterNeeds(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    uuid = peewee.CharField(unique=True, index=True, max_length=36)
    category = peewee.CharField(max_length=256)
    name = peewee.CharField(max_length=256)
    details = peewee.TextField()
    hide = peewee.BooleanField()

    class Meta:
        table_name = 'shelter_needs'
