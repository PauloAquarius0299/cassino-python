from abc import ABC, abstractmethod
import itertools
import random
from time import sleep
import os
import matplotlib.pyplot as plt

class BaseMachine(ABC):
    @abstractmethod
    def _gen_permutations(self):
        pass
        
    @abstractmethod
    def _get_final_result(self):
        pass
        
    @abstractmethod
    def _display(self):
        pass
    
    @abstractmethod
    def _check_result_user(self):
        pass
    
    @abstractmethod
    def _update_balance(self):
        pass
    
    @abstractmethod
    def _emojize(self):
        pass
    
    @abstractmethod
    def gain(self):
        pass
        
    @abstractmethod
    def play(self, amount_bet, player):
        pass


class Player:
    def __init__(self, balance=0):
        self.balance = balance

class CassaNiquel(BaseMachine):
    
    def __init__(self, level=1, balance=0):
        self.SIMBOLOS = {
            'star-struck': 'U+1F929',
            'face-with-tongue': 'U+1F61B',
            'smiling-face-with-hearts': 'U+1F970',
            'winking-face': 'U+1F609',
            'grinning-face-with-sweat': 'U+1F605'
        }
        self.level = level
        self.balance = balance
        self.initial_balance = balance
        self.permutations = self._gen_permutations()
    
    def _gen_permutations(self):
        permutations = list(itertools.product(self.SIMBOLOS.keys(), repeat=3))
        for _ in range(self.level):
            for symbol in self.SIMBOLOS.keys():
                permutations.append((symbol, symbol, symbol))
        return permutations

    def _get_final_result(self):
        result = list(random.choice(self.permutations))    
        if len(set(result)) == 3 and random.randint(0, 5) >= 2:
            result[1] = result[0]  
        return result
            
    def _display(self, amount_bet, result, time=0.3):
        seconds = 1
        for _ in range(int(seconds / time)):
            print(self._emojize(random.choice(self.permutations)))
            sleep(time)
            os.system('clear')
        print(self._emojize(result))
        
        if self._check_result_user(result):
            print(f'Você venceu e recebeu: {amount_bet * 3}')
        else:
            print('Foi quase, tente novamente')
        
    def _emojize(self, emojis):
        return ''.join(chr(int(self.SIMBOLOS[code].replace('U+', ''), 16)) for code in emojis)

    
    def _check_result_user(self, result):
        return len(set(result)) == 1  
    
    def _update_balance(self, amount_bet, result, player: Player):
        if self._check_result_user(result):
            ganho = amount_bet * 3
            self.balance -= ganho
            player.balance += ganho
        else:
            self.balance += amount_bet
            player.balance -= amount_bet
    
    def play(self, amount_bet, player: Player):
        result = self._get_final_result()
        #self._display(amount_bet, result)
        self._update_balance(amount_bet, result, player)
        
    @property
    def gain(self):
        return self.initial_balance + self.balance


maquina = CassaNiquel(level=1)

JOGADORES_POR_DIA = 1000
APOSTAS_POR_DIA = 5
DIAS = 180 
VALOR_MAXIMO = 200


saldo = []

players = [Player() for i in range(JOGADORES_POR_DIA)]

for i in range(0, DIAS):
    for j in players:
        for k in range(0, random.randint(1, APOSTAS_POR_DIA)):
            maquina.play(random.randint(5, VALOR_MAXIMO), j)
    saldo.append(maquina.gain)
            
plt.figure()
x = [i for i in range(1, DIAS + 1)]
plt.plot(x,saldo)
plt.show()

plt.plot([i for i in range(JOGADORES_POR_DIA)], [i.balance for i in players])
plt.grid(True)
plt.show()