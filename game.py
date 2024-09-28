import math
import random
import time
from platform_table import PlatformTable
from ship import Ship

class Game:
  def __init__(self) -> None:
    self.winner=None
    self.player_platform = PlatformTable(width=10, height=10)
    self.bot_platform = PlatformTable(width=10, height=10, hidden=True)
    self.load_bot()
    # print(self.bot_platform.to_string())
    self.load_player()
    self.start_battle()

  def load_player(self):
    orientation = {"V": "vertical", "H": "horizontal"}
    platform = self.player_platform

    print(platform.to_string())
    has_completed_input = False
    while not has_completed_input:
      try:
        print("\nConfigura tu Destructor [2 espacios]:")
        destroyer_data = {
          "start_x": int(input("Columna Inicial: ")),
          "start_y": int(input("Fila Inicial: ")),
          "orientation": orientation[input("Dirección (H para horizontal, V para Vertical):").upper()],
        }
        destroyerPlayer = Ship(name='Destructor', name_en="Destroyer", size=2, char="D", orientation=destroyer_data.get("orientation"), start_position=(destroyer_data.get("start_x"), destroyer_data.get("start_y")))
        platform.add_player_ship(destroyerPlayer)
        has_completed_input = True
      except KeyboardInterrupt:
        exit()
      except Exception as e:
        print(e)
        print("\n ======================================== \n")
        # raise Exception("error")
    print(platform.to_string())

    has_completed_input = False
    while not has_completed_input:
      try:
        print("\nConfigura tu Submarino [3 espacios]:")
        submarine_data = {
          "start_x": int(input("Columna Inicial: ")),
          "start_y": int(input("Fila Inicial: ")),
          "orientation": orientation[input("Dirección (H para horizontal, V para Vertical):").upper()],
        }
        submarinePlayer = Ship(name='submarino', name_en="Submarine", size=3, char="S", orientation=submarine_data.get("orientation"), start_position=(submarine_data.get("start_x"), submarine_data.get("start_y")))
        platform.add_player_ship(submarinePlayer)
        has_completed_input = True
      except KeyboardInterrupt:
        exit()
      except Exception as e:
        print(e)
        print("\n ======================================== \n")
        # raise Exception("error")
    print(platform.to_string())

    has_completed_input = False
    while not has_completed_input:
      try:
        print("\nConfigura tu Acorazado [4 espacios]:")
        battleship_data = {
          "start_x": int(input("Columna Inicial: ")),
          "start_y": int(input("Fila Inicial: ")),
          "orientation": orientation[input("Dirección (H para horizontal, V para Vertical):").upper()],
        }
        battleshipPlayer = Ship(name='Acorazado', name_en="Battleship", size=4, char="A", orientation=battleship_data.get("orientation"), start_position=(battleship_data.get("start_x"), battleship_data.get("start_y")))
        platform.add_player_ship(battleshipPlayer)

        has_completed_input = True
      except KeyboardInterrupt:
        exit()
      except Exception as e:
        print(e)
        print("\n ======================================== \n")
        # raise Exception("error")
    print(platform.to_string())


  def load_bot(self): 
    platform = self.bot_platform
    get_ship_data = lambda : {
      "start_x": random.randint(0, self.bot_platform.width),
      "start_y": random.randint(0, self.bot_platform.height),
      "orientation": random.choice(["vertical", "horizontal"]),
    }
    has_completed_input = False
    while not has_completed_input:
      try:
        destroyer_data = get_ship_data()
        destroyer_bot = Ship(name='Destructor', name_en="Destroyer", size=2, char="D", orientation=destroyer_data.get("orientation"), start_position=(destroyer_data.get("start_x"), destroyer_data.get("start_y")))
        platform.add_player_ship(destroyer_bot)
        has_completed_input = True
      except Exception:
        pass

    has_completed_input = False
    while not has_completed_input:
      try:
        submarine_data = get_ship_data()
        submarine_bot = Ship(name='submarino', name_en="Submarine", size=3, char="S", orientation=submarine_data.get("orientation"), start_position=(submarine_data.get("start_x"), submarine_data.get("start_y")))
        platform.add_player_ship(submarine_bot)
        has_completed_input = True
      except Exception:
        pass

    has_completed_input = False
    while not has_completed_input:
      try:
        battleship_data = get_ship_data()
        battleship_bot = Ship(name='Acorazado', name_en="Battleship", size=4, char="A", orientation=battleship_data.get("orientation"), start_position=(battleship_data.get("start_x"), battleship_data.get("start_y")))
        platform.add_player_ship(battleship_bot)
        has_completed_input = True
      except Exception:
        pass

  def start_battle(self):
    print('=====================================================')
    print('                      A Batallar                     ')
    print('=====================================================')
    play_bot = self.play_bot_init()
    while self.winner == None:
      try:
        self.play_player()
        play_bot()
      except KeyboardInterrupt:
        exit()
      except Exception as e:
        pass
    print("\n\n\n")
    print('=====================================================')
    print(f'              {self.winner} ha ganado!!!            ')
    print('=====================================================')
    print("\n\n\n")

  def play_player(self):
    if self.winner != None: return
    while self.winner == None:
      print("Selecciona tu acción:")
      print("B: Ver tablero del bot")
      print("P: Ver tu tablero")
      print("A: Atacar")
      option = input("Escribir opción:").upper()
      if option == 'B' or option == 'SHOW BOT':
        print('=====================================================')
        print(f'                 Tablero Bot: {self.player_platform.get_ships_life()}                   ')
        print('=====================================================')
        is_hidden_ship = False if option == 'SHOW BOT' else None
        print(self.bot_platform.to_string(is_hidden_ship))
      if option == 'P':
        print('=====================================================')
        print(f'                 Tablero Player: {self.player_platform.get_ships_life()}                   ')
        print('=====================================================')
        print(self.player_platform.to_string())
      if option == 'A':
        print("== seleccionar coordenada de ataque: ==")
        pos_x = int(input('Columna:'))
        pos_y = int(input('Fila:'))
        has_shot = self.bot_platform.shoot_place((pos_x, pos_y))
        time.sleep(1)
        if not has_shot:
          break
        is_player_winner = self.bot_platform.get_ships_life() <= 0
        if is_player_winner:
          self.winner = "Player"

  def play_bot_init(self):
    list_x = []
    list_y = []

    def play_bot():
      while self.winner == None:
        print("\n ======== Bot pensando .... ========== \n")
        x_pos=None
        y_pos=None
        is_new = False
        while not is_new:
          is_new = True
          x_pos = random.randint(0, self.player_platform.width)
          y_pos = random.randint(0, self.player_platform.height)
          for i in range(len(list_x)):
            is_new = list_x[i] != x_pos and list_y[i] != y_pos
            if not is_new:
              break

        time.sleep(2)
        has_shot = self.player_platform.shoot_place((x_pos, y_pos))
        if has_shot:
          print('=====================================================')
          print(f'                 Tablero Player: {self.player_platform.get_ships_life()}                   ')
          print('=====================================================')
          print(self.player_platform.to_string())
          print(" >>>> Bot dió a un barco - vuelve a jugar bot <<<<<\n")
          time.sleep(1)
          is_bot_winner = self.player_platform.get_ships_life() <= 0
          if is_bot_winner:
            self.winner = "Bot"
        else:
          print(" >>>> Bot ha fallado <<<<<\n")
          time.sleep(1)
          break

    return play_bot