from __future__ import annotations

from toga import LatLng

from ..utils import LoggedObject


class Geolocation(LoggedObject):
    def __init__(self, interface):
        self.interface = interface

        # -2: background permission *could* be granted, but hasn't been
        # -1: permission *could* be granted, but hasn't been
        # 0: permission has been denied, or can't be granted
        # 1: permission has been granted
        # 2: background permission has been granted
        self._has_permission = -1
        self._location = LatLng(10.0, 20.0)
        self._altitude = 0

    def _next_location(self):
        self._action("get next location")
        self._location = LatLng(self._location.lat + 3, self._location.lng + 5)
        self._altitude = (self._altitude + 3) % 10

        return self._location, self._altitude

    def has_permission(self):
        self._action("has permission")
        return self._has_permission > 0

    def has_background_permission(self):
        self._action("has background permission")
        return self._has_permission > 1

    def request_permission(self, future):
        self._action("request permission")
        self._has_permission = abs(self._has_permission)
        future.set_result(self._has_permission > 0)

    def request_background_permission(self, future):
        self._action("request background permission")
        self._has_permission = abs(self._has_permission)
        future.set_result(self._has_permission > 1)

    def current_location(self, result):
        if self.has_permission():
            location, altitude = self._next_location()
            result.set_result(location)
            self.interface.on_change(location=location, altitude=altitude)
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def start(self):
        if self.has_permission():
            self._action("start geolocation updates")
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def stop(self):
        if self.has_permission():
            self._action("stop geolocation updates")
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def simulate_update(self):
        location, altitude = self._next_location()
        self.interface.on_change(location=location, altitude=altitude)
