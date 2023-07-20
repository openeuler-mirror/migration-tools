# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
import sys

from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def MT_index():
    """
    跳转起始界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/MT_agreement', methods=['GET', 'POST'])
def MT_agreement():
    """
    跳转协议许可界面
    :return:
    """
    return render_template('MT_agreement.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9999')
