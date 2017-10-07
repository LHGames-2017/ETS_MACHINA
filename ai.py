from flask import Flask, request
from structs import *
from find_path import *
import json
import numpy

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

entity = {
    0: ' ',
    1: '#',
    2: 'H',
    3: '~',
    4: 'R',
    5: 'S',
    6: 'J'
}

def print_map(m):
    #m = json.loads(m)[u"CustomSerializedMap"]
    m = json.loads(m.replace('{', '[').replace('}', ']'))

    for y in m:
        out = []
        for x in y:
            out += [entity[x[0]]]
        print ' '.join(out)

def move_to_path(pos, path):
    if len(path) == 0:
        return pos
    if path[0] == '^':
        return Point(pos.X, pos.Y-1)
    if path[0] == 'v':
        return Point(pos.X, pos.Y+1)
    if path[0] == '>':
        return Point(pos.X+1, pos.Y)
    if path[0] == '<':
        return Point(pos.X-1, pos.Y)
    # something went very wrong
    return pos

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info
    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    print_map(serialized_map)
    deserialized_map = deserialize_map(serialized_map)

    otherPlayers = []

    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]

            if player_info == "notAPlayer":
                continue

            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info })

    print "Resources"
    print player.CarriedRessources
    print player.CarryingCapacity
    print "House pos:"
    print player.HouseLocation.X
    print player.HouseLocation.Y
    print "Player pos:"
    print player.Position.X
    print player.Position.Y

    pos = player.Position


    game_map = create_usable_map(deserialized_map, player.Position)
    if player.CarriedRessources == player.CarryingCapacity:
        path  = find_shortest_path(game_map, Tile(6, pos.X, pos.Y), Tile(2, player.HouseLocation.X, player.HouseLocation.Y))
        point = move_to_path(player.Position, path)
        return create_move_action(point)

    path = find_closest_tile(game_map, Tile(6, player.Position.X, player.Position.Y), 4)
    point = move_to_path(player.Position, path)
    if len(path) == 0:
        print "Collect!"
        # find tile to collect
        if game_map[pos.X+1][pos.Y].Content == 4:
            return create_collect_action(game_map[pos.X+1][pos.Y])
        if game_map[pos.X-1][pos.Y].Content == 4:
            return create_collect_action(game_map[pos.X-1][pos.Y])
        if game_map[pos.X][pos.Y+1].Content == 4:
            return create_collect_action(game_map[pos.X][pos.Y+1])
        if game_map[pos.X][pos.Y-1].Content == 4:
            return create_collect_action(game_map[pos.X][pos.Y-1])
    return create_move_action(point)

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
