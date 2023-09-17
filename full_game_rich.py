from deck_total import Card, Deck
from rich.console import Console
from rich.table import Table
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
rich_table = Table(title="Дурак", width = 170)
rich_table.add_column(f"Атакующий игрок", justify="right", no_wrap=True)
rich_table.add_column("Стол", style = 'blue')
rich_table.add_column("Отбивающийся игрок", justify="right")

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
            rich_table.add_row(f'{hand_1}', f'{attack_card}', f'{hand_2}')
            table+=[attack_card]
            has_card = True # Флаг наличия карт, которыми можно атаковать в одном ходу
            defend_card = Game.defend(attack_card,hand_2)

            if defend_card:
                rich_table.add_row('', f'{defend_card}', )
                rich_table.add_row(' ')
                table.append(defend_card) 
            else:
                '''Если защищающийся игрок не отбивается, то атакующий подкидывает все оставшиеся карты 
                   с одинаковым значением, защищающийся забирает все карты, рука не меняется'''
                rich_table.add_row( '', f'{hand_2.name} не может отбиться')
                add_card = Game.add_card(table, hand_1)
                while add_card:
                    rich_table.add_row( '', f'{hand_1.name} подкидывает {add_card} ')
                    table.append(add_card)
                    add_card = Game.add_card(table, hand_1)
                rich_table.add_row('', f'{hand_2.name} забирает все карты со стола')
                rich_table.add_row(' ')
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
                    rich_table.add_row('', f'{add_card}', )
                    defend_card = Game.defend(add_card,hand_2)
                    if defend_card:
                        '''Защищающийся игрок отбивается и цикл начинается снова'''
                        rich_table.add_row('', f'{defend_card}', )
                        table.append(defend_card)
                        rich_table.add_row(' ')
                    else:
                        '''Если защищающийся игрок не отбивается, то атакующий подкидывает все оставшиеся карты 
                           с одинаковым значением, защищающийся забирает все карты, рука не меняется'''
                        rich_table.add_row( '', f'{hand_2.name} не может отбиться')
                        add_card = Game.add_card(table, hand_1)
                        while add_card:
                            rich_table.add_row( '', f'{hand_1.name} подкидывает {add_card} ')
                            table.append(add_card)
                            add_card = Game.add_card(table, hand_1)
                        rich_table.add_row('', f'{hand_2.name} забирает все карты со стола')
                        rich_table.add_row(' ')
                        hand_2.cards += table
                        table.clear()
                        has_card = False
                        return change
                else:
                    rich_table.add_row(' ', 'Бито', ' ')
                    rich_table.add_row(' ')
                    table.clear()
                    change = True
                    has_card = False
                    return change






deck = Deck()
deck.shuffle()
# print(deck)

hand_1 = Hand(deck,'Asia')
hand_2 = Hand(deck,'Vania')

card_game = Game(hand_1,hand_2)

while hand_1.cards and hand_2.cards: # Пока в обеих рукахесть карты, то игра продолжается
    game = Game.game(hand_1, hand_2)
    Game.take(hand_1, deck)
    Game.take(hand_2, deck)
    if game:
        hand_1, hand_2 = hand_2, hand_1

if hand_1:
    rich_table.add_row(' ', f'Победил {hand_1.name} ', ' ')  
else:
    rich_table.add_row(' ', f'Победил {hand_2.name} ', ' ')
 
console = Console()
console.print(rich_table)





