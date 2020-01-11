import random
from draw_maze import draw_maze
from maze import MazeGenerator, BaseCell

w, h = 50, 50


class GITCell(BaseCell):
    @classmethod
    def get_colors(cls, kind):
        if kind == 'accessible':
            return (255, 0, 0)
        else:
            return super().get_colors(kind)


def unaccessible_neighbours(self, i, j):
    for t in self.neighbours(i, j):
        if t not in self.accessible:
            yield t


def accessible_neighbours(self, i, j):
    for t in self.neighbours(i, j):
        if t in self.accessible:
            yield t


def opened_neighbours(self, i, j):
    for t in self.neighbours(i, j):
        if t in self.opened:
            yield t


class GrowInTree(MazeGenerator):
    def __init__(self):
        super().__init__(w, h, Cell=GITCell)
        self.opened = set()
        self.accessible = []
        self.make_open(0, 0)
        self.make_accessible(1, 0)
        self.make_accessible(0, 1)

    def make_accessible(self, i, j):
        if (i, j) in self.opened:
            return False
        elif (i, j) not in self.accessible:
            self.accessible.append((i, j))
            self.cell(i, j).set_kind('accessible')
        return True

    def make_open(self, i, j):
        if (i, j) in self.accessible:
            self.accessible.remove((i, j))
        self.opened.add((i, j))
        self.cell(i, j).set_kind('empty')
        return True

    def step(self):
        if not self.accessible:
            return super().step() and False
        candidate = [t for t in self.accessible if len(list(opened_neighbours(self, *t))) == 1]

        if candidate:
            ni, nj = random.choice(candidate)
            self.make_open(ni, nj)

            for i, j in self.neighbours(ni, nj):
                self.make_accessible(i, j)
            return super().step() and True
        else:
            return super().step() and False

    def finalize(self):
        for (i, j) in self.accessible:
            self.cell(i, j).set_kind('wall')


draw_maze(GrowInTree)
