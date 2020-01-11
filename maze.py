blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)


class BaseCell:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self._kind = kind
        self.color = self.get_colors(kind)

    def set_kind(self, kind):
        self._kind = kind
        self.color = self.get_colors(kind)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self._kind})'

    @classmethod
    def get_colors(cls, kind):
        if kind == 'empty':
            return white
        elif kind == 'wall':
            return black
        else:
            return blue


class MazeGenerator:
    '''
    Maze generator base class.
    '''
    def __init__(self, w, h, Cell=BaseCell):
        self.w = w
        self.h = h
        self._cells = [Cell(i, j, 'starter') for i in range(w) for j in range(h)]
        self.step_num = 0

    def valid(self, i, j):
        return (0 <= i < self.w) and (0 <= j < self.h)

    def neighbours(self, i, j):
        for di, dj in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            if self.valid(i + di, j + dj):
                yield (i + di, j + dj)

    def step(self):
        'Run one more step in maze generation.'
        self.step_num += 1
        return True

    def finalize(self):
        'Run some final transformations when the drawer decided there has been enough steps.'
        return True

    def cell(self, i, j):
        return self._cells[i + j * self.w]

    def cells(self):
        'Generator yielding cells of current state.'
        for cell in self._cells:
            yield cell
