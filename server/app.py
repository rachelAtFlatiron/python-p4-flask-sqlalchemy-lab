#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    q = Animal.query.filter_by(id=id).first()
    return f'''
        <ul>ID: {q.id}</ul>
        <ul>Name: {q.name}</ul>
        <ul>Species: {q.species}</ul>
        <ul>Zookeeper: {q.zookeeper.name}</ul>
        <ul>Enclosure: {q.enclosure.environment}</ul>
    '''

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    z = Zookeeper.query.filter_by(id=id).first()
    str = f'''
        <ul>ID: {z.id}</ul>
        <ul>Name: {z.name}</ul>
        <ul>Birthday: {z.birthday}</ul>
    '''
    for animal in z.animals:
        str += f'<ul>Animal: {animal.name}</ul>'
    return str

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    e = Enclosure.query.filter_by(id=id).first()
    str = f'''
        <ul>ID: {e.id}</ul>
        <ul>Environment: {e.environment}</ul>
        <ul>Open to Visitors: {e.open_to_visitors}</ul>
    '''
    for animal in e.animals:
        str += f'<ul>Animal: {animal.name}</ul>'

    return str


if __name__ == '__main__':
    app.run(port=5555, debug=True)
