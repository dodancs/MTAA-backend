import peewee
from models.BaseModel import BaseModel


class Breed(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    name = peewee.CharField(unique=True, max_length=256)

    class Meta:
        table_name = 'breeds'
