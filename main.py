import Simulator


winner_count = {}

for i in range(10):
    sim = Simulator.Simulator([
        {"name": "Alvin", "power": "None"},
        {"name": "Brady", "power": "None"},
        {"name": "Charlie", "power": "None"},
        {"name": "Donnie", "power": "None"},
        {"name": "Martin", "power": "None"}
        ], False)
    for player in sim.game.game_winners:
        winner_count[player.name] = winner_count.get(player.name, 0) + 1

print(winner_count)

'''
Strategies:
default - play max card on offense, random card on defense
"def-neg" - play max card on offense, negotiate (if he/she has one) on defense

'''