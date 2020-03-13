import peewee
import datetime
from models.BaseModel import BaseModel


class User(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    uuid = peewee.CharField(unique=True, index=True, max_length=36)
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField(max_length=1024)
    firstname = peewee.CharField(max_length=256)
    lastname = peewee.CharField(max_length=256)
    activated = peewee.BooleanField(default=False)
    admin = peewee.BooleanField(default=False)
    donations = peewee.DoubleField(default=0)
    picture = peewee.CharField(max_length=36)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        table_name = 'users'
