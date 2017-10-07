from action import *

class State:
    pass

class StateMachine:
    def __init__(self):
        self.current = StateGatherRessources()

    def run(self, player, map, otherPlayers):
        if self.current is not None:
            action = self.current.run(player, map, other_players)
        else:
            action = create_move_action(Point(-1, -1))

        return action

pointConversion ⁼ {'^': Point(0, -1), '<': Point(-1, 0), '>': Point(1, 0), 'v': Point(0, 1) }

def getNextMove(playerPos, path):
    return playerPos + pointConversion[path[0]]

class StateRoam(State):
    def run(player, gameMap, other_players):

        if gameMap.contains(TileContent.Resource):
            return StateGatherRessources()

        path = findShortestPathToType(gameMap, player.Position, -1) #unknown tile
        return create_move_action(getNextMove(player.Position, path))


class StateGoToHouse(State):
    def run(player, gameMap, other_players):

        if player.Position == player.HouseLocation:
            return StateGatherRessources()

        path = findShortestPath(gameMap, player.Position, player.HouseLocation)
        return create_move_action(getNextMove(player.Position, path))

#gather closest ressource point from the player
class StateGatherRessources(State):

    def run(player, gameMap, other_players):

        if player.CarriedResources >= player.CarryingCapacity:
            return StateGoToHouse()

        path = findShortestPathToType(gameMap, player.Position, TileContent.Resource)

        if path is None:
            return StateRoam()

        closestResource = gameMap.touch(TileContent.Resource)
        if len(path) == 0:
            return create_collect_action(closestResource)
        else:
            return create_move_action(getNextMove(player.Position, path))
