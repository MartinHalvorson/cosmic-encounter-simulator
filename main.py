import random


class Simulator:
    def __init__(self, names):
        self.game = Game(names)
        print(self.game.winners)


class Game:
    def __init__(self, names):

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

        self.colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]

        self.powers = ["Zombie", "Cudgel", "Machine", "Loser", "Filch", "Reserve", "Vulch", "Macron", "Virus", "Tripler", "Masochist", "Warpish", "Symbiote", "None"]
        # Add descriptions of alien powers later

        # Initializing players
        self.players = []
        for name in names: # names is a parameter in Game constructor
            color = random.choice(self.colors) # Chooses random color
            self.colors.remove(color)
            power = random.choice(self.powers) # Chooses random power
            self.powers.remove(power)
            # Creates new player with chosen name, color, power
            self.players.append(Player(name, color, power))

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

        # Sets home planets for each player
        for player in self.players:
            player.home_planets = self.home_planets(player)

        while not self.is_over:
            input("New Encounter")

        # Start turn phase
            self.set_ranking()

            self.phase = "Start Turn"
            print(self)

            if self.encounter == 1:
                self.offense = self.players[0] # If new offense for this encounter

            # Fanciest line of code in whole program
            # Takes a list of tuples (player, num_of_foreign_colonies) and converts it to a string output
            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")
            print("Offense: " + self.offense.name)

            input()
        # Destiny phase
            self.phase = "Destiny"
            print(self)

            # Draw next destiny card, assign defense
            self.defense = self.destiny_deck.draw().other # Should be of type Player
            while self.defense == self.offense:
                self.defense = self.destiny_deck.draw().other

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")
            print("Offense: " + self.offense.name + "\nDefense: " + self.defense.name)

            input()
        # Launch phase
            self.phase = "Launch"

            self.defense_planet = random.choice(self.home_planets(self.defense))

            # Offense cannot already have ships there
            while self.defense_planet.ships.get(self.offense.name, 0) != 0:
                self.defense_planet = random.choice(self.home_planets(self.defense))

            # Ships offense is sending into the encounter
            self.offense_ships = {self.offense.name: 3}

            # Ships defense is sending into the encounter
            self.defense_ships = {self.defense.name: self.defense_planet.ships.get(self.defense.name, 0)}

            print(self)

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")

            print("Defense " + str(self.defense_planet))
            print("Offense ships: " + str(self.offense_ships.get(self.offense.name, 0)))
            print("Defense ships: " + str(self.defense_ships.get(self.defense.name, 0)))

            input()
        # Alliance phase
            self.phase = "Alliance"

            # Fill in invited logic
            self.offense_allies = []
            self.defense_allies = []

            print(self)

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")

            # Determines and prints offense invites
            print("Offense invites: ")
            if self.offense_allies == []:
                print("\t<No one invited>")
            else:
                for invitee in self.offense_allies:
                    print(invitee.name)

            # Determines and prints defense invites
            print("\nDefense invites: ")
            if self.defense_allies == []:
                print("\t<No one invited>")
            else:
                for invitee in self.defense_allies:
                    print(invitee.name)

            # Determines and prints which players join which side
            for player in self.players:
                if player != self.offense and player != self.defense:
                    if self.offense_allies.contains(player):
                        print(player.name + " joins the offense!")
                        if player in self.defense_allies:
                            self.defense_allies.remove(player)
                    elif self.defense_allies.contains(player):
                        print(player.name + " joins the defense!")
                        if player in self.offense_allies:
                            self.offense_allies.remove(player)
                    else:
                        print(player.name + " doesn't join either side.")


            input()
        # Planning phase
            self.phase = "Planning"

            print(self)

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")


            # Randomly select card for offense
            self.offense_card = random.choice(self.offense.hand)
            self.offense.hand.remove(self.offense_card)

            # Randomly select card for defense
            self.defense_card = random.choice(self.defense.hand)
            self.defense.hand.remove(self.defense_card)


            input()
        # Reveal phase
            self.phase = "Reveal"

            print(self)

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")

            print("Offense card: " + str(self.offense_card) + "Defense card: " + str(self.defense_card))

            input()
        # Resolution phase
            self.phase = "Resolution"
            print(self)

            print("Rankings: " + "   ".join([str(rankee[0]) + ": " + str(rankee[1]) for rankee in self.ranking]))
            print("Phase: " + self.phase + "\n")

            offense_value = self.offense_card.value
            defense_value = self.defense_card.value

            if offense_value == 0 and defense_value == 0:
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense, 0)

                # Add defensive ships to one of offense's home planets
                new_planet_for_defense = random.choice(self.offense)
                while new_planet_for_defense.ships.get(self.defense.name, 0) == 0:
                    new_planet_for_defense = random.choice(self.offense)

                new_planet_for_defense.ships[self.defense.name] = self.defense_ships.get(self.defense, 0)

                self.winner = self.offense
                pass

            # Offense dropped negotiate
            elif offense_value == 0:
                self.take_cards(self.offense, self.defense, self.offense_ships)

            # Defense dropped negotiate
            elif defense_value == 0:
                self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense, 0)
                self.take_cards(self.defense, self.offense, self.defense_ships.get(self.defense, 0))
            else:
                offense_value += sum(self.offense_ships.values())
                defense_value += sum(self.defense_ships.values())

                # Determines winner
                if offense_value > defense_value:
                    self.winner = self.offense
                    for player in self.offense_ships:
                        self.defense_planet.ships[self.offense.name] = self.offense_ships.get(self.offense, 0)
                else:
                    self.winner = self.defense

            # Prevent offense from going a third time or going again if they lost
            if self.encounter == 2 or self.winner == self.defense:
                self.players.append(self.players.pop(0))
                self.encounter = 1
            else:
                self.encounter = 2

            # Resets home planets for each player if any were changed
            for player in self.players:
                player.home_planets = self.home_planets(player)

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
            player.hand.append(self.draw_deck.draw())

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
                print(player1.name + " took " + player2.name + "'s " + str(chosen_card))

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
        for planet in self.home_planets:
            result += "\t\t" + str(planet)
        result += "\tHand:\n"
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
            self.cards += [Card("attack", i) for i in range(0, 20)]
            self.cards += [Card("negotiate", 0) for i in range(0, 5)]

        if type == "destiny":
            self.empty = False

        # The discard deck will be initialized as empty

    # Removes first card in Deck and returns it
    def draw(self):
        if self.empty:
            self.reshuffle()
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

    # Used to add ships to a Planet
    def add_ship(self, player, num_of_ships):
        self.ships[player.name] = self.ships.get(player.name, 0) + num_of_ships

    def __str__(self):
        result = "Planet: "
        for player in self.players:
            if self.ships.get(player.name, 0) != 0:
                result += str(player.name) + " " + str(self.ships[player.name]) + "   "
        return result + "\n"



sim = Simulator(["Alvin", "Brady"])