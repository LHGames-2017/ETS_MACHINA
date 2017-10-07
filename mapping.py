from savemap import get_map, save_map
import json

class Map:
    def __init__(self, name):
        self.name = name
        self.tiles = [[]]

        try:
            data = get_map(name)
            self.tiles = json.loads(data)
        except:
            pass

    def update(self, tiles):
        width = len(self.tiles)
        height = len(self.tiles[0]) if width > 0 else 0

        # yolo
        xmax = -100000
        ymax = -100000

        for array in tiles:
            for tile in array:
                if tile.X > xmax:
                    xmax = tile.X

                if tile.Y > ymax:
                    ymax = tile.Y


        for _ in range(xmax - width + 1):
            self.tiles.append([-1] * height)

        for array in self.tiles:
            for _ in range(ymax - height + 1):
                array.append(-1)

        changed = False
        for array in tiles:
            for tile in array:
                content = tile.Content if tile.Content is not None else -1

                if self.tiles[tile.X][tile.Y] != content:
                    self.tiles[tile.X][tile.Y] = content
                    changed = True

        if changed or xmax != width - 1 or ymax != height - 1:
            save_map(self.name, self.tiles)

    def display(self):
        entity = {
            -1: '?',
            0: ' ',
            1: '#',
            2: 'H',
            3: 'P',
            4: 'R',
            5: '~',
            6: 'S'
        }

        width = len(self.tiles)
        height = len(self.tiles[0]) if width > 0 else 0

        for y in range(height):
            out = []

            for x in range(width):
                out += [entity[self.tiles[x][y]]]

            print ' '.join(out)
