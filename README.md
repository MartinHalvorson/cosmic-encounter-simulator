# Cosmic Encounter Simulator

(This is a relatively old project from about ~ 5 years ago)

This simulator models the game of Cosmic Encounter with various alien powers. I use heuristics and some basic AI to model rational player interactions.

### Rules of the Game

"In Cosmic Encounter, each player becomes the leader of one of dozens of alien races, each with its own unique power. On a player's turn, he or she becomes the offense. The offense encounters another player on a planet by moving a group of his or her ships through the hyperspace gate to that planet. Both sides can invite allies and play cards to try and tip the encounter in their favor. The object of the game is to establish colonies in other players' planetary systems. The winner(s) are the first player(s) to have five colonies on any planets outside his or her home system. These colonies may all be in one system or scattered over multiple systems." - [Board Game Geek](https://boardgamegeek.com/boardgame/39463/cosmic-encounter)

[Additional Game Rules](https://images-cdn.fantasyflightgames.com/filer_public/11/c6/11c61988-bb60-428f-b614-9c3a952f070b/cosmic-encounter-rulebook.pdf)

## Results


![](https://github.com/14mthalvorson/cosmic-encounter-simulator/blob/master/table.png)

###### _Note: This table just shows win rates. The absolute power is proportional to the win rate adjusted for the number of players in the game. (Individual player win rates will generally go down the more players in the game.)_

This table shows how the absolute strength of each power changes based on the number of players in the game. Generally speaking, powers with "main player" interactions decrease in strength with more players in the game. Powers with "all player" or "per turn" or "not main player" interactions grow in strength the more players in the game.

![](https://github.com/14mthalvorson/cosmic-encounter-simulator/blob/master/Percentage%20Wins%20vs%20Number%20of%20Players.png)
