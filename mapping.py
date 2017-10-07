from savemap import get_map, save_map
import json
from structs import TileContent, Tile

class Map:
    def __init__(self, name, default=-1):
        self.name = name
        self.tiles = []
        self.default = default
        data = get_map(name)

        try:
            self.tiles = json.loads(data)
        except Exception as e:
            pass

        width, height = self.size()

        for x in range(width):
            for y in range(height):
                self.tiles[x][y] = Tile(self.tiles[x][y], x, y)

    def save(self):
        width, height = self.size()
        tiles = []

        for x in range(width):
            tiles.append([])
            for y in range(height):
                tiles[-1].append(self.tiles[x][y].Content)

        save_map(self.name, tiles)

    def contains(self, tile_content):
        for array in self.tiles:
            for tile in self.tiles:
                if tile == tile_content:
                    return True

        return False

    def at(point):
        return self.tiles[point.X][point.Y]

    def touch(self, player, tile_content):
        left = player.Position + Point(-1, 0)
        right = player.Position + Point(1, 0)
        up = player.Position + Point(0, -1)
        down = player.Position + Point(0, 1)

        for point in [left, right, up, down]:
            if self.at(point).Content == tile_content:
                return Tile(tile_content, point.X, point.Y)

        return None

    def size(self):
        width = len(self.tiles)
        height = len(self.tiles[0]) if width > 0 else 0
        return width, height

    def update(self, player, tiles):
        width, height = self.size()

        # yolo
        xmax = -100000
        ymax = -100000

        for array in tiles:
            for tile in array:
                if tile.X > xmax:
                    xmax = tile.X

                if tile.Y > ymax:
                    ymax = tile.Y

        if player.HouseLocation.X > xmax:
            xmax = player.HouseLocation.X

        if player.HouseLocation.Y > ymax:
            ymax = player.HouseLocation.Y

        for x in range(width, xmax + 1):
            array = []

            for y in range(height):
                array.append(Tile(self.default, x, y))

            self.tiles.append(array)

        for x in range(len(self.tiles)):
            for y in range(height, ymax + 1):
                self.tiles[x].append(Tile(self.default, x, y))

        changed = False
        for array in tiles:
            for tile in array:
                content = tile.Content if tile.Content is not None else self.default

                if self.tiles[tile.X][tile.Y].Content != content:
                    self.tiles[tile.X][tile.Y].Content = content
                    changed = True

        self.tiles[player.HouseLocation.X][player.HouseLocation.Y].Content = TileContent.House

        if changed or xmax != width - 1 or ymax != height - 1:
            self.save()

    def display(self):
        entity = {
            self.default: '?',
            0: ' ',
            1: '#',
            2: 'H',
            3: 'L',
            4: 'R',
            5: 'S',
            6: 'P'
        }

        width, height = self.size()

        for y in range(height):
            out = []

            for x in range(width):
                out += [entity[self.tiles[x][y].Content]]

            print ' '.join(out)
