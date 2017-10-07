from structs import *
import math

def grid_size(grid):
    width = len(grid)
    height = len(grid[0]) if width > 0 else 0
    return width, height

def a_star(game_map, start, end):
    def H(start, end):
        return math.sqrt((end.X - start.X) ** 2 + (end.Y - start.Y) ** 2)

    width, height = grid_size(game_map)

    def is_walkable(tile):
        return tile.Content == 0 or tile.Content == 2

    def neighbors(node):
        x, y = node.X, node.Y
        result = []

        if x - 1 >= 0 and is_walkable(game_map[x - 1][y]):
            result.append(Point(x - 1, y))
        if x + 1 < width and is_walkable(game_map[x + 1][y]):
            result.append(Point(x + 1, y))
        if y - 1 >= 0 and is_walkable(game_map[x][y - 1]):
            result.append(Point(x, y - 1))
        if y + 1 < height and is_walkable(game_map[x][y + 1]):
            result.append(Point(x, y + 1))

        return result

    def reconstruct_path(came_from, current):
        previous = None
        while current in came_from:
            previous = current
            current = came_from[current]

        return previous

    closed_set = []
    open_set = [start]
    came_from = {}

    g_score = {}
    g_score[start] = 0

    f_score = {}
    f_score[start] = H(start, end)

    INF = 1000000000000

    while len(open_set) > 0:
        open_set.sort(key = lambda x: f_score[x] if x in f_score else INF)
        current = open_set[0]

        if current == end:
            return reconstruct_path(came_from, current)

        open_set = open_set[1: ]
        closed_set.append(current)

        for neighbor in neighbors(current):
            if neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.append(neighbor)


            test_g_score = g_score[current] + 1
            if neighbor in g_score and test_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = test_g_score
            f_score[neighbor] = test_g_score + H(neighbor, end)

    return None

def create_usable_map(server_map, pos):
    startX = pos.X - 10 - 1
    endX   = pos.X + 10 + 1
    startY = pos.Y - 10 - 1
    endY   = pos.Y + 10 + 1

    game_map = []
    for x in range(endX):
        game_map.append([])
        for y in range(endY):
            #print(str(x) + ", " + str(y))
            game_map[x].append(Tile(None, x, y))

    for rows in server_map:
        for tile in rows:
            #print "type: " + str(tile.Content) + ", x: " + str(tile.X) + ", y: " + str(tile.Y)
            game_map[tile.X][tile.Y].Content = tile.Content
    return game_map

def is_movable(tile):
    return tile and (tile.Content == 0 or tile.Content == 2)

def is_seen(target, seen):
    for tile in seen:
        if target.X == tile.X and tile.Y == target.Y:
            return True
    return False

def is_adjacent(pos1, pos2):
    if abs(pos1.X - pos2.X) == 1 and pos1.Y == pos2.Y:
        return True
    if abs(pos1.Y - pos2.Y) == 1 and pos1.X == pos2.X:
        return True
    return False

def try_get(grid, x, y):
    width, height = grid_size(grid)
    if x >= 0 and x < width and y >= 0 and y < height:
        return grid[x][y]

def is_content(tile, content):
    return tile and tile.Content == content

def is_adjacent_to_type(grid, pos, content):
    up    = try_get(grid, pos.X, pos.Y-1)
    right = try_get(grid, pos.X+1, pos.Y)
    down  = try_get(grid, pos.X, pos.Y+1)
    left  = try_get(grid, pos.X-1, pos.Y)

    return is_content(up, content) or is_content(right, content) or is_content(down, content) or is_content(left, content)

# paths: [path1, path2, ...]
# path : [Tile, prev_path]
# grid : Tile[x][y]
def find_path_helper(grid, paths, target, seen, targetOnly=True):
    if len(paths) == 0:
        return None

    # Take next path to test and remove it from queue
    tile = paths[0][0]
    path = paths[0][1]
    paths = paths[1:]

    if targetOnly:
        if is_movable(target) and tile.X == target.X and tile.Y == target.Y:
            return path

        if not is_movable(target) and is_adjacent(target, tile):
            return path
    else:
        if is_adjacent_to_type(grid, tile, target.Content):
            return path

    seen.append(tile)
    if is_movable(grid[tile.X+1][tile.Y]) and not is_seen(grid[tile.X+1][tile.Y], seen):
        paths.append([Tile(tile.Content, tile.X+1, tile.Y), path + ">"])
        seen.append(grid[tile.X+1][tile.Y])
    if is_movable(grid[tile.X-1][tile.Y]) and not is_seen(grid[tile.X-1][tile.Y], seen):
        paths.append([Tile(tile.Content, tile.X-1, tile.Y), path + "<"])
        seen.append(grid[tile.X-1][tile.Y])
    if is_movable(grid[tile.X][tile.Y+1]) and not is_seen(grid[tile.X][tile.Y+1], seen):
        paths.append([Tile(tile.Content, tile.X, tile.Y+1), path + "v"])
        seen.append(grid[tile.X][tile.Y+1])
    if is_movable(grid[tile.X][tile.Y-1]) and not is_seen(grid[tile.X][tile.Y-1], seen):
        paths.append([Tile(tile.Content, tile.X, tile.Y-1), path + "^"])
        seen.append(grid[tile.X][tile.Y-1])

    return find_path_helper(grid, paths, target, seen, targetOnly)

def convert_result(result, start):
    if result and len(result) > 0:
        start = Point(start.X, start.Y)

        if result[0] == "<":
            return start + Point(-1, 0)
        elif result[0] == "^":
            return start + Point(0, -1)
        elif result[0] == ">":
            return start + Point(1, 0)
        elif result[0] == "v":
            return start + Point(0, 1)

    return None

def find_shortest_path(grid, start, target):
    result = find_path_helper(grid, [[start, ""]], target, [start])
    return convert_result(result, start)

def find_closest_tile(grid, start, content):
    target = Tile(content, 0, 0)
    result = find_path_helper(grid, [[start, ""]], target, [start], False)
    return convert_result(result, start)
