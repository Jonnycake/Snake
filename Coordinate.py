# Coordinate abstract class
class Coordinate(object):
	# x coordinate
	x = None

	# y coordinate
	y = None

	# z coordinate - doesn't apply currently
	z = None

	# Base class will not implement __init__(), exending classes should
	def __init__(self):
		raise NotImplementedError("Classes extending Coordinate MUST implement a constructor")

	# Check if there's any object at the same (x, y, z) as us
	def touching(self, collision_list):
		# coordinate_list is an array of Coordinates
		for coordinate in collision_list:
			# If our coordinates are the same, we are touching
			if coordinate.x == self.x and coordinate.y == self.y and coordinate.z == self.z:
				# Return the object we're touching
				return coordinate

		# Otherwise return false
		return False
