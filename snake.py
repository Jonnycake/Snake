#!/usr/bin/python
# Snake - Yet another snake implementation...
# Copyright (C) 2018  Jon Stockton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import curses
import random
import time

# Coordinate abstract class
class Coordinate:
	# x coordinate
	x = None

	# y coordinate
	y = None

	# z coordinate - doesn't apply currently
	z = None

	# Base class will not implement __init__(), exending classes should
	def __init__(self):
		raise NotImplementedError("Classes extending Coordinate MUST implement a constructor")

	# Check if there's any object at the same (x, y) as us
	def touching(self, collision_list):
		# coordinate_list is an array of Coordinates
		for coordinate in collision_list:
			# If our coordinates are the same, we are touching
			if coordinate.x == self.x and coordinate.y == self.y and coordinate.z == self.z:
				# Return the object we're touching
				return coordinate

		# Otherwise return false
		return False

# A piece of food
class Food(Coordinate):
	# Implement the constructor
	def __init__(self, game = None):
		# Generate a random position based on min and max with screen
		self.x = random.randint(0, game.screen.MAX_X - 1)
		self.y = random.randint(0, game.screen.MAX_Y - 1)

		# Set up our collision list (don't generate on top of the snake
		# or another piece of food)
		collision_list = []

		# We neeed the body
		collision_list += game.snake.body

		# We need the head
		collision_list.append(game.snake.head)

		# We neeed the tail
		collision_list.append(game.snake.tail)

		# We need to make sure we don't go on top of another piece of food
		# @note Not necessary, I was originally thinking of having multiple
		# pieces of foo at the same time, though
		collision_list += game.food_list

		# If we're touching anything in the collision_list, regenerate coordinates
		while self.touching(collision_list):
			self.x = random.randint(0, game.screen.MAX_X - 1)
			self.y = random.randint(0, game.screen.MAX_Y - 1)

		# Finally render us on the screen
		# @note It would be nice for Screen to handle this...
		game.screen.window.addch(self.y, self.x, "&")

# A part of the snake..
class SnakePart(Coordinate):
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

	# Initialize some properties
	def __init__(self, tail = None, is_head = False, game = None):
		# Either tail position must be defined or it must be the head of the snake
		if not is_head and tail is None:
			raise ValueError("A non-head part of the snake was initialized and no tail was provided!")

		# Game must be provided so we know how to wrap our coordinates
		if game is None:
			raise ValueError("A game must be provided to SnakePart!")
-		self.game = game

		# If it's the head we can set the position to a random location
		if is_head:
			# We need a screen object to find min and max
			#if screen is None or screen.__class__.__name__ != "Screen":
			#	raise ValueError("A valid screen object was not passed when initializing the head!")
			self.x = random.randint(0, self.game.screen.MAX_X - 1)
			self.y = random.randint(0, self.game.screen.MAX_Y - 1)
			self.direction = "r"

		# Otherwise we should follow the tail
		else:
			self.follow(tail)


	# Follow another part
	def follow(self, adjacent_part):
		# If adjacent_part is not a SnakePart, we don't know how to follow it
		if not adjacent_part.__class__.__name__ == "SnakePart":
			raise ValueError("A part of the snake was told to follow an object that was not a SnakePart!")

		# We just set following to adjacent_part
		self.following = adjacent_part

		# We need to set the coordinates based on direction
		# NOTE: Coordinates in ncurses are based on the upper left hand corner
		#       as the origin (0, 0), down increases y, right increases x
		# Up: new.x = adjacent.x; new.y = adjacent.y + 1
		if adjacent_part.direction == "u":
			self.x = adjacent_part.x
			self.y = adjacent_part.y + 1

		# Down: new.x = adjacent.x; new.y = adjacent.y - 1
		elif adjacent_part.direction == "d":
			self.x = adjacent_part.x
			self.y = adjacent_part.y -1

		# Left: new.x = adjacent.x - 1; new.y = adjacent.y
		elif adjacent_part.direction == "l":
			self.x = adjacent_part.x + 1
			self.y = adjacent_part.y

		# Right: new.x = adjacent.x + 1; new.y = adjacent.y
		elif adjacent_part.direction == "r":
			self.x = adjacent_part.x - 1
			self.y = adjacent_part.y

		# Otherwise it's busted
		else:
			raise ValueError("An invalid direction ('%s') was found!" % (adjacent_part.direction))

		# Finally set our direction to that of the adjacent_part
		self.direction = adjacent_part.direction

	# Move this part
	def move(self):
		# Set the old position
		self.old_position = (self.x, self.y)

		# Move in the appropriate direction
		# @note Using modulo division to provide wrapping
		# Up: y -= 1
		if self.direction == "u":
			self.y = (self.y - 1) % self.game.screen.MAX_Y

		# Down: y += 1
		elif self.direction == "d":
			self.y = (self.y + 1) % self.game.screen.MAX_Y

		# Left: x -= 1
		elif self.direction == "l":
			self.x = (self.x - 1) % self.game.screen.MAX_X

		# Right: x += 1
		elif self.direction == "r":
			self.x = (self.x + 1) % self.game.screen.MAX_X

		# Set the old direction
		self.old_direction = self.direction

		# NOTE: Now if we're following a part we are currently in the position
		#       it used to be at, meaning, that we must set our direction, to the
		#       old direction of it (to follow the same path).  This is really
		#       just to get around using ugly positional logic...
		if self.following is not None:
			self.direction = self.following.old_direction

# The snake...
class Snake:
	opposites = { "u": "d", "d": "u", "r": "l", "l": "r"}
	# The head is a SnakePart object
	# @note We could make t his part of the body and just use index 0
	head = None

	# Our body will be an array of SnakeParts
	body = None

	# The tail is a SnakePart oobject
	# @note We could make this part of the body and just use index -1
	tail = None

	# The callback for eating a piece of food
	eat = None

	# The game that we're in
	game = None

	# Whether or not we grew
	grew = False

	# Initialize some properties
	def __init__(self, game = None, eat = None, screen = None):
		# Game is what handles gameplay
		if game is None:
			raise ValueError("A game must be provided!")

		# Eat is what we call when we run into food
		if eat is None:
			raise ValueError("An eat callback must be provided!")

		# Screen is used for dimensions
		if screen is None:
			raise ValueError("A screen object must be provided!")

		# Hold onto the game object
		self.game = game

		# Create a new head
		self.head = SnakePart(is_head = True, game = game)

		# We don't start with a  body
		self.body = []

		# The tail directly follows the head
		self.tail = SnakePart(tail = self.head, game = game)

		# Finally set up our eat callback
		self.eat = eat


	# Turn the head of the snake a specific direction
	def turn(self, direction):
		if direction != self.opposites[self.head.direction]:
			# Keyboard input is interpreted already into the direction character
			self.head.direction = direction

	# Move on space
	def move(self):
		# Move the head first
		self.head.move()

		# If we hit a piece of food, eat it
		food = self.head.touching(self.game.food_list)
		if food:
			# Assign to a variable so we don't pass our self to the method
			#  @note Not entirely sure you need to do this, but I am to be
			#        safe, I'll experiment with it and see if I can take
			#        this out
			self.eat(food)


		# Then move each piece of the body (front to back)
		for part in self.body:
			part.move()

		# Then move the tail
		self.tail.move()

		# Finally, we need to make sure we aren't touching anything
		# Get the list of objects to check
		# @note array + array returns a union of the two arrays
		if self.head.touching(self.body + [self.tail]):
			self.game.lose()

	# Add a new SnakePart
	def grow(self):
		# Add the tail to the body
		self.body.append(self.tail)

		# The tail is a new object that follows the old one
		self.tail = SnakePart(tail = self.body[-1], game = self.game)

		# Set grew to True
		self.grew = True

class Screen:
	# Number of columns
	MAX_X = -1

	# Number of rows
	MAX_Y = -1

	# The key event handler
	keyHandler = None

	# The game object
	game = None

	# The snake
	# @note It would be nice not to have this in here
	snake = None

	# The window object as created by ncurses
	window = None

	# Initialize some properties
	def __init__(self, game, keyHandler = None):
		# Keep track of the game for the score
		self.game = game

		# If keyHandler isn't dfeined, we can just assume
		# it's game.keyHandler() for our purposes
		if keyHandler is None:
			# Default
			self.keyHandler = game.keyHandler
		else:
			# Let their defined handler do stuff
			self.keyHandler = keyHandler

		# Set up the curses interface
		try:
			# Initialize the screen
			self.window = curses.initscr()

			# Get the maximum x,y coordinates
			self.MAX_Y, self.MAX_X = self.window.getmaxyx()

			# Some ncurses settings
			# Disable line buffering
			curses.cbreak()

			# Don't display characters when user types them
			curses.noecho()

			# Act as a keypad (use string representations for function keys
			# instead of an escape sequence
			self.window.keypad(1)

			# 10 frames a second
			curses.halfdelay(1)
		except:
			# We died out in __init__, nothing else can take care of our issues.
			# Clean up our settings so that, hopefully, the console returns to
			# normal.
			curses.nocbreak()
			self.window.keypad(0)
			curses.echo()
			curses.endwin()
			print "Unexpected Error:", sys.exc_info()
			quit(1)

	# Wrapper for window.getkey()
	# Provided so that we can easily change display in the future, if desired
	def getKey(self):
		# Get user input
		try:
			key = self.window.getkey()
			return key

		# We get an exception if no input was passed, so just return an empty string...
		except Exception as e:
			return ""

	# Update the screen
	def update(self):
		# Get user input
		key = self.getKey()

		# The keyHandler will tell us whether to quit or continue
		to_continue = self.keyHandler(key)

		# If we should continue
		if to_continue:
			# Tell the snake to move one tick
			# @note This should be moved into a hook instead
			self.snake.move()

			# Draw the screen
			self.draw(self.window)

		# Pass on whether or not to continue
		return to_continue

	def draw(self, scr):
		# Since our innitial size is 2, we only need to update the head
		# and the tail, the other pieces will remain the same

		# NOTE: Coordinates in ncurses are reversed (y, x) instead of (x, y)
		# Set the new head position to an @
		self.window.addch(self.snake.head.y, self.snake.head.x, "@")

		# Set the old head position to a *
		#if self.snake.head.old_position is not None:
		if self.snake.head.old_position is not None:
			self.window.addch(self.snake.head.old_position[1], self.snake.head.old_position[0], "*")

		# If the snake didn't grow, set the tail position to a blank
		if not self.snake.grew:
			# If old_position is None, then we haven't moved yet (it's the first frame)
			if self.snake.tail.old_position is None:
				# Add the * for the tail
				self.window.addch(self.snake.tail.y, self.snake.tail.x, "*")
			else:
				# Add a space to overwrite the * that was there
				self.window.addch(self.snake.tail.old_position[1], self.snake.tail.old_position[0], " ")

		# Reset the snake.grew property
		self.snake.grew = False

		# Move the cursor back to the origin
		self.window.move(0,0)

		# Refresh the screen
		self.window.refresh()

	def setSnake(self, snake):
		# Just keep track of our snake since we have to display it
		self.snake = snake

# The Game...you just lost it
class Game:
	# Did we lose yet?
	lost = False

	# Maybe we can make controls configurable...
	keyMap = {"KEY_UP": "u", "KEY_DOWN": "d", "KEY_LEFT": "l", "KEY_RIGHT": "r"}

	# The screen object
	screen = None

	# The current score
	score = None

	# List of food objects
	food_list = []

	# The snake
	snake = None

	# Initialize some properties
	def __init__(self):
		# Score starts at 0, obviously
		self.score = 0

		# We need a screen to display on
		self.screen = Screen(self, keyHandler = self.keyHandler)

		# Create the snake
		self.snake = Snake(eat = self.eat, screen = self.screen, game = self)

		# Add the snake to the screen
		self.screen.setSnake(self.snake)

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
			self.screen.window.addstr(0, 0, "Quitting game...")
			self.screen.window.refresh()

			# Sleep for a second
			time.sleep(1)

			# We don't want to continue, so return false
			return False

		# If it's p, pause
		elif key.lower() == "p":
			# Let the user know the game is paused
			# @noet This should be handled in Screen
			self.screen.window.addstr(0, 0, "Paused")

			# Until they  hit the pause button again, do nothing
			while self.screen.getKey() != "p":
				pass

			# Get rid of the paused string
			self.screen.window.addstr(0, 0, "      ")

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
		while 1:
			# If there's no food on the screen
			if not len(self.food_list):
				# Create a new piece of food
				self.food_list.append(Food(self))

			# Check if we should continue based on update()
			to_continue = self.screen.update()

			# If we shouldn't, then break
			if not to_continue:
				break

	# You lose :'(
	def lose(self):
		# Set our lost property to true so it exits on the next frame
		self.lost = True

try:
	# Create a game object
	game = Game()

	# Start the main loop
	game.play()
finally:
	# Unset all the settings we set earlier
	game.screen.window.keypad(0)
	curses.nocbreak()
	curses.echo()
	curses.endwin()

	# If they lost instead of quit
	if game.lost:
		print "You lost :'("

	# Otherwise they must've quit or there was an error
	else:
		print "Leaving so soon? :/"

	# Let them know what their score was...
	print "Final score: %d" % (game.score)
