import Simulator


winner_count = {}

for i in range(100):
    sim = Simulator.Simulator([
        {"name": "Alvin"}, "power": "Machine"},
        {"name": "Brady", "power": "Warpish"},
        {"name": "Charlie", "power": "Zombie"},
        {"name": "Donnie"},
        {"name": "Martin", "strategy": "def-neg"},],
        False)
    for player in sim.game.game_winners:
        winner_count[player.name] = winner_count.get(player.name, 0) + 1

print(winner_count)

'''
Strategies:
default - play max card on offense, random card on defense
"def-neg" - play max card on offense, negotiate (if he/she has one) on defense

'''