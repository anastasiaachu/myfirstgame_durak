import random
from typing import Self

# Начнем с создания карты
# ♥ ♦ ♣ ♠
VALUES = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
SUITS = ('Spades', 'Clubs', 'Diamonds', 'Hearts')
SUITS_UNI = {
        'Spades': '♠',
        'Clubs': '♣',
        'Diamonds': '♦',
        'Hearts': '♥'
}

class Card:
    ''' Класс карта'''
    def __init__(self, value: str, suit: str):
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit    # Масть карты

    def to_str(self):
        '''Красивый вывод карты'''
        return f'{self.value}{SUITS_UNI[self.suit]}'
    
    def __str__(self):
        return f'{self.value}{SUITS_UNI[self.suit]}'
    
    def __repr__(self):
        return f'{self.value}{SUITS_UNI[self.suit]}'

    def equal_suit(self, other_card) -> bool:
        '''Проверка являются ли масти карт одинаковые'''
        return self.suit ==  other_card.suit 
            
    def more(self, other_card) -> bool:
        '''Проверка: является ли первая карта старше чем вторая.
           Сначала сравниваются значения карты, потом масти'''
        if self.value ==  other_card.value :
            return SUITS.index(self.suit) > SUITS.index(other_card.suit)
        return VALUES.index(self.value) > VALUES.index(other_card.value)              

    def less(self, other_card) -> bool:
        '''Проверка: является ли первая карта младше, чем вторая'''
        if self.value ==  other_card.value :
            return SUITS.index(self.suit) < SUITS.index(other_card.suit)
        return VALUES.index(self.value) < VALUES.index(other_card.value)
    
    def __gt__(self, other:Self) -> bool:
        return self.more(other)
    
    def __lt__(self, other:Self) -> bool:
        return self.less(other)
    

#Теперь создадим колоду из 52-ух карт и реализуем все методы

class Deck:
    '''Класс колода'''
    def __init__(self):
        # Список карт в колоде. Каждым элементом списка будет объект класса Card
        self.cards = [Card(value, suit)  for suit in SUITS for value in VALUES ]
        
    def show(self):
        '''Отображает все карты колоды в формате:deck[12]: 3♥, 4♦, A♣, … 
           где 12 - текущее кол-во карт в колоде.'''
        return f'desk[{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'
        
    def draw(self, x:int) -> Self:
        '''Возвращает x первых карт из колоды в виде списка, 
           эти карты убираются из колоды. Уточнение: первую карту в списке считаем верхней картой колоды'''
        draw_cards = self.cards[:x]
        self.cards = self.cards[x:]
        return draw_cards
            
    def shuffle(self):
        """Перетасовать колоду"""
        random.shuffle(self.cards)
    
    def __str__(self):
        return f'desk[{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'
    
    def __getitem__(self,index):
        return self.cards[index]
    
    def __iter__(self):
        self.index = -1
        return self 
    
    def __next__(self):
        self.index += 1
        if self.index < len(self.cards):
            return self.cards[self.index]
        else:
            raise StopIteration

    
# deck = Deck()
# # Задачи - реализовать нативную работу с объектами:
# # 1. Вывод колоды в терминал:
# print(deck)  # вместо print(deck.show())

# deck.shuffle()
# print(deck)

# card1, card2 = deck.draw(2)
# # # 2. Вывод карты в терминал:
# print(f'{card1 = }')  # вместо print(card1.to_str())
# print(f'{card2 = }')

# #
# # # 3. Сравнение карт:
# if card1 > card2:
#     print(f"{card1} больше {card2}")

# if card1 < card2:
#     print(f"{card1} меньше {card2}")

# # Это на следующее занятие.
# # 4. Итерация по колоде:
# for it_card in deck[:5]:
#     print(it_card, end=', ')
# print()
# # 5. Просмотр карты в колоде по ее индексу:
# # __getitem__(self, index):
# print('Шестая карта:', deck[5])


