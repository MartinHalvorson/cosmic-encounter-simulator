import random


class Simulator:
    def __init__(self, names):
        self.game = Game(names)


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

        self.colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]

        self.powers = ["Zombie", "Cudgel", "Machine", "None"]
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
            player.home_planets = [Planet(player.name, self.players) for i in range(5)]

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

        while not self.is_over:

        # Start turn phase
            self.phase = "Start Turn"
            print(self)

            if self.encounter == 1:
                self.offense = self.players[0] # If new offense for this encounter

            print("Offense: " + self.offense.name)

            input()
        # Destiny phase
            self.phase = "Destiny"
            print(self)

            # Draw next destiny card, assign defense
            self.defense = self.destiny_deck.draw().other # Should be of type Player
            while self.defense == self.offense:
                self.defense = self.destiny_deck.draw().other

            print("Offense: " + self.offense.name + "\nDefense: " + self.defense.name)

            input()
        # Launch phase
            self.phase = "Launch"
            print(self)


            input()
        # Alliance phase
            self.phase = "Alliance"
            print(self)


            input()
        # Planning phase
            self.phase = "Planning"
            print(self)

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

            print("Offense card: " + str(self.offense_card))
            print("Defense card: " + str(self.defense_card))

            input()
        # Resolution phase
            self.phase = "Resolution"
            print(self)

            offense_value = self.offense_card.value
            defense_value = self.defense_card.value

            if offense_value == 0 and defense_value == 0:
                # Colony swap
                self.winner = self.offense
                pass
            else:
                # Determines winner
                if offense_value > defense_value:
                    self.winner = self.offense
                else:
                    self.winner = self.defense

                # Compensation if one (and only one) side negotiated
                if offense_value == 0:
                    self.take_cards(self.offense, self.defense, 4)
                elif defense_value == 0:
                    self.take_cards(self.defense, self.offense, 4)

            # Prevent offense from going a third time or going again if they lost
            if self.encounter == 2 or self.winner == self.defense:
                self.players.append(self.players.pop(0))
                self.encounter = 1
            else:
                self.encounter = 2

            self.check_if_over()
            self.winner = None
            input()

    # Deals out eight cards to a player
    def deal_hand(self, player):
        for i in range(8):
            player.hand.append(self.draw_deck.draw())

    def check_if_over(self):
        for player in self.players:
            if len(player.foreign_colonies) == 5:
                self.is_over = True

    def take_cards(self, player1, player2, num_of_cards):
        for i in range(num_of_cards):
            if len(player2.hand) > 0:
                chosen_card = random.choice(player2.hand)
                player2.hand.remove(chosen_card)
                player1.hand.append(chosen_card)
                print(player1.name + " took " + player2.name + "'s " + str(chosen_card))

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

        # Everyone starts the game with five home planets; the total changes only in rare circumstances
        self.home_planets = []

        # Game finishes once a player or multiple players reach five foreign colonies
        self.foreign_colonies = []

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
    def __init__(self, name, players):
        self.ships = [name for i in range(5)]
        self.player_list = players

    # Used to add ships to a Planet
    def add_ship(self, ship):
        self.ships.append(ship)

    def __str__(self):
        result = "Planet: "
        for player in self.player_list:
            result += str(player.name) + " " + str(self.ships.count(player.name)) + "   "
        return result + "\n"



sim = Simulator(["Alvin", "Brady"])