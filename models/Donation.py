import peewee
import datetime
from models.BaseModel import BaseModel


class Donation(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    donator = peewee.CharField(index=True, max_length=36, null=True)
    amount = peewee.DoubleField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'donations'
