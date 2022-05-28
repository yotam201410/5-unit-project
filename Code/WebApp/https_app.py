import flask
from flask import render_template, redirect, url_for

app = flask.Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    return redirect("http://127.0.0.1")

def main():
    app.run(host="127.0.0.1", ssl_context=("server.crt", "server.key"), port=443)
