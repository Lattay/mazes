#!/usr/bin/env python

from sketcher import sketch, Sketch, config

w, h = 800, 800
nstep = 20
rate = 0.2

config.backend_use = 'tkinter'


def draw_maze(maze_generator):
    @sketch
    class Sk(Sketch):
        # you do not need to inherit from sketch but it help auto-completion
        def setup(self):
            self.size(w, h)
            self.frame(rate)
            self.maze = maze_generator()
            self.w = w / self.maze.w
            self.h = h / self.maze.h
            self.fill()
            self.fill_color((0, 0, 0))
            self.rectangle(0, 0, w, h)
            for cell in self.maze.cells():
                self.fill_color(cell.color)
                self.rectangle(self.w * cell.x, self.h * cell.y, self.w, self.h)

            self.stopped = False
            print('Inited')

        def loop(self):
            if not self.stopped:
                is_mod = False
                print('Step:', self.maze.step_num)
                for _ in range(nstep):
                    this_step = self.maze.step()
                    is_mod = is_mod or this_step
                if not is_mod:
                    self.maze.finalize()
                    self.stopped = True
                for cell in self.maze.cells():
                    self.fill_color(cell.color)
                    self.rectangle(self.w * cell.x, self.h * cell.y, self.w, self.h)
