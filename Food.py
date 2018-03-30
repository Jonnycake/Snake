from Renderable import CursesRenderable

# A piece of food
class Food(CursesRenderable):
	# Implement the constructor
	def __init__(self, game = None, collision_callback = None):
		self.character = "&"

		# We neeed the snake in our list
		#self.collision_list += game.snake.body + [game.snake.head] + [game.snake.tail]

		# We need to make sure we don't go on top of a piece of food
		self.collision_list += game.food_list

		# Call the renderable constructor
		CursesRenderable.__init__(self, game = game, collision_callback = collision_callback)
