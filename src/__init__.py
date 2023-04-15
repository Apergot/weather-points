from flask import Flask, jsonify, request
from src.database import Session
from src.model import Point
from src.services.weather_api_service import WeatherApiService

app = Flask(__name__)


@app.route('/api/points', methods=['POST'])
def create_point():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400

    session = Session()
    point = session.query(Point).filter(Point.name == data['name']).first()

    if point:
        return jsonify({'message': 'Point with given name already exists'}), 400

    res = WeatherApiService().search_interest_point(data['name'])

    if res:
        new_point = Point(res['name'], res['country'], res['region'], res['lat'], res['lon'])
        session = Session()
        session.add(new_point)
        session.commit()
        return jsonify(new_point.serialize()), 201

    return jsonify({'message': 'Could not create any point with given name'}), 400


@app.route('/api/points', methods=['GET'])
def get_points_collection():
    session = Session()
    points = session.query(Point).all()

    return jsonify([point.serialize() for point in points]), 200


@app.route('/api/points/<uuid>', methods=['GET'])
def get_point(uuid):
    session = Session()
    point = session.query(Point).filter(Point.uuid == uuid).first()

    if not point:
        return jsonify({'message': 'Point not found'}), 404

    return jsonify(point.serialize()), 200


@app.route('/api/points/<uuid>', methods=['PUT'])
def update_point(uuid):
    session = Session()
    point = session.query(Point).filter(Point.uuid == uuid).first()

    if not point:
        return jsonify({'message': 'Point not found'}), 404

    data = request.get_json()

    for field in ['name', 'country', 'region', 'lat', 'lon']:
        if field in data:
            setattr(point, field, data[field])

    session.commit()

    return jsonify(point.serialize()), 200


@app.route('/api/points/<uuid>', methods=['DELETE'])
def delete_point(uuid):
    session = Session()
    point = session.query(Point).filter(Point.uuid == uuid).first()

    if not point:
        return jsonify({'message': 'Point not found'}), 404

    session.delete(point)
    session.commit()

    return '', 204
