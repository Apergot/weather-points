from flask import Flask, jsonify, request
from src.database import Session
from src.model import Point

app = Flask(__name__)


@app.route('/api/points', methods=['POST'])
def create_point():
    # TODO: validate json content (probably not needed)
    data = request.get_json()
    new_point = Point(data['name'], data['country'], data['region'], data['lat'], data['lon'])
    session = Session()
    session.add(new_point)
    session.commit()
    return jsonify(new_point.serialize()), 201


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
