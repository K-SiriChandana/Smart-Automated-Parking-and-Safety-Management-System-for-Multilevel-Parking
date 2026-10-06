from config import (
    SERVO_OPEN_ANGLE,
    SERVO_CLOSED_ANGLE
)


class Gate:

    def __init__(self):

        self.is_open = False

        self.angle = SERVO_CLOSED_ANGLE

    def open(self):

        self.is_open = True

        self.angle = SERVO_OPEN_ANGLE

    def close(self):

        self.is_open = False

        self.angle = SERVO_CLOSED_ANGLE

    def get_angle(self):

        return self.angle