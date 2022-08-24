from flask import Flask, request
from flask_negotiate import consumes

from markov import generate

app =  Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
@consumes('text/plain')
def index():
    r = request.get_data().decode('utf-8')
    return generate(r), 200 , {'Content-Type': 'text/plain; charset=utf-8'}
