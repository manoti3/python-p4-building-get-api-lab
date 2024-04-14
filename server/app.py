#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_data = [bakery.to_dict() for bakery in bakeries]

    return jsonify(bakeries_data), 200


@app.route('/bakeries/<int:bakery_id>')
def get_bakery_by_id(bakery_id):
    bakery = db.session.get(Bakery, bakery_id)

    if bakery:
        bakery_data = bakery.to_dict()
        return jsonify(bakery_data), 200

    return jsonify({'error': 'Bakery not found'}), 404


@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_data = [good.to_dict() for good in baked_goods]

    return jsonify(baked_goods_data), 200


@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive:
        most_expensive_data = most_expensive.to_dict()
        return jsonify(most_expensive_data), 200

    return jsonify({'error': 'No baked goods found'}), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)