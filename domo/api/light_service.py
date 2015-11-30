from flask import Flask, jsonify
from domo.domo import *


service = Flask(__name__)


@service.route("/lights_service/api/v1.0/lights", methods=['GET'])
def get_lights():
    lights = has.get_actuators()
    json = {}
    for light in lights:
        json[light.name] = {'id': light.id, 'name': light.name,
                            'pos': light.position, 'state': light.state.name}
    resp = jsonify(json)
    resp.status_code = 200
    return resp


@service.route("/lights_service/api/v1.0/lights/<id>", methods=['GET'])
def get_light(id):
    light = has.get_actuator(id)
    resp = jsonify({light.name: {'id': light.id, 'name': light.name,
                                 'pos': light.position, 'state': light.state.name}})
    resp.status_code = 200
    return resp


@service.route("/lights_service/api/v1.0/lights/<id>", methods=['PUT'])
def update_light(id):
    pass


@service.route("/lights_service/api/v1.0/lights/", methods=['POST'])
def create_light():
    pass

has = HAS()
d = Driver()
l1 = Light(has, d, "p1", "l1")
l2 = Light(has, d, "p2", "l2")
l3 = Light(has, d, "p3", "l3")
has.add_actuator(l1)
has.add_actuator(l2)
has.add_actuator(l3)

l2.on()
if __name__ == "__main__":
    service.run(debug=True)
