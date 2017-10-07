from action import *

class StateMachine:
    def __init__(self):
        self.current = None

    def run(self, player, map, otherPlayers):
        if self.current is not None:
            action = self.current.run(player, map, other_players)
        else:
            action = create_move_action(Point(-1, -1))

        return action
