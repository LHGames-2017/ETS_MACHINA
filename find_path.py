from structs import *

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
    return tile.Content == 0 or tile.Content == 2

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

def is_adjacent_to_type(grid, pos, content):
    up    = grid[pos.X][pos.Y-1]
    right = grid[pos.X+1][pos.Y]
    down  = grid[pos.X][pos.Y+1]
    left  = grid[pos.X-1][pos.Y]

    return up.Content == content or right.Content == content or down.Content  == content or left.Content  == content

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

def find_shortest_path(grid, start, target):
    return find_path_helper(grid, [[start, ""]], target, [start])

def find_closest_tile(grid, start, content):
    target = Tile(content, 0, 0)
    return find_path_helper(grid, [[start, ""]], target, [start], False)
