import Simulator


winner_count = {}
num_games_simulated = 2000

for i in range(num_games_simulated):
    sim = Simulator.Simulator([
        {"name": "Alvin", "power": "Machine"},
        {"name": "Brady", "power": "Virus"},
        {"name": "Charlie", "power": "Zombie"},
        {"name": "Donnie", "power": "Warpish"},
        {"name": "Martin", "power": "Machine"}
        ], False)
    for player in sim.game.game_winners:
        winner_count[player.name] = winner_count.get(player.name, 0) + 1

# Print number of wins
# print(winner_count)

# Display winning percentages
for name in winner_count.keys():
    print(name + ": " + str(winner_count[name] * 100 / num_games_simulated))


'''
Explanation of Strategies:
default - play max card on offense, random card on defense
"def-neg" - play max card on offense, negotiate (if he/she has one) on defense

'''