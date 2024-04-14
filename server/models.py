# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)

# class Bakery(db.Model, SerializerMixin):
#     __tablename__ = 'bakeries'

#     serialize_rules = ('-baked_goods.bakery',)

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     baked_goods = db.relationship('BakedGood', backref='bakery')

#     def __repr__(self):
#         return f'<Bakery {self.name}>'

# class BakedGood(db.Model, SerializerMixin):
#     __tablename__ = 'baked_goods'

#     serialize_rules = ('-bakery.baked_goods',)

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     price = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

#     def __repr__(self):
#         return f'<Baked Good {self.name}, ${self.price}>'

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy and Metadata with custom naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})
db = SQLAlchemy(app, metadata=metadata)

# Define Bakery model with SerializerMixin for JSON serialization
class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define relationship with BakedGood model
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)

    # Custom method to convert model instance to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'baked_goods': [good.to_dict() for good in self.baked_goods]
        }

# Define BakedGood model with SerializerMixin for JSON serialization
class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define foreign key relationship with Bakery model
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'), nullable=False)

    # Custom method to convert model instance to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'bakery_id': self.bakery_id
        }

# Define routes to interact with the bakery and baked goods data
@app.route('/')
def index():
    return '<h1>Welcome to the Bakery API!</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries]), 200

@app.route('/bakeries/<int:bakery_id>')
def get_bakery(bakery_id):
    bakery = Bakery.query.get_or_404(bakery_id)
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods')
def get_baked_goods():
    baked_goods = BakedGood.query.all()
    return jsonify([good.to_dict() for good in baked_goods]), 200

@app.route('/baked_goods/<int:good_id>')
def get_baked_good(good_id):
    good = BakedGood.query.get_or_404(good_id)
    return jsonify(good.to_dict()), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
