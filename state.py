from action import *
from find_path import *
from structs import TileContent

def player_tile(player):
    return Tile(TileContent.Player, player.Position.X, player.Position.Y)

def house_tile(player):
    return Tile(TileContent.House, player.HouseLocation.X, player.HouseLocation.Y)

class State:
    pass

class StateMachine:
    def __init__(self):
        self.current = StateRoam()

    def run(self, player, map, other_players):
        action = None

        while True:
            if self.current is not None:
                action = self.current.run(player, map, other_players)
            else:
                action = create_move_action(player.Position + Point(0, -1))

            if not isinstance(action, State):
                break

            self.current = action

        return action

class StateRoam(State):
    def run(self, player, gameMap, other_players):
        # Try to find a resource
        if gameMap.contains(TileContent.Resource):
            return StateGatherRessources()

        # If no resources are found, try to find a way to an unexplored tile
        path = find_closest_tile(gameMap.tiles, player_tile(player), -1)

        # Check if a path to an unexplored tile was found
        if path is not None:
            return create_move_action(path)
        else:
            # Break a wall to (hopefully) find a path to an unexplored tile
            return StateBreakWall()


class StateGoToHouse(State):
    def run(self, player, gameMap, other_players):
        print "Going to house"
        if player.Position == player.HouseLocation:
            return StateGatherRessources()

        path = find_shortest_path(gameMap.tiles, player_tile(player), house_tile(player))

        if path:
            return create_move_action(path)
        else:
            return create_move_action(Point(player.Position))

#gather closest ressource point from the player
class StateGatherRessources(State):
    def run(self, player, gameMap, other_players):
        print "Gathering"
        if player.CarriedResources >= player.CarryingCapacity:
            return StateGoToHouse()

        closestResource = gameMap.touch(player, TileContent.Resource)

        if closestResource:
            return create_collect_action(closestResource)
        else:
            path = find_closest_tile(gameMap.tiles, player_tile(player), TileContent.Resource)

            if path is None:
                return StateRoam()

            return create_move_action(path)

class StateBreakWall(State):
    def __init__(self):
        self.found_wall = None

    def run(self, player, gameMap, other_players):
        if self.found_wall:
            if gameMap.touch(player, TileContent.Wall) == self.found_wall:
                return create_attack_action(self.found_wall)
            else:
                return StateRoam()
        else:
            wall = find_closest_tile(gameMap.tiles, player_tile(player), TileContent.Wall)

            if wall is None:
                self.found_wall = gameMap.touch(player, TileContent.Wall)
                return self.run(player, gameMap, other_players)
            else:
                return create_move_action(wall)
