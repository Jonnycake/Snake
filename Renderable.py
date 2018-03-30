from Coordinate import Coordinate

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
		game.screen.addObj(self)

	def renderable_added(self, renderable):
		self.collision_list.append(renderable)

	def added(self, uuid):
		self.uuid = uuid
		return uuid

	def collide(self):
		self.collision_callback(self)
