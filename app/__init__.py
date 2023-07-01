from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5c801ae29bc79f4a63d042a31149c40' # Generated using secrets.token_hex(num)

from app import routes