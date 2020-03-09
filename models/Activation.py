import peewee
import datetime
from models.BaseModel import BaseModel
from models import User


class Activation(BaseModel):
    user = peewee.CharField(unique=True, index=True, max_length=36)
    seed = peewee.CharField(max_length=256)

    class Meta:
        table_name = 'activations'
