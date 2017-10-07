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

    def update(tiles):
        width = len(self.tiles)
        height = len(self.tiles[0]) if width > 0 else 0

        xmax = -100000
        ymax = -100000

        for array in tiles:
            for tile in array:
                if tile.x > xmax:
                    xmax = tile.x

                if tile.y > ymax:
                    ymax = tile.y

        if ymax >= height:
            for array in self.tiles:
                array.append(-1)

        if xmax >= width:
            self.tiles.append([-1] * ymax)

        for array in tiles:
            for tile in array:
                self.tiles[tile.X][tile.Y] = tile.Content

    def display():
        pass
