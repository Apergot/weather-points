from flask import Flask, jsonify, request
from src.database import Session
from src.model import Point
from src.services.weather_api_service import WeatherApiService
import uuid

app = Flask(__name__)


@app.route('/api/points', methods=['POST'])
def create_point():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400

    res = WeatherApiService().search_interest_point(data['name'])

    if res:
        session = Session()
        point = session.query(Point).filter(Point.name == res['name']).first()

        if point:
            return jsonify({'message': 'Point with given name already exists'}), 400

        new_point = Point(res['name'], res['country'], res['region'], res['lat'], res['lon'])
        session.add(new_point)
        session.commit()

        return jsonify(new_point.serialize()), 201

    return jsonify({'message': 'Could not create any point with given data'}), 400


@app.route('/api/points', methods=['GET'])
def get_points_collection():
    session = Session()
    points = session.query(Point).all()
    session.close()

    return jsonify([point.serialize() for point in points]), 200


@app.route('/api/points/forecasts', methods=['GET'])
def get_points_collection_forecasts():
    session = Session()
    points = session.query(Point).all()
    session.close()

    serialized_points = []

    for point in points:
        forecasts = WeatherApiService().get_current_and_next_day_forecasts(point.name)
        serialized_point = point.serialize()

        serialized_point['currentDay'] = {
            'avgtemp_c': forecasts[0]['day']['avgtemp_c'],
            'humidity': forecasts[0]['day']['avghumidity'],
            'totalprecip_mm': forecasts[0]['day']['totalprecip_mm']
        }

        serialized_point['nextDay'] = {
            'avgtemp_c': forecasts[1]['day']['avgtemp_c'],
            'humidity': forecasts[1]['day']['avghumidity'],
            'totalprecip_mm': forecasts[1]['day']['totalprecip_mm']
        }

        serialized_points.append(serialized_point)

    return jsonify(serialized_points), 200


@app.route('/api/points/<param_uuid>', methods=['DELETE'])
def delete_point(param_uuid):
    try:
        uuid.UUID(param_uuid, version=4)
    except ValueError:
        return jsonify({'message': 'Invalid uuid format provided'}), 400

    session = Session()
    point = session.query(Point).filter(Point.uuid == param_uuid).first()

    if not point:
        return jsonify({'message': 'Point not found'}), 404

    session.delete(point)
    session.commit()
    session.close()

    return '', 204
