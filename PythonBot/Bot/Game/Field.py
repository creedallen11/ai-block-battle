import copy

class Field:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.field = [[0]*self.width]*self.height

    def __str__(self):
        """String representation for debug."""
        output = []
        for row in self.field:
            for value in row:
                output.append(str(value))
            output.append("\n")
        return " ".join(output)

    def size(self):
        """Getter for dim of field."""
        return self.width, self.height

    def updateField(self, field):
        """Setter for field."""
        self.field = field

    def projectPieceDown(self, piece, offset):
        """Pushes the piece down possibly with an offset.
        Returns the new field with the piece dropped in the first fit."""
        piecePositions = self.__offsetPiece(piece.positions(), offset)

        field = None
        for height in range(0, self.height-1):
            tmp = self.fitPiece(piecePositions, [0, height])

            if not tmp:
                break
            field = tmp

        return field

    @staticmethod
    def __offsetPiece(piecePositions, offset):
        piece = copy.deepcopy(piecePositions)
        for pos in piece:
            pos[0] += offset[0]
            pos[1] += offset[1]

        return piece

    def __checkIfPieceFits(self, piecePositions):
        for x,y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] > 1:
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, offset=None):
        """Fits the piecePosition to the field if the piece fits.
        Otherwise returns None. Why does this set field values to 4?"""
        if offset:
            piece = self.__offsetPiece(piecePositions, offset)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x,y in piece:
                field[y][x] = 4 # Why 4?

            return field
        else:
            return None
