import random


class Simulator:
    def __init__(self, names_dict):
        self.game = Game(names_dict)
        print(self.game.winners)


class Game:
    def __init__(self, names_dict):

        # Game variables

        # Draw and discard decks for main deck (encounter cards, flares, artifacts, ...)
        self.draw_deck = Deck("draw", False) # Final product will have this as True (draw_deck should be hidden)
        self.discard_deck = Deck("discard")

        # Shuffle all decks
        self.draw_deck.shuffle()
        self.discard_deck.shuffle()

        # Determines which player is "destined" to be attacked during the encounter
        self.destiny_deck = Deck("destiny", False)

        self.warp = [] # Where "dead" ships are stored
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
            # Creates new player with chosen name, color, power
            self.players.append(Player(person_dict["name"], color, power))

        # Randomize the order of play
        random.shuffle(self.players)

        # Now that there are players, fill the destiny deck with 10 cards per person
        for player in self.players:
            self.destiny_deck.cards += [Card("destiny", player.name, player) for i in range(8)]
        self.destiny_deck.shuffle()

        # Initialize each player with five home planets
        for player in self.players:
            self.planets += [Planet(player, self.players) for i in range(5)]

        # Deal each player a starting hand
        for player in self.players:
            self.deal_hand(player)

        # Control of flow variables
        self.phase = "start_turn"
        self.offense = None
        self.offense_card = None
        self.defense = None
        self.defense_card = None
        self.winner = None
        self.is_over = False
        self.encounter = 1
        self.ranking = []
        self.output = ""
        self.defense_planet = None

        # Sets home planets for each player
        for player in self.players:
            player.home_planets = self.home_planets(player)

        while not self.is_over:
            self.output = ""
            input("New Encounter")

        # Start turn phase
            self.set_ranking()

            self.phase = "Start Turn"
            print(self)
            print("Phase: " + self.phase + "\n")

            if self.encounter == 1:
                self.offense = self.players[0] # If new offense for this encounter

            # Fanciest line of code in whole program
            # Takes a list of tuples (player, num_of_foreign_colonies) and converts it to a string output
            self.output += "Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking])

            self.output += "\n\nOffense: " + self.offense.name + "\n"
            print(self.output)

            input()
        # Destiny phase
            self.phase = "Destiny"
            print(self)
            print("Phase: " + self.phase + "\n")

            # Draw next destiny card, assign defense
            self.defense = self.destiny_deck.draw(self.discard_deck).other # Should be of type Player
            while self.defense == self.offense:
                self.defense = self.destiny_deck.draw(self.discard_deck).other

            self.output += "Defense: " + self.defense.name + "\n\n"
            print(self.output)

            input()

        # Launch phase
            self.phase = "Launch"
            print(self)
            print("Phase: " + self.phase + "\n")

            self.defense_planet = random.choice(self.home_planets(self.defense))

            # Offense cannot already have ships there
            while self.defense_planet.ships.get(self.offense.name, 0) != 0:
                self.defense_planet = random.choice(self.home_planets(self.defense))

            # Ships offense is sending into the encounter
            offense_ships_chosen = 3
            self.offense_ships = {self.offense.name: offense_ships_chosen}

            # Remove ships from offense's home planets
            for i in range(offense_ships_chosen):
                planet = random.choice(self.home_planets(self.offense))
                if planet.ships.get(self.offense.name, 0) > 1:
                    planet.ships[self.offense.name] -= 1
                else:
                    i -= 1

            # Ships defense is sending into the encounter
            self.defense_ships = {self.defense.name: self.defense_planet.ships.get(self.defense.name, 0)}

            self.output += "Defense " + str(self.defense_planet) + "\n"
            self.output += "Offense ships: " + str(self.offense_ships.get(self.offense.name, 0)) + "\n"
            self.output += "Defense ships: " + str(self.defense_ships.get(self.defense.name, 0)) + "\n\n"
            print(self.output)

            input()
        # Alliance phase
            self.phase = "Alliance"
            print(self)

            # Fill in invited logic
            self.offense_allies = []
            self.defense_allies = []

            # Determines and prints offense invites
            self.output += "Offense invites:\n"
            if self.offense_allies == []:
                self.output += "\t<No one invited>\n"
            else:
                for invitee in self.offense_allies:
                    self.output += invitee.name + "\n"

            # Determines and prints defense invites
            self.output += "\nDefense invites:\n "
            if self.defense_allies == []:
                self.output += "\t<No one invited>\n"
            else:
                for invitee in self.defense_allies:
                    self.output += invitee.name + "\n"
            self.output += "\n"

            # Determines and prints which players join which side
            for player in self.players:
                if player != self.offense and player != self.defense:
                    if player in self.offense_allies:
                        self.output += player.name + " joins the offense!\n"
                        if player in self.defense_allies:
                            self.defense_allies.remove(player)
                    elif player in self.defense_allies:
                        self.output += player.name + " joins the defense!\n"
                        if player in self.offense_allies:
                            self.offense_allies.remove(player)
                    else:
                        self.output += player.name + " doesn't join either side.\n"

            print("Phase: " + self.phase + "\n")
            print(self.output)

            input()
        # Planning phase
            self.phase = "Planning"
            print(self)

            # Provides new hand for offense if he/she needs one
            if len(self.offense.hand) == 0:
                self.deal_hand(self.offense)
                self.output += self.offense.name + " draws a new hand."

            # Randomly select card for offense
            self.offense_card = random.choice(self.offense.hand)
            self.offense.hand.remove(self.offense_card)

            # Provides new hand for defense if he/she needs one
            if len(self.defense.hand) == 0:
                self.deal_hand(self.defense)
                self.output += self.defense.name + " draws a new hand."

            # Randomly select card for defense
            self.defense_card = random.choice(self.defense.hand)
            self.defense.hand.remove(self.defense_card)

            print("Phase: " + self.phase + "\n")
            print(self.output)

            input()
        # Reveal phase
            self.phase = "Reveal"

            print(self)

            self.output += "\nOffense card: " + str(self.offense_card)
            self.output += "Defense card: " + str(self.defense_card) + "\n"

            print("Phase: " + self.phase + "\n")
            print(self.output)

            input()
        # Resolution phase
            self.phase = "Resolution"
            print(self)
            self.set_ranking()

            offense_value = self.offense_card.value
            defense_value = self.defense_card.value

            # Both drop negotiates
            if offense_value == 0 and defense_value == 0:
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)

                # Add defensive ships to one of offense's home planets
                new_planet_for_defense = random.choice(self.offense)
                while new_planet_for_defense.ships.get(self.defense.name, 0) != 0:
                    new_planet_for_defense = random.choice(self.offense.home_planets)

                new_planet_for_defense.ships[self.defense.name] = self.defense_ships.get(self.defense.name, 0)

                self.output += "Colony swap occurred.\n"

                self.winner = self.offense
                pass

            # Offense dropped negotiate
            elif offense_value == 0:
                # Offense gets cards from defense
                self.take_cards(self.offense, self.defense, self.offense_ships.get(self.offense.name, 0))
                self.output += "\nDefense wins, offense draws cards.\n"

            # Defense dropped negotiate
            elif defense_value == 0:
                # Add offense's ships
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)
                self.defense_planet.ships[self.defense.name] = 0

                # Defense gets cards from offense
                self.take_cards(self.defense, self.offense, self.defense_ships.get(self.defense.name, 0))
                self.output += "\nOffense wins and lands on the colony. Defense draws cards.\n"

            # Both drop attack cards
            else:
                # Add in value of ships
                offense_value += sum(self.offense_ships.values())
                defense_value += sum(self.defense_ships.values())

                # Add some option for reinforcements later

                # Determines winner
                if offense_value > defense_value:
                    self.output += "Offense wins and lands on the colony.\n"
                    self.winner = self.offense
                    self.defense_planet.ships[self.defense.name] = 0
                    for player in self.offense_ships:
                        self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense.name, 0)
                else:
                    self.output += "Defense wins.\n"
                    self.winner = self.defense

            # Prevent offense from going a third time or going again if they lost
            if self.encounter == 2 or self.winner == self.defense:
                self.players.append(self.players.pop(0))
                self.encounter = 1
            else:
                self.encounter = 2

            if self.encounter == 2:
                self.output += "Offense elects for another encounter."

            # Updates planet list for each player if any were changed
            for player in self.players:
                player.home_planets = self.home_planets(player)

            print("Phase: " + self.phase + "\n")
            print(self.output)

            self.check_if_over()
            self.winner = None
            input()

        # Game Over, Determining winners
        self.winners = []
        for player in self.players:
            if self.num_of_foreign_colonies(player) == 5:
                self.winners.append(player)

    # Deals out eight cards to a player
    def deal_hand(self, player):
        for i in range(8):
            player.hand.append(self.draw_deck.draw(self.discard_deck))

    # Returns list of home planets of input player
    def home_planets(self, player):
        result = []
        for planet in self.planets:
            if planet.owner == player:
                result.append(planet)
        return result

    def check_if_over(self):
        for player in self.players:
            if self.num_of_foreign_colonies(player) == 5:
                self.is_over = True

    def take_cards(self, player1, player2, num_of_cards):
        for i in range(num_of_cards):
            if len(player2.hand) > 0:
                chosen_card = random.choice(player2.hand)
                player2.hand.remove(chosen_card)
                player1.hand.append(chosen_card)
                self.output += player1.name + " took " + player2.name + "'s " + str(chosen_card)

    def take_ships(self, player, num_of_ships):
        for i in range(num_of_ships):
            planet = random.choice(player.home_planets)
            for occupier in planet:
                if occupier[0] == player.name:
                    if occupier[1] > 1:
                        occupier = (player.name, occupier[1] - 1)
                        i += 1
            i -= 1

    def num_of_foreign_colonies(self, player):
        count = 0
        for planet in self.planets:
            if (planet.owner != player) and (planet.ships.get(player.name, 0) != 0):
                count += 1
        return count

    def set_ranking(self):
        self.ranking = [(player.name, self.num_of_foreign_colonies(player)) for player in self.players]
        self.ranking.sort(key = lambda x: x[1], reverse = True)

    def __str__(self):
        result = "Phase: " + self.phase + "\n"
        for player in self.players:
            result += str(player)
        result += str(self.draw_deck)
        result += str(self.discard_deck)
        result += str(self.destiny_deck)
        return result


class Player:
    def __init__(self, name, color, power, hidden = False):

        # List of the cards the player contains in his/her hand
        self.hand = []

        self.name = name
        self.color = color
        self.power = power
        self.hidden = hidden # Used to hide opponent's hand

        # Game finishes once a player or multiple players reach five foreign colonies
        self.home_planets = []

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
    def __init__(self, type = "none", hidden = False):
        self.cards = []
        self.type = type
        self.hidden = hidden
        self.empty = True

        # Draw deck initialized with attack cards 0-19, 5 negotiates
        if type == "draw":
            self.empty = False
            self.cards += [Card("attack", i) for i in range(0, 30)]
            self.cards += [Card("attack", i) for i in range(0, 15)]
            self.cards += [Card("negotiate", 0) for i in range(0, 5)]

        if type == "destiny":
            self.empty = False

        # The discard deck will be initialized as empty

    # Removes first card in Deck and returns it
    def draw(self, discard_deck):
        if self.empty:
            self.cards = discard_deck.cards
            self.reshuffle()
            discard_deck.cards = []
        self.empty = len(self.cards) - 1 == 0
        return self.cards.pop()

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
            self = Deck("draw")
        elif self.type == "destiny":
            Game.initialize_destiny_deck()

    # Used for printing out the cards in the deck
    def __str__(self):

        # Give a title to the name of the return deck
        result = "Discard Deck:\n"
        if self.type == "draw":
            result = "Draw Deck:\n"
        elif self.type == "destiny":
            result = "Destiny Deck:\n"

        # Adds cards to return string if not hidden
        if self.empty:
            result += "\t<empty>\n"
        elif self.hidden:
            result += "\t<hidden>\n"
        else:
            count = 0
            for card in self.cards:
                count += 1
                num_cards_shown = 5
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

sim = Simulator([{"name": "Martin", "power": "None", "color": "Orange"},
                 {"name": "Alvin", "color": "Blue"},
                 {"name": "Brady", "color": "Blue"},
                 {"name": "Charlie"},
                 {"name": "Donnie"}])