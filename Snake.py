from Movable import CursesMovable

class CursesSnakePart(CursesMovable):
	def __init__(self, game = None, is_head = False, head = None):
		collision_callback = None
		collision_list = []
		position = "random"
		self.direction = "r"
		if is_head:
			self.character = "@"
			position = [20, 20]
		elif head is None:
			raise ValueError("Can not pass a None head with a non-head piece...")
		else:
			self.character = "*"
			position = [19, 20]
			self.follow(head)

		CursesMovable.__init__(self, position = position, game = game, collision_callback = collision_callback, collision_list = collision_list)


	def move(self):
		CursesMovable.move(self)

		# NOTE: Now if we're following a part we are currently in the position
		#       it used to be at, meaning, that we must set our direction, to the
		#       old direction of it (to follow the same path).  This is really
		#       just to get around using ugly positional logic...
		if self.following is not None:
			self.direction = self.following.old_direction

# The snake...
class CursesSnake(CursesMovable):
	# Pieces of our snake
	pieces = []

	def __init__(self, game = None):
		self.game = game
		self.pieces.append(CursesSnakePart(game = game, is_head = True))
		self.pieces.append(CursesSnakePart(game = game, is_head = False, head = self.pieces[0]))

	# We need to move all of our pieces
	def move(self):
		for piece in self.pieces:
			piece.move()

	def turn(self, direction):
		CursesMovable.turn(self.pieces[0], direction)

	def added(self, uuid):
		for piece in self.pieces:
			# We tell the pieces to move, this way we can
			# ensure the order of movement
			self.game.screen.addObj(piece, False)
		CursesMovable.added(self, uuid)
