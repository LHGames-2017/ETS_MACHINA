from action import *

class State:
    pass

class StateMachine:
    def __init__(self):
        self.current = None

    def run(self, player, map, otherPlayers):
        action = None

        while True:
            if self.current is not None:
                action = self.current.run(player, map, other_players)
            else:
                action = create_move_action(player.Position + Point(0, -1))

            if not isinstance(action, State):
                break

        return action
