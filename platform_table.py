from typing import List, Tuple
from ship import Ship
from functools import reduce

class PlatformTable:
  def __init__(self, width, height, hidden = False) -> None:
    self.table = self.__create_platform(width, height)
    self.width = width
    self.height = height
    self.player_ships:List[Ship] = []
    self.hidden_ship = hidden
  
  def __create_platform(self, width: int, height: int):
    return [ [{"field": f" ", "ship": None, "is_shot": False} for x in range(width)] for y in range(height) ]
  
  def to_string(self, hidden_ship:bool = None):
    is_hidden_ship = hidden_ship if not hidden_ship == None else self.hidden_ship
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
    get_hidden_shoot_value = lambda x,y: '✠' if self.table[y][x].get('is_shot') else ' '
    get_value = lambda x,y: get_hidden_shoot_value(x,y) if is_hidden_ship else self.table[y][x].get('field')
    get_is_water = lambda x,y: self.table[y][x].get('field') == ' '
    get_calculated_value = lambda x,y: get_value(x,y) if (not self.table[y][x].get('is_shot')) or not get_is_water(x,y) else '.'
    for y in range(height):
      row_data = [f"{RED if self.table[y][x].get('is_shot') else GREEN_BOLD}  {get_calculated_value(x,y)} {RESET}" for x in range(width)]
      row = f" {self.__get_label_position_format(y)} |" +  "|".join(row_data)
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
      cross = self.table[y_pos][x_pos].get('field') != " "
      if cross:
        raise Exception("Estas colocando un barco sobre otro")
      self.table[y_pos][x_pos].update({'field': ship.char, 'ship': ship})
      """ try:
      except:
        print("No se puede colocar el ship") """
      count_size = count_size + 1
    self.player_ships.append(ship)
  
  def verify_ship_cross(self, ship: Ship): 
    is_cross = False
    is_over_flow = False
    for registered_ship in self.player_ships:
      is_cross = is_cross or self.verify_lines_cross((ship.start_position, ship.end_position), (registered_ship.start_position, registered_ship.end_position))
      if is_cross:
        break
    is_over_flow = ship.end_position[0] >= self.width or ship.end_position[1] >= self.height
    print(is_over_flow, is_cross)
    return is_cross or is_over_flow
  
  def verify_lines_cross(self, line1:Tuple[Tuple[int,int],Tuple[int,int]], line2:Tuple[Tuple[int,int],Tuple[int,int]]):
    line1_start, line1_end = line1
    line2_start, line2_end = line2
    
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    # Case 1: One vertical, one horizontal
    if x1 == x2 and y3 == y4:  # line1 is vertical, line2 is horizontal
        return (x3 <= x1 <= x4) and (y1 <= y3 <= y2 or y2 <= y3 <= y1)
    if y1 == y2 and x3 == x4:  # line1 is horizontal, line2 is vertical
        return (y3 <= y1 <= y4) and (x1 <= x3 <= x2 or x2 <= x3 <= x1)
    # Case 2: Both are vertical (same x, overlapping y-range)
    if x1 == x2 and x3 == x4:
        return (x1 == x3) and (max(y1, y2) >= min(y3, y4)) and (max(y3, y4) >= min(y1, y2))
    # Case 3: Both are horizontal (same y, overlapping x-range)
    if y1 == y2 and y3 == y4:
        return (y1 == y3) and (max(x1, x2) >= min(x3, x4)) and (max(x3, x4) >= min(x1, x2))
    return False
  
  def shoot_place(self, position: Tuple[int, int]):
    pos_x, pos_y = position
    place_data = self.table[pos_y][pos_x]
    field = place_data.get('field')
    ship = place_data.get('ship')
    is_shot = place_data.get('is_shot')
    place_data.update({'is_shot': True})
    has_shot = False
    if ship is None :
      print("...|==> Le diste al agua <==|...\n\n")
    else:
      if not is_shot:
        ship:Ship = place_data.get('ship')
        ship.life = ship.life - 1
        place_data.update({'is_shot': True})
        print('"  Diste a un barco  "\n\n')
        has_shot = True
      else:
        print('"  ...  "\n\n')
    return has_shot

  def get_ships_life(self):
    all_life = reduce(lambda a, b: a + b.life, self.player_ships, 0)
    return all_life