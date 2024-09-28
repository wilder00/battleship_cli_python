from platform_table import PlatformTable
from ship import Ship

class Game:
  def __init__(self) -> None:
    self.platform = PlatformTable(width=10, height=10)
    self.run()

  def run(self):
    orientation = {"V": "vertical", "H": "horizontal"}
    platform = self.platform

    destroyer = Ship(name='Destructor', name_en="Destroyer", size=2, char="D", orientation="horizontal", start_position=(0,0))
    submarine = Ship(name='submarino', name_en="Submarine", size=3, char="S", orientation="vertical", start_position=(2,0))
    battleship = Ship(name='Acorazado', name_en="Battleship", size=4, char="A", orientation="vertical", start_position=(3,1))
    
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




    """ while True:
      pass """