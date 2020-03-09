import peewee
import json

# Open configuration file
with open('config.json', encoding='utf8') as config_file:
    Config = json.load(config_file)

db = peewee.MySQLDatabase(
    Config['db_db'], host=Config['db_host'], port=Config['db_port'], user=Config['db_user'], passwd=Config['db_password'], charset='utf8mb4')


class BaseModel(peewee.Model):
    class Meta:
        database = db
