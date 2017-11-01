#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS_211 Week 11, Assignment 1, Web Dev Flask"""

from flask import Flask, render_template
from flask import request, redirect, flash
import glob, re, pickle

class SaveList(object):
    def __init__(self, filename=None):
        self.filename = filename

    def save(self, item_list):
        with open(self.filename, "wb") as save_list:
            pickle.dump(item_list, save_list)
            print 'List saved'

    def load(self):
        with open(self.filename, "rb") as item_list:
            state = pickle.load(item_list)
            print 'List loaded'
            return state

app = Flask(__name__)
app.secret_key = 'secret'

TO_DO = []

filename = 'save_list.txt'
save_list = SaveList(filename)

if glob.glob(filename):
    TO_DO = save_list.load()

@app.route('/')
def home():
    return render_template('index.html', to_do=TO_DO)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    row_id = len(TO_DO)

    email_pattern = re.compile(r'[a-zA-Z0-9.!*&$#_%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')

    if email_pattern.match(email):
        TO_DO.append((task, email, priority, row_id))
        save_list.save(TO_DO)
    else:
        flash('Invalid email address')
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    TO_DO[:] = []
    save_list.save(TO_DO)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form.get('row_id', type=int)
    for row in TO_DO:
        if row[3] == id:
            TO_DO.remove(row)
    save_list.save(TO_DO)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
