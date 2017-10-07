from action import *
from find_path import *
from structs import TileContent

class State:
    pass

class StateMachine:
    def __init__(self):
        self.current = StateGatherRessources()
        #self.current = None

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
        if gameMap.contains(TileContent.Resource):
            return StateGatherRessources()

        path = find_closest_tile(gameMap.tiles, Tile(TileContent.Player, player.Position.X, player.Position.Y), -1) #unknown tile
        return create_move_action(path)


class StateGoToHouse(State):
    def run(self, player, gameMap, other_players):
        print "Going to house"
        if player.Position == player.HouseLocation:
            return StateGatherRessources()

        path = find_shortest_path(gameMap.tiles, Tile(TileContent.Player, player.Position.X, player.Position.Y), Tile(TileContent.House, player.HouseLocation.X, player.HouseLocation.Y))

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
            path = find_closest_tile(gameMap.tiles, Tile(TileContent.Player, player.Position.X, player.Position.Y), TileContent.Resource)

            if path is None:
                return StateRoam()

            return create_move_action(path)
