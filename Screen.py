import curses
import uuid
import time
import copy
from Movable import CursesMovable

class CursesScreen:
	# Renderable Objects
	_objects = {}

	# Number of columns
	_MAX_X = -1

	# Number of rows
	_MAX_Y = -1

	# The key event handler
	_keyHandler = None

	# The game object
	_game = None

	# The window object as created by ncurses
	_window = None

	# Initialize some properties
	def __init__(self, game, keyHandler = None):
		# Keep track of the game for the score
		self._game = game

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
			self._window = curses.initscr()

			# Get the maximum x,y coordinates
			self._MAX_Y, self._MAX_X = self._window.getmaxyx()

			# Some ncurses settings
			# Disable line buffering
			curses.cbreak()

			# Don't display characters when user types them
			curses.noecho()

			# Act as a keypad (use string representations for function keys
			# instead of an escape sequence
			self._window.keypad(1)

			# 10 frames a second
			curses.halfdelay(1)

			# Hide the cursor
			curses.curs_set(0)
		except:
			# We died out in __init__, nothing else can take care of our issues.
			# Clean up our settings so that, hopefully, the console returns to
			# normal.
			curses.nocbreak()
			self._window.keypad(0)
			curses.echo()
			curses.endwin()
			print "Unexpected Error:", sys.exc_info()
			quit(1)

	# Wrapper for window.getkey()
	# Provided so that we can easily change display in the future, if desired
	def getKey(self):
		# Get user input
		try:
			key = self._window.getkey()
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

		# Move any movable objects
		objects = copy.copy(self._objects)
		for _uuid in objects:
			object = self._objects[_uuid]
			if object.has_key('move') and object.has_key('object'):
				if object['move'] and isinstance(object['object'], CursesMovable):
					object['object'].move()
					object['object'].check_collision()
			else:
				raise Exception("Duhhh wtf?")

		# If we should continue
		if to_continue:
			# Draw the screen
			self.draw(self._window)

		# Pass on whether or not to continue
		return to_continue

	def addObj(self, renderable, move = True, render = True):
		# Generate a new uuid
		new_uuid = str(uuid.uuid1())

		# Let everything else know there's a new renderable
		objects = copy.copy(self._objects)
		for _uuid in objects:
			if self._objects[_uuid].has_key('object'):
				object = self._objects[_uuid]['object']
				object.renderable_added(renderable)

				# Let the renderable know about everything else too
				renderable.renderable_added(object)


		# Add to our list of objects
		self._objects[new_uuid] = { "object": renderable, "move": move, "render": render }

		# Finally let the renderable know it was added
		renderable.added(new_uuid)

		return new_uuid
	def draw(self, scr):
		self._window.clear()

		for _uuid in self._objects:
			# @note Maybe  we should just make these keys a part of the renderable class...
			if self._objects[_uuid].has_key('object') and self._objects[_uuid].has_key('render') and self._objects[_uuid]['render']:
				object = self._objects[_uuid]['object']
				self._window.addch(object.y, object.x, object.character)
		# Clear then refresh the screen
		self._window.refresh()

	def print_debug(self):
		y = 0
		self._window.clear()
		for object in self._objects:
			self._window.addstr(y, 0, str(self._objects[object]['object'].debug()))
			y += 1
		self._window.refresh()
		time.sleep(10)
