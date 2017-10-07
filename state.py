from action import *
from find_path import *
from structs import TileContent

class State:
    pass

class StateMachine:
    def __init__(self):
        self.current = StateGatherRessources()

    def run(self, player, map, other_players):
        action = None

        while True:
            if self.current is not None:
                action = self.current.run(player, map, other_players)
            else:
                action = create_move_action(player.Position + Point(0, -1))

            if not isinstance(action, State):
                break

        return action

pointConversion = {'^': Point(0, -1), '<': Point(-1, 0), '>': Point(1, 0), 'v': Point(0, 1) }

def getNextMove(playerPos, path):
    return playerPos + pointConversion[path[0]]

class StateRoam(State):
    def run(self, player, gameMap, other_players):

        if gameMap.contains(TileContent.Resource):
            return StateGatherRessources()

        path = find_closest_tile(gameMap.tiles, Tile(TileContent.Player, player.Position.X, player.Position.Y), -1) #unknown tile
        return create_move_action(getNextMove(player.Position, path))


class StateGoToHouse(State):
    def run(self, player, gameMap, other_players):

        if player.Position == player.HouseLocation:
            return StateGatherRessources()

        path = findShortestPath(gameMap.tiles, player.Position, player.HouseLocation)
        return create_move_action(getNextMove(player.Position, path))

#gather closest ressource point from the player
class StateGatherRessources(State):

    def run(self, player, gameMap, other_players):

        if player.CarriedResources >= player.CarryingCapacity:
            return StateGoToHouse()

        path = find_closest_tile(gameMap.tiles, Tile(TileContent.Player, player.Position.X, player.Position.Y), TileContent.Resource)

        if path is None:
            return StateRoam()

        closestResource = gameMap.touch(TileContent.Resource)
        if len(path) == 0:
            return create_collect_action(closestResource)
        else:
            return create_move_action(getNextMove(player.Position, path))
