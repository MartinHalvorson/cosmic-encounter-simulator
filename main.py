import Simulator

num_games_simulated = 1000
num_players = 5

names_list = ["Alvin", "Brady", "Charlie", "Daniel", "Ernie", "Freddie", "Gale", "Henry"]

sim = Simulator.Simulator(num_games_simulated,
    [{"name": names_list[i]} for i in range(num_players)],
        catch_errors=True,
        show_output=False)

# Display clock stats
print("\nTotal Time: " + str(round(sim.total_time, 2)) + " seconds")
print("Average Time: " + str(round(sim.average_time, 4)) + " seconds")
print("Number of Exceptions: " + str(sim.exceptions))
print("Average Wins: " + str(sim.average_wins))

# Display winning percentages for each player
print("\nPlayer Win Percentages:")
player_win_list = [(name, sim.player_wins.get(name, 0) / num_games_simulated) for name in sim.player_wins.keys()]
# Sort so winningest players are first
player_win_list.sort(key=lambda x: x[1], reverse=True)
for player_tuple in player_win_list:
    print(player_tuple[0] + ": " + str(round(100 * player_tuple[1], 1)))

# Display winning percentages for each power
print("\nAlien Power Win Percentages:")
power_win_list = []
for tuple in sim.power_count.items():
    power_win_list.append((tuple[0], sim.power_wins.get(tuple[0], 0) / tuple[1]))
# Sort so winningest alien powers are first
power_win_list.sort(key=lambda x: x[1], reverse=True)
for power_tuple in power_win_list:
    print(str(power_tuple[0]) + ": " + str(round(100 * power_tuple[1], 1)))