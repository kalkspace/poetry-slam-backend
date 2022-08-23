from flask import Flask, request

from markov import generate

app =  Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    r = request.get_json()
    return generate(r), 200 , {'Content-Type': 'text/plain; charset=utf-8'}
