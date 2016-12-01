import Simulator

# Keeps track of total wins by each player
player_wins = {}

# Keeps track of total wins by each power
power_wins = {}

# Keeps track of total games played by each power
power_count = {}

num_games_simulated = 1000

for i in range(num_games_simulated):

    if False:  # Playing actual game mode
        sim = Simulator.Simulator([
            {"name": "Martin"},
            {"name": "Brady"},
            {"name": "Charlie"},
            {"name": "Donnie"},
            {"name": "Ernie"}
        ], True)
    if True:  # Debugging game mode
        sim = Simulator.Simulator([
            {"name": "Alvin", "power": "Parasite"},
            {"name": "Brady", "power": "Cudgel"},
            {"name": "Charlie", "power": "Kamikazee"},
            {"name": "Donnie", "power": "Tripler"},
            {"name": "Ernie", "power": "Symbiote"}
            ], True)
    if False:  # Simulation mode
        try:
            sim = Simulator.Simulator([
                {"name": "Alvin"},
                {"name": "Brady"},
                {"name": "Charlie"},
                {"name": "Donnie"},
                {"name": "Ernie"}
            ], False)
        except:
            i -= 1

        if i % 200 == 0:
            print(i)

    for player in sim.game.players:
        if player in sim.game.game_winners:
            player_wins[player.name] = player_wins.get(player.name, 0) + 1
            power_wins[player.power] = power_wins.get(player.power, 0) + 1
        power_count[player.power] = power_count.get(player.power, 0) + 1

# Display winning percentages for each player
print("Player Win Percentages:")
player_win_list = [(player.name, player_wins.get(player.name, 0) / num_games_simulated) for player in sim.game.players]
# Sort so winningest players are first
player_win_list.sort(key=lambda x: x[1], reverse=True)
for player_tuple in player_win_list:
    print(player_tuple[0] + ": " + str(round(100 * player_tuple[1], 1)))

# Display winning percentages for each power
print("\nAlien Power Win Percentages:")
power_win_list = []
for tuple in power_count.items():
    power_win_list.append((tuple[0], power_wins.get(tuple[0], 0) / tuple[1]))
# Sort so winningest alien powers are first
power_win_list.sort(key=lambda x: x[1], reverse=True)
for power_tuple in power_win_list:
    print(power_tuple[0] + ": " + str(round(100 * power_tuple[1], 1)))