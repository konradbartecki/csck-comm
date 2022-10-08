import enum

class CelestialBodyType(str, enum.Enum):
    Star = 1,
    Planet = 2,
    Comet = 3,
    Asteroid = 4,
    Meteor = 5,
    Galaxy = 6
