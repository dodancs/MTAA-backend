from flask import jsonify
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
def ConvertImage(picture):
    # Try to parse Base64 data
    try:
        base64.b64decode(re.sub('^data:image/.+;base64,', '', picture))
    except:
        return None
    # Try to parse image
    try:
        image = Image.open(BytesIO(base64.b64decode(
            re.sub('^data:image/.+;base64,', '', picture))))
    except PIL.UnidentifiedImageError:
        return None

    if image.format not in Config['allowed_image_types']:
        return None

    buffer = BytesIO()
    image.thumbnail((256, 256))
    image.save(buffer, format="PNG")

    return bytes(
        "data:image/png;base64,", encoding='utf-8') + base64.b64encode(buffer.getvalue())
