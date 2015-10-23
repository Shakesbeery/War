import numpy as np

class Card():

	def __init__(self, suit, value):
		self.suit = suit
		self.value = value

	def __eq__(self, other):
		return self.value == other.value

	def __gt__(self, other):
		return self.value>other.value

	def __lt__(self, other):
		return self.value<other.value

	def __radd__(self, other):
		return self.value+other

class Player():

	def __init__(self, cards):
		self.discard = []
		self.deck = cards

	def draw(self):
		try:
			return self.deck.pop()
		except IndexError:
			self.shuffle()
			return self.deck.pop()

	def shuffle(self):
		if len(self.deck)==0:
			np.random.shuffle(self.discard)
			self.deck = self.discard
		else:
			np.random.shuffle(self.discard)
			unused = self.discard
			unused.extend(self.deck)
			deck = unused
		self.discard = []

	def take(self, cards):
		self.discard.extend(cards)

	def no_cards(self):
		return (len(self.deck)+len(self.discard)) == 0

	def total(self):
		return len(self.deck)+len(self.discard)

def war(player1, player2, ante_pool=[]):
	if len(player1.deck)<4:
		player1.shuffle()
	if len(player2.deck)<4:
		player2.shuffle()

	if player1.total()<=4 or player2.total()<=4:
		final_war(player1, player2, ante_pool)
		return

	ante_pool = [player1.draw(),player1.draw(),player1.draw(),
				player2.draw(),player2.draw(),player2.draw()]

	player1_card = player1.draw()
	player2_card = player2.draw()

	if player1_card < player2_card:
		player2.take(ante_pool)
	elif player1_card > player2_card:
		player1.take(ante_pool)
	else:
		if player1.total()<=4 or player2.total()<=4:
			ante_pool.extend([player1_card,player2_card])
			final_war(player1, player2, ante_pool)
			return
		else:
			ante_pool.extend([player1.draw(),player1.draw(),player1.draw(),
							player2.draw(),player2.draw(),player2.draw()])
			ante_pool.extend([player1_card,player2_card])
			war(player1, player2, ante_pool)

def final_war(player1, player2, ante_pool):
	#If the last draw was the only remaining card, this becomes 
	#the player's comparison card. Otherwise, use 4 card (after ante)
	#or use deepest card after incomplete ante
	if not bool(player1.deck):
		player1_card = ante_pool[-2]
	else:
		try:
			player1_card = player1.deck[-4]
		except IndexError:
			player1_card = player1.deck[0]
	if not bool(player2.deck):
		player2_card = ante_pool[-1]
	else:
		try:
			player2_card = player2.deck[-4]
		except IndexError:
			player2_card = player2.deck[0]

	if player1_card < player2_card:
		player2.take([player1_card,player2_card])
	elif player1_card > player2_card:
		player1.take([player1_card,player2_card])
	else:
		player1_ante_sum = sum(player1.deck[-3:])
		player2_ante_sum = sum(player2.deck[-3:])
		if player1_ante_sum>player2_ante_sum:
			player1.take([player1_card,player2_card])
		else:
			player2.take([player1_card,player2_card])

def generate_deck():
	deck = []
	for suit in ('Hearts','Clubs','Spades','Diamonds'):
		for value in range(1,14):
			deck.append(Card(suit, value))
	np.random.shuffle(deck)
	return deck

if __name__ == '__main__':
	deck = generate_deck()
	player1 = Player(deck[:27])
	player2 = Player(deck[27:])
	no_victor = True
	while no_victor:
		player1_card = player1.draw()
		player2_card = player2.draw()

		if player1_card < player2_card:
			player2.take([player1_card,player2_card])
		elif player1_card > player2_card:
			player1.take([player1_card,player2_card])
		else:
			if player1.total()<=4 or player2.total()<=4:
				final_war(player1, player2, [player1_card,player2_card])
			else:
				war(player1, player2, [player1_card,player2_card])
		if player1.no_cards() or player2.no_cards():
			no_victor=False

	if player1.no_cards():
		print 'PLAYER 1 LOSES!'
	else:
		print 'PLAYER 2 LOSES!'
	