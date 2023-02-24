# Standard Library
import json


def _read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data


def _read_json(path):
    return json.loads(_read_file(path))


def _write_json(path, data):
    return _write_file(path, json.dumps(data))


def _write_file(path, data):
    file = open(path, "w")
    file.write(str(data))
    file.close()


def read_scanning_state(path):
    return _read_json(path)["scanning_state"]


def write_scanning_state(path, scanning_state):
    json_data = _read_json(path)
    json_data["scanning_state"] = scanning_state
    _write_json(path, json_data)


def read_unprovisioned(path):
    return _read_json(path)["unprovisend_devices"]


def write_unprovisioned(path, unprovisioned):
    json_data = _read_json(path)
    json_data["unprovisioned"] = unprovisioned
    _write_json(path, json_data)


def write_prov(path, state, device):
    json_data = _read_json(path)
    json_data["prov_state"] = state
    json_data["prov_uuid"] = device
    _write_json(path, json_data)


def read_prov_state(path):
    return _read_json(path)["prov_state"]


def read_prov_device(path):
    return _read_json(path)["prov_uuid"]
