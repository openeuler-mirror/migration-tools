# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
import sys

from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9999')
