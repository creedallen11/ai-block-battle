from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
import sys
import numpy as np

class GeneticStrategy(AbstractStrategy):
	def __init__(self, game):
		AbstractStrategy.__init__(self, game)
		self.actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

	def choose(self):
		moves = []

		rotation_count = len(self._game.piece._rotations)
		candidates = []
		# Go through rotations, positions find best drop
		for r in xrange(rotation_count):
			for pos in xrange(self._game.me.field.width):
				field = self._game.me.field.projectPieceDown(self._game.piece, [pos, 0])
				if field: candidates.append((r, pos, field))
			self._game.piece.turnRight()

		self._game.piece.turnLeft(times=rotation_count) # reset the piece
		scores = map(lambda x: self.get_height(x[2]), candidates)
		# Take the best rotation and offset and perform moves
		best_rot, best_offset, best_field = candidates[scores.index(min(scores))]

		for _ in xrange(best_rot): moves.append('turnright') # make appropriate # of turns

		offset = best_offset - 3 
		if offset > 0: action = "right"
		else: action = "left"
		for _ in xrange(abs(offset)): moves.append(action) 
		moves.append("drop")
		return moves

	
	def get_height(self, field):
		"""Transpose the fields so each entry is a column. Penalize placements in high
		locations the most. Attempt to minimize this."""
		field_tp = np.transpose(np.array(field))
		score = 0
		for col in field_tp:
			score += sum([len(col) - i for i in xrange(len(col)) if col[i] > 1])
		return score