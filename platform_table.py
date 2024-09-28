from typing import List
from ship import Ship


class PlatformTable:
  def __init__(self, width, height) -> None:
    self.table = self.__create_platform(width, height)
    self.width = width
    self.height = height
    self.player_ships:List[Ship] = []
    self.botShips = []
  
  def __create_platform(self, width: int, height: int):
    return [ [f" " for x in range(width)] for y in range(height) ]
  
  def to_string(self):
    RED = "\033[31m"
    GREEN = "\033[32m"
    GREEN_BOLD = "\033[1;32m"
    RESET = "\033[0m"
    width = self.width
    height = self.height
    header = [f" {self.__get_label_position_format(x)} " for x in range(width)]
    header.insert(0, "    ")
    header = "|".join(header)
    header_separator= "----+" + "+".join(["----" for x in range(width)])
    rows = ""
    print(f"{RED} Bright Green{RESET} \n")
    for y in range(height):
      row = f" {self.__get_label_position_format(y)} |" +  "|".join([f"{GREEN_BOLD}  {self.table[y][x]} {RESET}" for x in range(width)])
      row_separator = "----+" + "+".join(["----" for x in range(width)])
      rows = rows + row + "\n" + row_separator + "\n"
    return header + "\n" + header_separator + "\n" + rows
  
  def __get_label_position_format(self, position: int) -> str:
    if position < 10:
      return f" {position}"
    return f"{position}"
  
  def add_player_ship(self, ship:Ship):
    has_cross = self.verify_ship_cross(ship)
    if(has_cross):
      #print("Hay un cruce con otro barco o se sale del tablero")
      #return None
      raise Exception("Hay un cruce con otro barco o se sale del tablero")
    x_pos=ship.start_position[0]
    y_pos=ship.start_position[1]
    count_size = 0
    cross = False
    while not cross and not count_size >= ship.size:
      x_pos = ship.start_position[0] + count_size if ship.orientation == "horizontal" else x_pos
      y_pos = ship.start_position[1] + count_size if ship.orientation == "vertical" else y_pos
      cross = self.table[y_pos][x_pos] != " "
      if cross:
        raise Exception("Estas colocando un barco sobre otro")
      self.table[y_pos][x_pos] = ship.char
      """ try:
      except:
        print("No se puede colocar el ship") """
      count_size = count_size + 1
    self.player_ships.append(ship)
  
  def verify_ship_cross(self, ship: Ship): 
    is_cross = False
    is_over_flow = False
    for registered_ship in self.player_ships:
      is_new_ship_x_repeated = ship.orientation == 'vertical'
      is_registered_x_repeated = registered_ship.orientation == 'vertical'
      value = ship.start_position[0] if is_new_ship_x_repeated else ship.start_position[1]
      value_registered_start = registered_ship.start_position[0] if not is_registered_x_repeated else registered_ship.start_position[1]
      value_registered_end = registered_ship.end_position[0] if not is_registered_x_repeated else registered_ship.end_position[1]
      is_cross = is_cross or (value_registered_start <= value <= value_registered_end)
      if is_cross:
        break
    is_over_flow = ship.end_position[0] >= self.width or ship.end_position[1] >= self.height
    return is_cross or is_over_flow