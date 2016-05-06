from random import randint
from AbstractStrategy import AbstractStrategy
import sys
import numpy as np

class RandomStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
    	"""For all possible moves/rotations, make the move with the highest score."""
        moves = [] 
        best_rot = None
        best_position = None

        # Can probably remove this error check. Should not occur.
        if self._game.piece is not None:
        	rotation_count = len(self._game.piece._rotations)
    	else:
    		moves.append("drop")
    		return moves

        # For each rotation and position (ignoring height for now, just dropping piece down.)
        min_score = sys.maxint

        for r in xrange(rotation_count):
        	for positions in xrange(0, self._game.me.field.width):
        		field = self._game.me.field.projectPieceDown(self._game.piece, [0, positions])

        		if field is not None:
        			# calculate a score function
        			score = self.get_height(field)
        			if score < min_score:
        				min_score = score
        				best_rot = r
        				best_position = positions

			self._game.piece.turnRight()

		for _ in xrange(best_rot): moves.append('turnright')

		pos_dif = self._game.piecePosition[1] - best_position

		if pos_dif > 0: # slide to the left
			action = "left"
		else: # slide to the right
			action = "right"

		for _ in xrange(abs(pos_dif)): moves.append(action)


        moves.append('drop')
        return moves

    def generateMoves(self):
    	"""Given a target rotation & position, generate a list of moves that 
    	get piece to destination."""
    	pass

    def get_height(self, field):
    	# transpose -> list of columns where the first entry of each list is the top of the column.
    	# for each entry in the columns, if there is a block there, score how high the block is
    	field_tp = np.transpose(np.array(field))
    	score = 0
    	for col in field_tp:
    		score += sum([i for i in xrange(len(col)) if col[i] > 1])
		return score

