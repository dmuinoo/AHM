
import json
import uuid

from datetime import datetime, timezone
from flask import Flask, request
from flask_restful import Resource, Api, abort


app = Flask(__name__)
api = Api(app)


def generate_uuid():
    identifier = uuid.uuid4()
    return json.dumps(identifier, default=str)


def get_utc_now():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return json.dumps(now, default=str)

MEASUREMENTS =[ 
    {
    'id': '84c0300-4c7d-4cf3-b8d0-4743b4883d28',
    'sys': 120,
    'dis': 80,
    'pul': 70,
    'created': get_utc_now(),
    'user-id': 'c823600-8078-4cf3-b7d5-9090d4883a28'
},
    {
    'id': '84c0800-4c6d-4cf2-b8d0-5043b4883d28',
    'sys': 120,
    'dis': 80,
    'pul': 70,
    'created': get_utc_now(),
    'user-id': 'c823600-8078-4cf3-b7d5-9090d4883a28'
}
]


class Measurement(Resource):
    def get(self, id):
        for measurement in MEASUREMENTS:
            if id == measurement.get('id'):
                return measurement, 200
        abort(404, message=f'Measurement ID={id} was not found')

class MeasurementList(Resource):
    def get(self):
        return MEASUREMENTS, 200

    def post(self):
        data = json.loads(request.data)
        measurement = {
            'id': generate_uuid(),
            'sys': data.get('sys'),
            'dis': data.get('dis'),
            'pul': data.get('pul'),
            'created': get_utc_now(),
            'user_id': 'c823600-8078-4cf3-b7d5-9090d4883a28'
        }
        MEASUREMENTS.append(measurement)
        return measurement, 201


api.add_resource(Measurement, '/v1/measurements/<string:id>')
api.add_resource(MeasurementList, '/v1/measurements')

if __name__ == '__main__':
    app.run(debug=True)
