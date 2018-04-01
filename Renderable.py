from Coordinate import Coordinate
import random

# CursesRenderable class
class CursesRenderable(Coordinate):
	uuid = None
	character = "&"
	collision_list = []
	collision_callback = None
	game = None

	# @todo Implement position options
	def __init__(self, position = "random", game = None, collision_callback = collision_callback, collision_list = []):
		self.game = game

		# If position is a string
		if isinstance(position, str):
			# Generate a random position based on min and max with screen
			self.x = random.randint(0, game.screen._MAX_X - 1)
			self.y = random.randint(0, game.screen._MAX_Y - 1)
		# Otherwise just assume it's a tuple
		# @note Tsk tsk, trust, but verify
		else:
			self.x = position[0]
			self.y = position[1]

		# If we're touching anything in the collision_list, regenerate coordinates
		while self.touching(self.collision_list):
			self.x = random.randint(0, game.screen._MAX_X - 1)
			self.y = random.randint(0, game.screen._MAX_Y - 1)

		# Set the collision callback
		self.collision_callback = collision_callback

		# Add us to the screen
		game.screen.addObj(self, move = False)

	def renderable_added(self, renderable):
		self.collision_list.append(renderable)

	def added(self, uuid):
		self.uuid = uuid
		return uuid

	def collide(self):
		pass
		#self.collision_callback(self)

	def debug(self):
		collision_info = []
		for collidable in self.collision_list:
			collision_info.append(str(collidable))
		output = "%s: %s - %s" % (self.__class__, self.uuid, ",".join(collision_info))
		return output

	def __str__(self):
		x = -1
		y = -1
		if self.x is not None:
			x = self.x
		if self.y is not None:
			y = self.y

		return "%s(%d, %d)" % (self.uuid, x, y)
