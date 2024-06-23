import random, requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

SECRET_API_KEY = os.getenv('SECRET_API_KEY')


# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/all')
def all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()

    cafe_list = [
        {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price,
        }
        for cafe in cafes
    ]

    return jsonify(json_list=cafe_list)


@app.route('/random')
def get_random_cafe():
    cafes = Cafe.query.all()
    cafe = random.choice(cafes)
    random_cafe = {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price,
        }

    return jsonify(random_cafe)


@app.route('/search')
def search_cafe():
    location = request.args.get('loc')
    condition = Cafe.location.like(f"%{location}%")
    cafes = db.session.execute(db.select(Cafe).where(condition)).scalars().all()
    selected_cafe = [
        {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price,
        }

         for cafe in cafes
    ]
    if selected_cafe:
        return jsonify(selected_cafe)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})


# HTTP POST - Create Record
@app.route('/add', methods=["POST"])
def add():
    add_cafe = Cafe(
        name=request.form['name'],
        map_url=request.form['map_url'],
        img_url=request.form['img_url'],
        location=request.form['location'],
        seats=request.form['seats'],
        has_toilet=bool(request.form['has_toilet']),
        has_wifi=bool(request.form['has_wifi']),
        has_sockets=bool(request.form['has_sockets']),
        can_take_calls=bool(request.form['can_take_calls']),
        coffee_price=request.form['coffee_price'],
    )
    db.session.add(add_cafe)
    db.session.commit()
    result = {
        "response": {
            "success": "Successfully added the new cafe"
        }
    }

    return jsonify(response={"success": "Successfully added the new cafe"})


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    update_cafe = db.get_or_404(Cafe, cafe_id)

    if update_cafe:
        update_price.price = request.args.get('coffee_price')
        db.session.commit()

        return jsonify(response={"success": "Coffee price updated successfully"}), 200
    else:
        return jsonify(error={"Not Found": "Cafe not found"}), 404


# HTTP DELETE - Delete Record
@app.route('/delete/<int:cafe_id>', methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == '2345asdf4@#rf4rcdsf':
        delete_cafe = db.get_or_404(Cafe, cafe_id)

        if delete_cafe:
            db.session.delete(delete_cafe)
            db.session.commit()

            return jsonify(response={"Success": "Cafe deleted successfully"}), 200
        else:
            return jsonify(error={"Not Found": "Cafe not found"}), 404

    else:
        return jsonify(error={"Not Allowed": "Wrong API Key"}), 403


if __name__ == '__main__':
    app.run(debug=True)
