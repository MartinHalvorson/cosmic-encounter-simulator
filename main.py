import random


class Simulator:
    def __init__(self, names):
        self.game = Game(names)


class Game:
    def __init__(self, names):
        self.draw_deck = Deck("draw", False) # Final product will have this as True (draw_deck should be hidden)
        self.discard_deck = Deck("discard")
        self.destiny_deck = Deck("destiny", False)
        self.colors = ["red", "orange", "yellow", "green", "blue", "purple"]

        # Used to dictate order of play during an encounter
        self.phase = "start_turn"

        self.powers = ["Zombie", "Cudgel", "Machine", "None"]
        # Zombie - doesn't lose ships to the warp
        # Cudgel - if victorious, forces the losing side to lose as many ships as cudgel sent (in addition)

        self.players = []
        self.offense = None
        self.defense = None

        # Initializing players
        for name in names:
            color = random.choice(self.colors)
            self.colors.remove(color)
            power = random.choice(self.powers)
            self.powers.remove(power)
            self.players.append(Player(name, color, power))

        # Randomize the order of play
        random.shuffle(self.players)

        # Initialize each player with five home planets
        for player in self.players:
            player.home_planets = [Planet(player.name, self.players) for i in range(5)]

        # Essentially where "dead" ships are stored
        self.warp = []

        # Shuffle the draw deck
        self.draw_deck.shuffle()

        # Shuffle the destiny deck
        self.destiny_deck.shuffle()

        # Deal each player a starting hand
        for player in self.players:
            self.deal_hand(player)

        print("Game:\nStarting phase:\n" + str(self))

        self.is_over = False

        while not self.is_over:
            encounter = 1

            while encounter == 1 or encounter == 2:
                # Start turn phase
                self.phase = "start_turn"
                self.offense = self.players[0]

                # Destiny phase
                self.phase = "destiny"
                self.defense = self.destiny_deck.draw() # Should be of type Player

                print("Offense: " + self.offense + "\nDefense: " + self.defense)

                # Launch phase
                self.phase = "launch"


                # Alliance phase
                self.phase = "alliance"

                # Planning phase
                self.phase = "planning"

                # Reveal phase
                self.phase = "reveal"

                # Resolution phase
                self.phase = "resolution"
                self.players.append(self.offense)
                self.check_if_over()
                encounter += 1

    # Deals out eight cards to a player
    def deal_hand(self, player):
        for i in range(8):
            player.hand.append(self.draw_deck.draw())

    def initialize_destiny_deck(self):
        for player in self.players:
            self.destiny_deck.cards += [Card("destiny", player.name, player) for i in range(3)]
        self.destiny_deck.shuffle()

    def check_if_over(self):
        for player in self.players:
            if len(player.foreign_colonies) == 5:
                self.is_over = True

    def __str__(self):
        result = ""
        for player in self.players:
            result += str(player)
        result += str(self.draw_deck)
        result += str(self.discard_deck)
        result += str(self.destiny_deck)
        return result


class Player:
    def __init__(self, name, color, power):

        # List of the cards the player contains in his/her hand
        self.hand = []
        self.name = name
        self.color = color
        self.power = power

        # Everyone starts the game with five home planets; the total changes only in rare circumstances
        self.home_planets = []

        # Game finishes once a player or multiple players reach five foreign colonies
        self.foreign_colonies = []

    # Used for printing out a player
    def __str__(self):
        result = "Player: " + self.power + " - " + self.name + ", " + self.color + "\n"
        for planet in self.home_planets:
            result += str(planet)
        result += "Hand:\n"
        for card in self.hand:
            result += str(card)
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
            self.cards += [Card("negotiate", "normal") for i in range(0, 5)]

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
            result += "<empty>\n"
        elif self.hidden:
            result += "<hidden>\n"
        else:
            for card in self.cards:
                result += str(card)
        return result + "\n"


class Card:
    def __init__(self, type, value, other = "None"):
        self.type = type
        self.value = value
        self.other = other

    # Used for printing out the type of card
    def __str__(self):
        return self.type + " - " + str(self.value) + "\n"


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