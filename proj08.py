import cards

########CLASSES########
class Row(object):
    '''
    Each row has simmilar attribute so It was made into a class. The class handles a rgeat deal of the funstionality
    The row class handles most of the move mechanics, by checking if it is psossible to move the cards. It also unhides card when nessecary
    '''
    def __init__(self):
        '''
        This just makes an empty list that represents the cards in the row
        '''
        self.deck = []
    
    def add(self, card):
        '''
        Description: Adds the given card to the end of the list associated wit the row
        Requires: the card to be added
        Returns: nothing
        '''
        self.deck.append(card)

    def Empty(self):
        '''
        Description: Checks to see if the list associate with the row is empty or not
        Returns: Boolean of the state of the row
        Requires: Nothing
        '''
        if len(self.deck) == 0:
            return True
        else:
            return False
        
    def Get_run(self, num):
        '''
        Description: Checks the legitimacy of the cards being moved. it makes sure they are in the same suit, and are in numerical order
        Requires: The number of cars that are trying ot be moved
        Returns: a list of cards that are to be moved. If the move is illegal it returns None
        '''
        run = []
        suit = self.deck[-1].get_suit()
        for i in range(num):
            if self.deck[-1].get_hidden():
                print("that is hidden")
                return None
            if self.deck[-1].get_suit() != suit:
                print("Not of same suit")
                return None
        for i in range(num):
            run.append(self.deck.pop(-1))
        return run

    def make_unhidden(self):
        '''
        Description: Unhides the last card in the row. This corresponds to the card at the end
        Requires:Nothing
        Returns: Nothing
        '''
        try:
            self.deck[-1].set_hidden(False)
        except IndexError:
            pass
        

    def Set_check(self):
        '''
        Description: After a move is made it checks the row the cards were added to to see if there was a set made.
        Requires: Nothing
        Returns: Boolean of wheter a set was made or not
        '''
        suit = self.deck[-1].get_suit()
        for i in range(1,14):
            try:
                card = self.deck[-i]
            except IndexError:
                return False
            if card.get_suit() != suit:
                return False
            else:
                if card.get_rank() != i:
                    return False
                else:
                    continue
        for i in range(13):
            self.deck.pop(-1)
        return True
                    

 #######FUNCTIONS#######
def setup():
    '''
    Description: Creates the deck that will be usde in the game. Creates 4 Deck items and then takes out only the Hearts and Spades
    Requires: Nothing
    Returns:List of cards that are still to be used and a List of Row objects that are holding cards
    '''
    rows = []
    Maindeck = []
    for i in range(4):
        tmp = cards.Deck()
        tmp.shuffle()
        while tmp.empty() == False:
            card = tmp.deal()
            if card.get_suit() == "S" or card.get_suit() == "H":
                Maindeck.append(card)
    for i in range(10):
        rows.append(Row())
    for i in range(54):
        r = i%10
        Card = Maindeck.pop(0)
        if i < 44:
            Card.set_hidden(True)
        rows[r].add(Card)
    return Maindeck, rows

def Display(Game,deck,Sets):
    '''
    Description: This takes all the things to be displayed adn then displas them accordingly
        The list of rows is cycled through and ustilizes the hidden function of cards.
    Requires: Takes a list of rows in the game, the List of cards to be used, and the number of sets made
    Returns: Outputs to the console the game set up
    '''
    print("---------------------")
    for i in range(len(Game)):
        print("Row",i+1,": ", end = '')
        for j in Game[i].deck:
            print(j, end = ' ')
        print()
    print("---------------------")
    print("Stock:",len(deck))
    print(Sets, " out of 8 sets.")
    print("---------------------")
    print()

def Options():
    '''
    Description: Funciton that displays the options the player has. Gets an input form the user to return
    Requires: Nothing
    Returns: The users choice
    '''
    print("Enter an option")
    print("\t d - deal new row")
    print("\t h - help")
    print("\t q - quit")
    print("\t m (Source row #)(Target row#)(Number of cards) - move")
    prompt = input("")
    prompt.strip()
    choice = prompt.split(' ')
    return choice

def deal(Game, Deck):
    '''
    Description: Funciton that deals a card to each row if the rules are met.(All rows have at least one card)
    Requires: The list of game rows, and the list of cards to be dealt
    Returns: The updated list of cards to be dealt and the game rows
    '''
    if len(Deck) >0:
        for i in range(10):
            if Game[i].Empty():
                print("Can not deal cards when a row is empty")
                return Game, Deck
        for i in range(10):
            Game[i].deck.append(Deck.pop(0))
    else:
        print("No more cards to deal")
    return Game, Deck

def Help():
    print('1. A card moved in the tableau must be placed on a card that is ranked one higher than itself. For example, a “3” can be placed on a “4”, but not the other way around. They do not have to be the same suit.')
    print("2. A sequence of cards with the same suit and descending rank (i.e. a “run”) can be moved in the tableau according to the following restrictions \n \t the connecting card must follow the same rank rule, i.e. the highest card in the run must be ranked one lower than the card it is placed on, but need not be the same suit.For example, a sequence with a 4, 3, and 2 of hearts can be place on a 5 card of any suit")
    print("3. Cards can only be dealt from the stock if none of the tableau rows are empty.")

def Move(Game, From, To, Number,Sets):
    '''
    Description: Utilizes the Row classes funcitons to check if you can move cards. If it can move the cards then it will proceede to move them
    Requires: The list of game rows, what rows are involved in the move, and how many sets are completed
    Returns: The updated game rows list, and how many sets have been made
    '''
    run = Game[From-1].Get_run(Number)
    if run == None:
        print("That is an invlaid move")
        return Game, Sets
    else:
        try: 
            l = Game[To-1].deck[-1].get_rank()-1
        except IndexError:
            l = run[-1].get_rank()
        if run[-1].get_rank() == l:
            for i in range(1,Number+1):
                Game[To-1].add(run[-i])
                Game[From-1].make_unhidden()
                Set = Game[To-1].Set_check()
                if Set:
                    Sets += 1
        else:
            print("That is an invalid move")
            for i in range(1,Number+1):
                Game[From-1].add(run[-i])
    return Game, Sets

def main():
    '''
    Description: Main function that runs the game loop
    Requires: Nothing
    Returns: Nothing
    '''
    deck, Game = setup()
    Sets = 0
    Turn = 1
    run = True
    while run:
        Display(Game,deck,Sets)
        print("Turn:",Turn)
        choice = Options()
        if choice[0] == 'd':
            Game, deck = deal(Game,deck)
        elif choice[0] == 'h':
            Help()
        elif choice[0] == 'q':
            break
        elif choice[0] == 'm':
            try:
                Game, Sets = Move(Game,int(choice[1]),int(choice[2]),int(choice[3]),Sets)
            except IndexError:
                print("Not enough inputs")
        else:
            print("That is an invlaid choice")
        for i in range(10):
            if Game[i].Empty():
                run = False
                print("You win!")
            else:
                pass
    print("Thanks for playing!")
    
            
            


##########RUN###########
    
if __name__ == '__main__':
    main()
