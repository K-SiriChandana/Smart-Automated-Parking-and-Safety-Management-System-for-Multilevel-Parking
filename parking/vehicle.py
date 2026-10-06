class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.slot = None


class VehicleManager:

    def __init__(self):
        self.counter = 0
        self.vehicles = {}

    def create_vehicle(self):

        self.counter += 1

        vehicle_id = f"VEH-{self.counter:03d}"

        vehicle = Vehicle(vehicle_id)

        self.vehicles[vehicle_id] = vehicle

        return vehicle