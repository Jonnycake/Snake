from Screen import CursesScreen

# The Game...you just lost it
class Game:
	# Track our frames
	frames = 0

	# Did we lose yet?
	lost = False

	# Maybe we can make controls configurable...
	keyMap = {}

	# The screen object
	screen = None

	# The current score
	score = None

	# Initialize some properties
	def __init__(self, screenClass = None):
		# Score starts at 0, obviously
		self.score = 0

		if screenClass is None:
			# We need a screen to display on
			self.screen = CursesScreen(self, keyHandler = self.keyHandler)

	# Keyboard Input Callback
	# @note Default implementation is do absolutely nothing
	def keyHandler(self, key):
		return True

	# Tell the screen to update
	def frame(self):
		# Check if we should continue based on update()
		to_continue = self.screen.update()

		# Increment our frame count
		self.frames += 1

		# Pass on to_continue
		return to_continue

	# You lose :'(
	def lose(self):
		# Set our lost property to true so it exits on the next frame
		self.lost = True

