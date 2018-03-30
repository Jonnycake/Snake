from Renderable import CursesRenderable
import time

class CursesMovable(CursesRenderable):
	# The game object
	game = None

	# The direction it's moving in
	direction = None

	# The previous direction (for followers)
	old_direction = None

	# If it's following anything
	following = None

	# The previous position
	old_position = None

	# Follow another part
	def follow(self, target):
		# We just set following to target
		self.following = target

		# We need to set the coordinates based on direction
		# NOTE: Coordinates in ncurses are based on the upper left hand corner
		#       as the origin (0, 0), down increases y, right increases x
		# Up: new.x = adjacent.x; new.y = adjacent.y + 1
		if target.direction == "u":
			self.x = target.x
			self.y = target.y + 1

		# Down: new.x = adjacent.x; new.y = adjacent.y - 1
		elif target.direction == "d":
			self.x = target.x
			self.y = target.y -1

		# Left: new.x = adjacent.x - 1; new.y = adjacent.y
		elif target.direction == "l":
			self.x = target.x + 1
			self.y = target.y

		# Right: new.x = adjacent.x + 1; new.y = adjacent.y
		elif target.direction == "r":
			self.x = target.x - 1
			self.y = target.y

		# Otherwise it's busted
		else:
			raise ValueError("An invalid direction ('%s') was found!" % (target.direction))

		# Finally set our direction to that of the target
		self.direction = target.direction

	# Move this part
	def move(self):
		# Set the old position
		self.old_position = (self.x, self.y)

		# Move in the appropriate direction
		# @note Using modulo division to provide wrapping
		# @todo Don't access private variables
		# Up: y -= 1
		if self.direction == "u":
			self.y = (self.y - 1) % self.game.screen._MAX_Y

		# Down: y += 1
		elif self.direction == "d":
			self.y = (self.y + 1) % self.game.screen._MAX_Y

		# Left: x -= 1
		elif self.direction == "l":
			self.x = (self.x - 1) % self.game.screen._MAX_X

		# Right: x += 1
		elif self.direction == "r":
			self.x = (self.x + 1) % self.game.screen._MAX_X

		# Set the old direction
		self.old_direction = self.direction

	def check_collision(self):
		for renderable in self.collision_list:
			if renderable.touching(self):
				renderable.collide()

	def turn(self, direction):
		self.old_direction = self.direction
		self.direction = direction
