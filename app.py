# -*- encoding: utf-8 -*-
"""
@File : app.py
@Time : 2022/5/14 14:30
@Author : Linleil
"""
import os
import sys
import click
import random


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for, redirect, flash


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))


@app.route('/', methods=['GET', 'POST'])
def food_index():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name or len(name) > 60:
            flash('Wrong input.')
            return redirect(url_for('food_index'))
        food = Food(name=name)
        db.session.add(food)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('food_index'))
    foods = Food.query.all()
    return render_template('index.html', foods=foods)


@app.route('/choose')
def food_choose():
    results = Food.query.all()
    result = random.choice(results)
    flash(result.name)
    return redirect(url_for('food_index'))


@app.route('/backend')
def backend():
    foods = Food.query.all()
    return render_template('backend.html', foods=foods)


@app.route('/delete/<int:food_id>', methods=['POST'])
def delete(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('food_index'))


@app.route('/me')
def me():
    return render_template('me.html')


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')