import json
import os


class Store:
    def __init__(
        self,
        location="apps/sit_ble_devices/static/store/store.json",
    ) -> None:
        self._location = location

        if self._location:
            if os.path.exists(self._location):
                with open(self._location, "r", encoding="utf8") as store_file:
                    self._data = json.load(store_file)
            else:
                self._data = {}

    def save(self):
        with open(self._location, "w", encoding="utf8") as f:
            json.dump(self._data, f)

    def delete(self, key):
        del self._data[key]

    def set_value(self, key, value):
        self._data[key] = value
        self.save()

    def get_value(self, key, fallback=None):
        if key not in self._data:
            self._data[key] = fallback
        return self._data.get(key)
