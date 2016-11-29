import random


class Simulator:
    def __init__(self, names_dict, step_through = False):
        self.game = Game(names_dict, step_through)


class Game:
    def __init__(self, names_dict, step_through = False):

        # Simulation variables
        self.step_through = step_through

        # Game variables
        self.warp = {} # Where "dead" ships are stored
        self.planets = []

        self.colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black", "White", "Brown"]

        self.powers = ["Zombie", "Cudgel", "Machine", "Loser", "Filch", "Reserve", "Vulch", "Macron", "Virus", "Tripler", "Masochist", "Warpish", "Symbiote", "None"]
        # Add descriptions of alien powers later

        # Initializing players
        self.players = []
        for person_dict in names_dict: # names is a parameter in Game constructor

            color = person_dict.get("color", random.choice(self.colors)) # Chooses random color
            # Exception handling here can allow multiple people to be the same color
            try:
                self.colors.remove(color)
            except:
                pass

            power = person_dict.get("power", random.choice(self.powers)) # Chooses random power
            # Exception handling here can allow multiple people to be the same power
            try:
                self.powers.remove(power)
            except:
                pass
            strategy = person_dict.get("strategy", None)
            # Creates new player with chosen name, color, power
            self.players.append(Player(person_dict["name"], color, power, strategy))

        # Randomize the order of play
        random.shuffle(self.players)

        # self.players is ordered in the order of play (first on the list goes first)

        # Draw and discard decks for main deck (encounter cards, flares, artifacts, ...)
        self.discard_deck = Deck()
        self.draw_deck = Deck("draw", False, self.discard_deck)  # Final product will have this as True (draw_deck should be hidden)

        # Determines which player is "destined" to be attacked during the encounter
        self.destiny_discard_deck = Deck()
        self.destiny_draw_deck = Deck("destiny", False, self.destiny_discard_deck, self.players)

        # Determines which player is "destined" to be attacked during the encounter
        self.rewards_discard_deck = Deck()
        self.rewards_draw_deck = Deck("rewards", False, self.rewards_discard_deck, self.players)

        # Decks are automatically shuffled on creation

        # Initialize each player with five home planets
        for player in self.players:
            self.planets += [Planet(player, self.players) for i in range(5)]

        # Deal each player a starting hand
        for player in self.players:
            self.deal_hand(player)

        # Control of flow variables
        self.phase = "start_turn"

        # Will either be 1 or 2 (player may elect for a second encounter), resets on each turn
        self.encounter = 1

        self.offense = None
        self.offense_card = None
        self.defense = None
        self.defense_card = None
        self.defense_planet = None

        # An ordering of players based on number of foreign colonies (5 to win)
        self.ranking = {}
        self.ordered_ranking = []

        # Used to display to happenings of each encounter in the console
        self.output = ""

        # Used to determine if another encounter is allowed or if the game is over
        self.is_over = False
        self.game_winners = []

        # Used to set winner of encounter
        self.encounter_winner = None

        # Sets home planets for each player
        for player in self.players:
            player.home_planets = self.home_planets(player)

        # A little guidance for navigating the console
        if step_through:
            print("<Enter> to advance.\n")

        # This is the main while loop where an entire encounter is cycled through
        while not self.is_over:

            if step_through:
                self.output = ""

            self.encounter_winner = None

            if step_through:
                input("New Encounter")

        # Start Turn phase
            self.phase = "Start Turn"

            # Prints state of the game, which includes visible decks and players (their hands and planets)
            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            if self.encounter == 1:
                self.offense = self.players[0]  # Selects new offense for this encounter

            self.set_ranking()

            if step_through:
                self.output += "Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ordered_ranking])

                self.output += "\n\nOffense: " + self.offense.name + "\n"

                print(self.output)

                input()

        # Destiny phase
            self.phase = "Destiny"

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            # Draw next destiny card, assign defense
            self.destiny_card = self.destiny_draw_deck.draw()

            # If offense draws his/herself for a destiny (player to attack)
            while self.destiny_card.other == self.offense:

                # Discard card
                self.destiny_discard_deck.discard(self.destiny_card)

                # and redraw until they don't draw his/herself
                self.destiny_card = self.destiny_draw_deck.draw()

            # Assign the defense
            self.defense = self.destiny_card.other

            # Put destiny card in destiny discard deck
            self.destiny_discard_deck.discard(self.destiny_card)

            if step_through:
                self.output += "Defense: " + self.defense.name + "\n\n"
                print(self.output)

                input()

        # Launch phase
            self.phase = "Launch"

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            # May change this later to select the most advantageous planet for the offense to attack
            self.defense_planet = random.choice(self.home_planets(self.defense))

            # Rechoose planet if offense already has ships there
            while self.defense_planet.ships.get(self.offense.name, 0) != 0:
                self.defense_planet = random.choice(self.home_planets(self.defense))

            # Ships offense is sending into the encounter
            offense_ships_chosen = 3

            if self.offense.power == "Zombie":
                offense_ships_chosen = 4

            self.offense_ships = {self.offense.name: offense_ships_chosen}

            self.take_ships(self.offense, offense_ships_chosen)

            # Ships defense is sending into the encounter
            self.defense_ships = {self.defense.name: self.defense_planet.ships.get(self.defense.name, 0)}

            # In the event of the defense losing, defense ships will be removed in the resolution stage

            if step_through:
                self.output += "Defense " + str(self.defense_planet) + "\n"
                self.output += "Offense ships: " + str(self.offense_ships.get(self.offense.name, 0)) + "\n"
                self.output += "Defense ships: " + str(self.defense_ships.get(self.defense.name, 0)) + "\n\n"
                print(self.output)

                input()

        # Alliance phase
            self.phase = "Alliance"

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            self.offense_allies = []
            self.defense_allies = []

            # Offense logically invites anyone equal or less than them

            offense_num_planets = self.ranking.get(self.offense.name, 0)
            for player in self.players:
                if player is not self.offense and player is not self.defense:
                    if self.ranking.get(player.name, 0) <= offense_num_planets:
                        self.offense_allies.append(player)

            # Defense invites are random for now
            for player in self.players:
                if player is not self.offense and player is not self.defense:
                    if random.randint(0, 1) == 1:
                        self.defense_allies.append(player)

            # Determines and prints offensive invitees
            if step_through:
                self.output += "Offense invites:\n"
                if self.offense_allies is []:
                    self.output += "\t<No one invited>\n"
                else:
                    for invitee in self.offense_allies:
                        self.output += invitee.name + "\n"

            # Determines and prints defensive invitees
            if step_through:
                self.output += "\nDefense invites:\n"
                if self.defense_allies is []:
                    self.output += "\t<No one invited>\n"
                else:
                    for invitee in self.defense_allies:
                        self.output += invitee.name + "\n"

                self.output += "\n"

            # Determines and prints which players join which side
            for player in self.players:
                if player != self.offense and player != self.defense:
                    if player in self.offense_allies:
                        if step_through:
                            self.output += player.name + " joins the offense!\n"
                        if player in self.defense_allies:
                            self.defense_allies.remove(player)
                    elif player in self.defense_allies:
                        if step_through:
                            self.output += player.name + " joins the defense!\n"
                        if player in self.offense_allies:
                            self.offense_allies.remove(player)
                    else:
                        if step_through:
                            self.output += player.name + " doesn't join either side.\n"

            # Add in ships for allies
            for player in self.players:
                if player in self.offense_allies:
                    self.take_ships(player, 2)
                    self.offense_ships[player.name] = 2
                if player in self.defense_allies:
                    self.take_ships(player, 2)
                    self.defense_ships[player.name] = 2

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

                print(self.output)

                input()

        # Planning phase
            self.phase = "Planning"

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            # Provides new hand for offense if he/she needs one
            if len(self.offense.hand) == 0 or not self.offense.has_encounter_card():
                self.deal_hand(self.offense)
                if step_through:
                    self.output += "\n" + self.offense.name + " draws a new hand.\n"

            # Select max value card for offense
            self.offense_card = self.select_offense_encounter_card()

            # Provides new hand for defense if he/she needs one
            if len(self.defense.hand) == 0 or not self.defense.has_encounter_card():
                self.deal_hand(self.defense)
                if step_through:
                    self.output += "\n" + self.defense.name + " draws a new hand.\n"

            self.defense_card = self.select_defense_encounter_card()

            if step_through:
                print(self.output)

                input()

        # Reveal phase
            self.phase = "Reveal"

            if step_through:
                print(self)

                self.output += "\nOffense card: " + str(self.offense_card)
                self.output += "Defense card: " + str(self.defense_card) + "\n"

                print("Phase: " + self.phase + "\n")
                print(self.output)

                input()

        # Resolution phase
            self.phase = "Resolution"

            if step_through:
                print(self)
                print("Phase: " + self.phase + "\n")

            offense_value = self.offense_card.value
            defense_value = self.defense_card.value

            # Both drop negotiates
            if offense_value == 0 and defense_value == 0:
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)

                # Add defensive ships to one of offense's home planets
                new_planet_for_defense = random.choice(self.offense.home_planets)
                while new_planet_for_defense.ships.get(self.defense.name, 0) != 0:
                    new_planet_for_defense = random.choice(self.offense.home_planets)

                new_planet_for_defense.ships[self.defense.name] = self.defense_ships.get(self.defense.name, 0)

                if step_through:
                    self.output += "Colony swap occurred.\n"

                self.encounter_winner = self.offense
                pass

            # Offense dropped negotiate
            elif offense_value == 0:
                # Offense gets cards from defense
                self.take_cards(self.offense, self.defense, self.offense_ships.get(self.offense.name, 0))
                self.warp[self.offense.name] = self.warp.get(self.offense.name, 0) + self.offense_ships.get(self.offense.name, 0)
                if step_through:
                    self.output += "\nDefense wins, offense draws cards.\n"
                self.encounter_winner = self.defense

            # Defense dropped negotiate
            elif defense_value == 0:
                # Add offense's ships
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)
                self.defense_planet.ships[self.defense.name] = 0
                self.encounter_winner = self.offense
                self.warp[self.defense.name] = self.warp.get(self.defense.name, 0) + self.defense_ships.get(self.defense.name, 0)


                # Defense gets cards from offense
                self.take_cards(self.defense, self.offense, self.defense_ships.get(self.defense.name, 0))
                if step_through:
                    self.output += "\nOffense wins and lands on the colony. Defense draws cards.\n"

            # Both drop attack cards
            else:
                # Add in value of ships
                offense_value += sum(self.offense_ships.values())
                defense_value += sum(self.defense_ships.values())

                if self.offense.power == "Warpish":
                    offense_value += sum(self.warp.values())

                if self.defense.power == "Warpish":
                    defense_value += sum(self.warp.values())

                # Add some option for reinforcements later

                # Determines encounter winner
                if offense_value > defense_value:
                    if step_through:
                        self.output += "Offense wins and lands on the colony.\n"
                    self.encounter_winner = self.offense
                    self.defense_planet.ships[self.defense.name] = 0
                    self.warp[self.defense.name] = self.warp.get(self.defense.name, 0) + self.defense_ships.get(self.defense.name, 0)

                    for player in self.offense_ships:
                        self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)
                else:
                    if step_through:
                        self.output += "Defense wins.\n"
                    self.warp[self.offense.name] = self.warp.get(self.offense.name, 0) + self.offense_ships.get(self.offense.name, 0)
                    self.encounter_winner = self.defense

            for player in self.players:
                if player.power == "Zombie":
                    self.return_ships(player, self.warp.get(player.name, 0))
                    self.warp[player.name] = 0

            # Prevent offense from going a third time or going again if they lost
            if ((self.encounter == 1 and self.encounter_winner == self.offense) or self.offense.power == "Machine") and self.offense.has_encounter_card():
                self.encounter = 2
            else:
                self.players.append(self.players.pop(0))
                self.encounter = 1

            # Offense may elect for second encounter if both victorious on first and he/she has another encounter card
            if self.encounter == 2:
                if step_through:
                    self.output += "Offense elects for another encounter."

            # Updates planet list for each player if any were changed
            for player in self.players:
                player.home_planets = self.home_planets(player)

            if step_through:
                print(self.output)

            # Adds encounter cards to discard pile
            self.discard_deck.cards.append(self.offense_card)
            self.discard_deck.cards.append(self.defense_card)

            self.check_if_over()

            if step_through:
                input()

        # Game Over, determining winners
        for player in self.players:
            if self.num_of_foreign_colonies(player) == 5:
                self.game_winners.append(player)

        # If player won without reaching five colonies, he/she may have already been added to winners

    # Deals out eight cards to a player
    def deal_hand(self, player):
        for i in range(8):
            player.hand.append(self.draw_deck.draw())

    # Removes num_of_cards from player1 and gives them to player2
    def take_cards(self, player1, player2, num_of_cards):
        for i in range(num_of_cards):
            if len(player2.hand) > 0:
                chosen_card = random.choice(player2.hand)
                player2.hand.remove(chosen_card)
                player1.hand.append(chosen_card)
                self.output += player1.name + " took " + player2.name + "'s " + str(chosen_card)

    def select_offense_encounter_card(self):

        # Throw exception if offense doesn't have encounter card
        if not self.offense.has_encounter_card:
            raise Exception("Offense doesn't have encounter card.")

        return_card = None

        for card in self.offense.hand:
            if return_card is None and card.is_encounter_card():
                return_card = card

            # Makes sure reinforcement is not selected as encounter card
            if card.is_encounter_card() and card.value > return_card.value:
                    return_card = card

        self.offense.hand.remove(return_card)
        return return_card

    def select_defense_encounter_card(self):

        # Throw exception if defense doesn't have encounter card
        if not self.defense.has_encounter_card():
            raise Exception("Defense doesn't have encounter card.")

        return_card = None

        # "def-neg" strategy is to play a negotiate as defense to obtain more cards
        if self.defense.strategy == "def-neg":
            # Select a negotiate if there is one
            for card in self.defense.hand:
                if return_card is None and card.is_encounter_card():
                    return_card = card
                if card.type == "negotiate":
                    return_card = card

        else:
            # Randomly select card for defense
            while return_card is None:
                card = random.choice(self.defense.hand)
                if card.is_encounter_card():
                    return_card = card

        try:
            self.defense.hand.remove(return_card)
        except:
            raise Exception("Cannot remove card from defense's hand.")
        return return_card

    def check_if_over(self):
        for player in self.players:
            if self.num_of_foreign_colonies(player) == 5:
                self.is_over = True

    def take_ships(self, player, num_ships):
        # Remove appropriate number of ships from offense's (home) planets
        for i in range(num_ships):
            planet = random.choice(self.home_planets(player))
            if planet.ships.get(player.name, 0) > 1:
                planet.ships[player.name] -= 1
            else:
                i -= 1

    def return_ships(self, player, num_ships):
        for i in range(num_ships):
            planet = random.choice(player.home_planets)
            if planet.ships.get(player.name, 0) > 0:
                planet.ships[player.name] = planet.ships[player.name] + 1
            else:
                i -= 1

                # Returns list of home planets of input player
                def home_planets(self, player):
                    result = []
                    for planet in self.planets:
                        if planet.owner == player:
                            result.append(planet)
                    return result

    # Returns list of home planets of input player
    def home_planets(self, player):
        result = []
        for planet in self.planets:
            if planet.owner == player:
                result.append(planet)
        return result

    # Counts number of foreign colonies a player has
    def num_of_foreign_colonies(self, player):
        count = 0
        for planet in self.planets:
            if (planet.owner != player) and (planet.ships.get(player.name, 0) != 0):
                count += 1
        return count

    def set_ranking(self):
        # Fanciest lines of code in whole project
        # Takes a list of tuples (player, num_of_foreign_colonies) and converts it to a string output
        self.ordered_ranking = [(player.name, self.num_of_foreign_colonies(player)) for player in self.players]
        self.ordered_ranking.sort(key = lambda x: x[1], reverse = True)
        for pair in self.ordered_ranking:
            self.ranking[pair[0]] = pair[1]

    def __str__(self):
        result = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        result += "Phase: " + self.phase + "\n"
        result += "Warp:\n"
        for player in self.players:
            result += str(player.name) + ": " + str(self.warp.get(player.name, 0)) + "\n"
        # Add each player to the output
        for player in self.players:
            result += str(player)

        # Add decks to output
        result += str(self.draw_deck)
        result += str(self.discard_deck)
        result += str(self.rewards_draw_deck)
        result += str(self.rewards_discard_deck)
        result += str(self.destiny_draw_deck)

        return result


class Player:
    def __init__(self, name, color, power, strategy, hidden = False):

        # List of the cards the player contains in his/her hand
        self.hand = []

        self.name = name
        self.color = color
        self.power = power
        self.strategy = strategy
        self.hidden = hidden # Used to hide opponent's hand

        # Once powers become a thing, add rule to update after attack if players still have their powers
        self.power_active = True

        # Game finishes once a player or multiple players reach five foreign colonies
        self.home_planets = []

    def has_encounter_card(self):
        for card in self.hand:
            if card.is_encounter_card():
                return True
        return False

    # Used for printing out a player
    def __str__(self):
        result = "Player: " + self.name + " \t" + self.power + " \t" + self.color + "\n"

        # Adds Player's planets to result
        for planet in self.home_planets:
            result += "\t\t" + str(planet)

        # Adds Player's hand to result
        result += "\tHand: (" + str(len(self.hand)) + " cards)\n"

        # Depending on who's playing, hand may be hidden
        if self.hidden:
            result += "\t<hidden>"
        else:
            if len(self.hand) == 0:
                result += "\t\t<empty>\n"
            else:
                for card in self.hand:
                    result += "\t\t" + str(card)
        return result + "\n"


class Deck:
    def __init__(self, type = "none", hidden = False, discard_deck = None, other = None):
        self.cards = []
        self.type = type
        self.hidden = hidden
        self.empty = True
        self.discard_deck = discard_deck

        # Draw deck will be initialized with attack, negotiate, and reinforcement cards
        if type == "draw":
            self.empty = False
            self.cards += [Card("attack", i) for i in range(0, 30)]
            self.cards += [Card("attack", i) for i in range(0, 15)]
            self.cards += [Card("negotiate", 0) for i in range(0, 10)]
            self.cards += [Card("reinforcement", i) for i in range(2, 5)]
            self.cards += [Card("reinforcement", i) for i in range(2, 5)]
            self.cards += [Card("artifact", "cosmic zap") for i in range(2)]
            self.cards += [Card("artifact", "card zap") for i in range(2)]
            self.cards += [Card("artifact", "mobius tubes") for i in range(2)]
            self.cards += [Card("artifact", "emotion control") for i in range(2)]
            self.cards.append(Card("artifact", "force field"))
            self.cards.append(Card("artifact", "quash"))

        # Defender rewards deck
        if type == "rewards":
            self.empty = False
            self.cards += [Card("attack", i) for i in range(20, 30)]
            self.cards += [Card("attack", i) for i in range(20, 30)]
            self.cards += [Card("negotiate", 0) for i in range(0, 4)] # Change to special negotiates later
            self.cards += [Card("reinforcement", i) for i in range(5, 8)]
            self.cards += [Card("reinforcement", i) for i in range(5, 8)]
            self.cards += [Card("kicker", i) for i in range(-1, 5)]
            self.cards.append(Card("artifact", "cosmic zap"))
            self.cards.append(Card("artifact", "card zap"))
            self.cards.append(Card("artifact", "omni-zap"))
            self.cards.append(Card("artifact", "solar wind"))
            self.cards.append(Card("artifact", "rebirth"))
            self.cards.append(Card("artifact", "ship zap"))
            self.cards.append(Card("artifact", "hand zap"))
            #self.cards.append(Card("artifact", "finder"))
            self.cards.append(Card("artifact", "space junk"))
            self.cards.append(Card("artifact", "victory boon"))

        # Destiny decks will have five cards of each player, should be initialized with other = list of players in game
        if type == "destiny":
            self.empty = False

            players = other
            for player in players:
                self.cards += [Card("destiny", player.name, player) for i in range(3)]

        self.shuffle()

        # The discard decks will be initialized as empty

    # Removes first card in Deck and returns it
    def draw(self):
        # Replenish deck if empty
        if self.empty:
            self.reshuffle()

        # At this point, deck should not be empty
        self.empty = len(self.cards) - 1 == 0
        return self.cards.pop(0)

    # Accepts card and adds it to the top of the deck
    def discard(self, card):
        self.empty = False
        self.cards.insert(0, card)

    # Random shuffle
    def shuffle(self):
        if not self.empty:
            random.shuffle(self.cards)

    # Discarded cards are added back in and shuffled
    def reshuffle(self):
        empty = False

        if self.type == "draw":
            self.cards = self.discard_deck.cards
            self.discard_deck.cards = []

        elif self.type == "destiny":
            self.cards = self.discard_deck.cards
            self.discard_deck.cards = []

        self.shuffle()

    # Used for printing out the cards in the deck
    def __str__(self):

        # Give a title to the name of the return deck
        result = "Discard Deck:\n"
        if self.type == "draw":
            result = "Draw Deck:\n"
        elif self.type == "destiny":
            result = "Destiny Deck:\n"
        elif self.type == "rewards":
            result = "Rewards Deck:\n"

        # Adds cards to return string if not hidden
        if self.empty:
            result += "\t<empty>\n"
        elif self.hidden:
            result += "\t<hidden>\n"
        else:
            count = 0
            for card in self.cards:
                count += 1
                num_cards_shown = 3
                result += "\t" + str(card)
                if count == num_cards_shown and (len(self.cards) > num_cards_shown):
                    result += "\t<plus " + str(len(self.cards) - num_cards_shown) + " more>\n"
                    break
        return result + "\n"


class Card:
    def __init__(self, type, value, other = "None"):
        self.type = type
        self.value = value
        self.other = other

    def is_encounter_card(self):
        return self.type == "negotiate" or self.type == "attack"

    # Used for printing out the type of card
    def __str__(self):
        return self.type + " ~ " + str(self.value) + "\n"


class Planet:
    def __init__(self, player, players):
        self.ships = {player.name: 4}
        self.owner = player
        self.players = players

    def __str__(self):
        result = "Planet: "
        for player in self.players:
            if self.ships.get(player.name, 0) != 0:
                result += str(player.name) + " " + str(self.ships[player.name]) + "   "
        return result + "\n"
