import peewee
import datetime
from models.BaseModel import BaseModel


class Cat(BaseModel):
    id = peewee.BigAutoField(unique=True, index=True, primary_key=True)
    uuid = peewee.CharField(unique=True, index=True, max_length=36)
    name = peewee.CharField(max_length=256)
    age = peewee.SmallIntegerField()
    sex = peewee.BooleanField()
    breed = peewee.BigIntegerField()
    health_status = peewee.BigIntegerField()
    castrated = peewee.BooleanField()
    vaccinated = peewee.BooleanField()
    dewormed = peewee.BooleanField()
    colour = peewee.BigIntegerField()
    description = peewee.TextField()
    health_log = peewee.TextField()
    adoptive = peewee.BooleanField()
    adopted_by = peewee.CharField(unique=True, index=True, max_length=36, null=True)
    pictures = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Cat, self).save(*args, **kwargs)

    class Meta:
        table_name = 'cats'
