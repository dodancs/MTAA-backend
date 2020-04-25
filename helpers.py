from flask import jsonify, escape
import hashlib
import json
import base64
import binascii
import re
import PIL
from PIL import Image
from io import BytesIO

# Open configuration file
with open('config.json', encoding='utf8') as config_file:
    Config = json.load(config_file)

# Open responses definitions file
with open('responses.json', encoding='utf8') as responses_file:
    Responses = json.load(responses_file)


# Responses formatter
def Response(tag):
    if tag == "empty":
        return "", 200
    return jsonify(Responses[tag][0]), Responses[tag][1]


# Make hash from password and salt
def MakeHash(password, salt):
    return salt.hex() + hashlib.pbkdf2_hmac(Config['hash_algo'], password.encode('utf-8'), salt, Config['hash_iterations'], dklen=Config['hash_length']).hex()


# Convert image
def ConvertImage(bytes, width, height):
    # Try to parse image
    try:
        image = Image.open(BytesIO(bytes))
    except PIL.UnidentifiedImageError:
        return None
    except:
        return None

    if image.format not in Config['image_allowed_format']:
        return None

    buffer = BytesIO()
    image.thumbnail((width, height), Image.ANTIALIAS)
    image.save(buffer, format=Config['image_store_format'])

    return buffer


# Sanitize user input
def Sanitize(string, strip=True):
    return str(escape(string)).strip() if strip else str(escape(string))
