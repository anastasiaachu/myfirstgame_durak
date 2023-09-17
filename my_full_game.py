from deck_total import Card, Deck
'''
создадим имитацию ходов в “Дурака без козырей”:

1. Создайте колоду из 52 карт. Перемешайте ее.
2. Первый игрок берет сверху 10 карт
3. Второй игрок берет сверху 10 карт.
4. Игрок-1 ходит:
    4.1. игрок-1 выкладывает самую маленькую карту по значению
    4.2. игрок-2 пытается бить карту, если у него есть такая же масть, но значением больше.
    4.3. Если игрок-2 не может побить карту, то он проигрывает/забирает себе(см. пункт 7)
    4.4. Если игрок-2 бьет карту, то игрок-1 может подкинуть карту любого значения, которое есть на столе.
5. Если Игрок-2 отбился, то Игрок-1 и Игрок-2 меняются местами. Игрок-2 ходит, Игрок-1 отбивается.    
6. Выведите в консоль максимально наглядную визуализацию данных ходов.
7* Реализовать возможность добрать карты из колоды после того, как один из игроков отбился/взял в руку
'''


MAX_CARDS = 10


class Hand():
    '''Класс рука игрока'''
    def __init__(self, deck: Deck, name):
        self.cards = deck.draw(MAX_CARDS)
        self.name = name

    def __str__(self):
        return f'{self.name} [{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'
    
    def __repr__(self):
        return f'Карт в руке [{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'
    
    def __getitem__(self, item):
        return self.cards[item]
    
    def __iter__(self):
        self.index = -1
        return self 
    
    def __next__(self):
        self.index += 1
        if self.index < len(self.cards):
            return self.cards[self.index]
        else:
            raise StopIteration
    

            
class Game():
    '''Класс игра'''
    
    
    def __init__(self, hand_1, hand_2):
        self.hand_1 = hand_1
        self.hand_2 = hand_2
 
    def attack(forward_player: Hand) -> Card:
        '''Игрок атакует'''
        return forward_player.cards.pop(forward_player.cards.index(min(forward_player.cards)))
    
    def defend(forward_card: Card, player: Hand) -> Card or None:
        '''Другой игрок защищается.
           forward_card - карта атакующего
           player - рука отбивающегося'''
        res = [card for card in player if forward_card.equal_suit(card) and card > forward_card]

        if res:
            return player.cards.pop(player.cards.index(min(res)))

    def add_card(table: list, forward_player: Hand) -> Card or None:
        '''Атакущюий игрок подкидыает карты с одинаковым значением'''
        cards_values = [card.value for card in table]
        res = [card for card in forward_player if card.value in cards_values]

        if res:
            return forward_player.cards.pop(forward_player.cards.index(min(res)))
           
    def take(player: Hand, deck: Deck) -> None:
        '''Игрок берёт необходимое кол-во карт из колоды'''
        if len(player.cards) <= 10:
            number = MAX_CARDS - len(player.cards)
            max_num_of_cards = min(len(deck.cards),number)
            player.cards += deck.draw(max_num_of_cards)

    def game(hand_1: Hand, hand_2: Hand) -> bool:
            '''Реализация игры. Первый ход за первой рукой'''
            
            
            table = []  # Игровой стол
            change = False # Флаг смены руки
            

            
            attack_card = Game.attack(hand_1)
            print(f'Ходит {hand_1.name} {attack_card}')
            table+=[attack_card]
            has_card = True # Флаг наличия карт, которыми можно атаковать в одном ходу
            defend_card = Game.defend(attack_card,hand_2)

            if defend_card:
                print(f'Отбивается {hand_2.name} {defend_card}')
                table.append(defend_card) 
            else:
                '''Если защищающийся игрок не отбивается, то атакующий подкидывает все оставшиеся карты 
                   с одинаковым значением, защищающийся забирает все карты, рука не меняется'''
                add_card = Game.add_card(table, hand_1)
                while add_card:
                    print(f'{hand_1.name} подкидывает карту {add_card}')
                    table.append(add_card)
                    add_card = Game.add_card(table, hand_1)
                print(f'{hand_2.name} забирает все карты со стола')
                hand_2.cards += table
                table.clear()
                return change

            while has_card:
                '''Если защищающийся игрок отбился, то атакующий подбрасывает ему карты 
                   с одинаковым значением, если имеет такие, если таких нет, 
                   то у нас Бито, атакующий и защищающийся игроки меняются местами'''
                add_card = Game.add_card(table, hand_1)
                if add_card and hand_2.cards:
                    table.append(add_card)
                    print(f'{hand_1.name} подкидывает карту {add_card}')
                    defend_card = Game.defend(add_card,hand_2)
                    if defend_card:
                        '''Защищающийся игрок отбивается и цикл начинается снова'''
                        table.append(defend_card)
                        print(f'{hand_2.name} отбивается {defend_card}')
                    else:
                        '''Если защищающийся игрок не отбивается, то атакующий подкидывает все оставшиеся карты 
                           с одинаковым значением, защищающийся забирает все карты, рука не меняется'''
                        print(f'{hand_2.name} не может отбиться')
                        add_card = Game.add_card(table, hand_1)
                        while add_card:
                            table.append(add_card)
                            print(f'{hand_1.name} подкидывает карту {add_card}')
                            add_card = Game.add_card(table, hand_1)
                        print(f'{hand_2.name} забирает все карты со стола')
                        hand_2.cards += table
                        table.clear()
                        has_card = False
                        return change
                else:
                    print('Бито')
                    table.clear()
                    change = True
                    has_card = False
                    return change






deck = Deck()
deck.shuffle()
# print(deck)

hand_1 = Hand(deck,'Asia')
hand_2 = Hand(deck,'Vania')
print(hand_1)
print(hand_2)
print(deck)

card_game = Game(hand_1,hand_2)

while hand_1.cards and hand_2.cards: # Пока в обеих рукахесть карты, то игра продолжается
    game = Game.game(hand_1, hand_2)
    print(hand_1)
    print(hand_2)
    Game.take(hand_1, deck)
    Game.take(hand_2, deck)
    print(hand_1)
    print(hand_2)
    if game:
        hand_1, hand_2 = hand_2, hand_1

if hand_1:
    print(f'Победил игрок {hand_1.name}')  
else:
    print(f'Победил игрок {hand_2.name}')  
 








