# automaton-create
Pretty pixel animations through the game of life

#### Create a raw 24-24 pixel animation

```python
import life

def create_life(outfile, background, palette, seed, generations=100, duration=100):
    mat = life.sid_to_mat(seed, size=10)
    mat = life.mat_padding(mat, padding=7)
    world = life.World(mat, background=background, palette=palette)
    world.gif(generations=generations, duration=duration, file=outfile)

create_life("gifs/example-raw.gif", 
            background="#FFE478", 
            palette=["#363636", "#E8175D"], 
            seed="1001110101110110110100001100011001011010000111101010111111000111010001111110101010000110001001001100")
```

#### Scale it up!
```python

life.resize_gif("gifs/example-raw.gif", "gifs/example.gif", size=350, duration=100)
```

![](https://github.com/ether-automaton/automaton-create/blob/master/gifs/example.gif)
