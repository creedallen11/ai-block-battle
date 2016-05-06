# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
import random
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from math import sqrt

class FirstStray(AbstractStrategy):
    def __init__(self, game, w1=0.7, w2=0.3):
        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']
        self.log = open('first_log.txt', 'w')
        self.count = 0
        self.w1 = w1
        self.w2 = w2

    def choose(self):
        ind = [randint(0, 4) for _ in range(1, 10)]
        # moves = map(lambda x: self._actions[x], ind)
        # moves = list(map(lambda x: self._actions[x], ind))
        game = self._game
        field = game.me.field
        piece = game.piece

        projs = []
        for i in range(field.width):
            flag = True
            while flag:
                flag = piece.turnLeft() 
            projs.append((piece._rotateIndex, i, field.projectPieceDown(piece, [i,0])))
            while piece.turnRight():
                projs.append((piece._rotateIndex, i, field.projectPieceDown(piece, [i,0])))
        projs = filter(lambda x: x[2], projs)

        bproj = self.best_proj(projs,field)
        self.log.write('bproj %d(%d,%d):\n' % (self.count, bproj[0], bproj[1]))
        self.log.write(self.fstr(bproj) + '\n')
        self.count += 1



        moves = [self._actions[x] for x in ind]
        moves.append('drop')


        return self.get_moves(bproj)

    def get_moves(self, bproj):
        piece = self._game.piece
        ri,h_off = bproj[0],bproj[1]
        mvs = []
        if ri != 0:
            t = 'turnright'
            if ri < 0:
                t = 'turnleft'
                ri = -ri
            for i in range(ri):
                mvs.append(t)
        to_slide = h_off - piece.start_x
        s = 'right'
        if to_slide < 0:
            s = 'left'
            to_slide = -to_slide
        for i in range(to_slide):
            mvs.append(s)
        mvs.append('drop')
        return mvs


    def close(self):
        x = 1
        self.log.close()

    def best_proj(self, projs,f):
        errs = map(lambda x: (self.error(x[2],f), x), projs)
        s = sorted(errs, key=lambda x: x[0])
        err = s[0][0]
        res = list(filter(lambda x: x[0] == err, s))
        random.shuffle(res)
        return res[0][1]

    def error(self, proj,f):
        e_general_holes = 0
        e_bad_holes = 0
        f = f.field
        orig_err = self.col_err(f)


        # general_holes, vertical depth
        errs = [self.e1(proj),self.col_err(proj)]

        if self.w1 == 0.0 and self.w2 == 0.0:
            return tuple(errs)
        errs[0] *= self.w1
        errs[1] *= self.w2

        return sum(errs)

    def e1(self, proj):
        tot = 0
        for i in range(len(proj)-1):
            r = len(proj)-(i+1)
            row = proj[r]
            rs = set(row)
            if 0 in rs and len(rs) == 1:
                break
            tot += ((float(i+1) ** (-1)) * sum([x == 0 for x in proj[r]]))
        return tot
    
    def col_err(self, proj):
        for i in range(len(proj[0])):
            proj[0][i] = 0
        cols = self.trans(proj)
        err = 0
        for c in cols:
            flag = False
            te = 0
            for i in range(len(c)):
                if c[i] != 0:
                    flag = True
                elif c[i] == 0 and flag:
                    te += 1
            err += te ** 2
        return err

    def trans(self,proj):
        cols = [[0 for i in range(len(proj))] for j in range(len(proj[0]))]
        for x in range(len(proj)):
            for y in range(len(proj[x])):
                cols[y][x] = proj[x][y]
        return cols

    def fstr(self,f):
        s = ""
        f = f[2]
        for r in f:
            s+= "".join(map(lambda x: str(x),r))
            s+='\n'
        return s