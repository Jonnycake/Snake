from Game import Game
from Snake import CursesSnake
import time

# The Game...you just lost it
class SnakeGame(Game):
	lost = False

	# Maybe we can make controls configurable...
	keyMap = {"KEY_UP": "u", "KEY_DOWN": "d", "KEY_LEFT": "l", "KEY_RIGHT": "r"}

	# The current score
	score = None

	# List of food objects
	food_list = []

	# The snake
	snake = None

	# Game rules
	rules = {"rgrow": 0, "igrow": 0, "traps": 0}

	# Initialize some properties
	def __init__(self, args = None):
		if args is not None:
			# Set up our twists :P
			self.rules = {"rgrow": args.rgrow, "traps": args.traps, "igrow": args.igrow}

		# Call superclass Init
		Game.__init__(self)

		# Create the snake
		self.snake = CursesSnake(game = self)

		# Add our snake to the screen
		self.screen.addObj(self.snake)

	# Keyboard Input Callback
	def keyHandler(self, key):
		# If it's a directional key
		if self.keyMap.has_key(key):
			direction = self.keyMap[key]
			self.snake.turn(direction)

		# If it's q, quit
		elif key.lower() == "q":
			# Let the user know that they're quitting
			# @note This should be handled in Screen
			# @todo 

			# Sleep for a second
			time.sleep(1)

			# We don't want to continue, so return false
			return False

		# If it's p, pause
		elif key.lower() == "p":
			# Let the user know the game is paused
			# @note This should be handled in Screen
			# @todo

			# Until they  hit the pause button again, do nothing
			while self.screen.getKey() != "p":
				pass

		# Only continue if we haven't lost yet
		return not self.lost

	# Eat callback
	def eat(self, food):
		# This SHOULD be this object, if it's not or score is None then something broke
		if self.__class__.__name__ != "Game" or self.score is None:
			raise ValueError("An invalid object was passed to the eat callback!")

		# We should grow and increase the score
		self.snake.grow()

		# Increase the score
		self.score += 1

		# Take the food out of our list
		self.food_list.pop()

	# Play the game (handle keyboard input and food)
	def play(self):
		to_continue = True
		while to_continue:
			to_continue = Game.frame(self)

	# You lose :'(
	def lose(self):
		# Set our lost property to true so it exits on the next frame
		self.lost = True

