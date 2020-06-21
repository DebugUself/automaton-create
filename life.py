from PIL import Image, ImageDraw, ImageSequence

# Enlarge a raw 24-24 pixel GIF to a desired size
def resize_frames(frames, size):
    for frame in frames:
        f = frame.copy()
        f = f.resize((size, size))
        yield f

def resize_gif(infile, outfile, size=350, duration=100):
    im = Image.open(infile)
    frames = ImageSequence.Iterator(im)
    frames = resize_frames(frames, size)
    om = next(frames)
    om.info = im.info
    om.save(outfile, 
            save_all=True, 
            append_images=list(frames),
            optimize=False, 
            duration=duration, 
            loop=0)

import copy
import random
import math
import numpy

# The actual algorithm part
def random_color(palette):
    color = palette[int(random.uniform(0, len(palette)))]
    return(color)

def mat_random(size, seed=0):
    numpy.random.seed(seed)
    mat = [[numpy.random.binomial(1, p=0.5) for x in range(size)] for y in range(size)]
    return(mat)

def mat_padding(mat, padding=0):
    size = len(mat)
    for y in range(size):
        for i in range(padding):
            mat[y].insert(0, 0)
            mat[y].append(0)
    for i in range(padding):
        mat.insert(0, [0 for i in range(size+padding*2)])
        mat.append([0 for i in range(size+padding*2)])
    return(mat)

def mat_to_sid(mat):
    vals = []
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            vals.append(str(mat[y][x]))
    sid = "".join(vals)
    return(sid)

def sid_to_mat(sid, size):
    vals = [int(i) for i in sid]
    mat = [[vals.pop(0) for x in range(size)] for y in range(size)]
    return(mat)

class Cell:
    def __init__(self, x, y, state=0, color="black"):
        self.x = x
        self.y = y
        self.state = state
        self.color = color

    def is_alive(self):
        return(self.state == 1)

    def get_state(self):
        return(self.state)

class World():
    def __init__(self, mat, background="white", palette=["black"]):
        self.background = background
        self.palette = palette
        self.x = len(mat[0])
        self.y = len(mat)
        self.cells = copy.deepcopy(mat)
        for y in range(self.y):
            for x in range(self.x):
                state = mat[y][x]
                self.cells[y][x] = Cell(x, y, state, color=random_color(palette))

    def show(self):
        for y in range(self.y):
            for x in range(self.x):
                cell = self.cells[y][x]
                print(cell.state, end=" ")
            print("\n", end="")

    def get_neighbors(self, cell):
        y_u = cell.y-1 if (cell.y-1 >= 0) else self.y-1
        y_d = cell.y+1 if (cell.y+1 <= self.y-1) else 0
        x_l = cell.x-1 if (cell.x-1 >= 0) else self.x-1
        x_r = cell.x+1 if (cell.x+1 <= self.x-1) else 0

        return([
            self.cells[cell.y][x_l].get_state(),
            self.cells[cell.y][x_r].get_state(),
            self.cells[y_u][cell.x].get_state(),
            self.cells[y_d][cell.x].get_state(),
            self.cells[y_u][x_l].get_state(),
            self.cells[y_u][x_r].get_state(),
            self.cells[y_d][x_l].get_state(),
            self.cells[y_d][x_r].get_state()
        ])

    def get_fate(self, cell):
        neighbors = self.get_neighbors(cell)
        population = sum(neighbors)

        if cell.is_alive():
            if population < 2 or population > 3:
                fate = 0
            else:
                fate = 1
        else:
            if population == 3:
                fate = 1
            else:
                fate = 0

        return(fate)

    def step(self):
        cells_next = [[0 for x in range(self.x)] for y in range(self.y)]
        for y in range(self.y):
            for x in range(self.x):
                cell = self.cells[y][x]
                fate = self.get_fate(cell)
                cells_next[y][x] = copy.deepcopy(cell)
                cells_next[y][x].state = fate
        self.cells = cells_next

    def draw(self):
        img = Image.new('RGBA', (self.x, self.y), self.background)
        draw = ImageDraw.Draw(img)
        for y in range(self.y):
            for x in range(self.x):
                cell = self.cells[y][x]
                if cell.is_alive():
                    draw.rectangle(xy=[(cell.x, cell.y), (cell.x+1, cell.y+1)], fill=cell.color)
        return(img)

    def gif(self, generations, duration, file):
        images = []
        for i in range(generations):
            images.append(self.draw())
            self.step()

        images[0].save(file,
                       save_all=True, 
                       append_images=images[1:], 
                       optimize=False, 
                       duration=duration, 
                       loop=0)
