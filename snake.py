#!/usr/bin/python
import curses
from SnakeGame import SnakeGame
import argparse
import sys
import traceback

# Parse our arguments for a twist :D
parser = argparse.ArgumentParser(description='Snake game...twists added ;P')
parser.add_argument('--rgrow', type=int, action='store', help='Grow the snake randomly at a <RGROW>%% percent chance')
parser.add_argument('--traps', type=int, action='store', help='Create a <TRAPS> (count) traps on the level')
parser.add_argument('--igrow', type=int, action='store', help='Grow regularly ever <IGROW> frames')
args = parser.parse_args()

try:
	# Create a game object
	game = SnakeGame()

	# Start the main loop
	game.play()
except Exception as e:
	exception_error = sys.exc_info()
	print "Why?"
	print traceback.print_tb(exception_error[2])
finally:
	# Unset all the settings we set earlier
	# @todo move into the screen
	game.screen._window.keypad(0)
	curses.nocbreak()
	curses.echo()
	curses.endwin()

	# If they lost instead of quit
	if game.lost:
		print "You lost :'("

	# Otherwise they must've quit or there was an error
	else:
		exception_error = sys.exc_info()
		print exception_error
		traceback.print_tb(exception_error[2])
		print "Leaving so soon? :/"

	# Let them know how many frames they lasted...
	print "Frame count: %d" % (game.frames)

	# Let them know what their score was...
	print "Final score: %d" % (game.score)
