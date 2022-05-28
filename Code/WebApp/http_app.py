import flask
from flask import redirect, render_template, url_for

app = flask.Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    return "<h1>you cant access this page</h1>"

def main():
    app.run(host="127.0.0.1",port=80)
