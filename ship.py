from typing import Literal, Tuple

class Ship:
  def __init__(self, name: str, size: int, name_en: str, start_position: Tuple[int, int], char: str = "?", orientation:  Literal["vertical", "horizontal"] = "horizontal") -> None:
    self.name = name
    self.name_en = name_en
    self.size = size
    self.live = size
    self.char = char[0]
    self.orientation:Literal["vertical", "horizontal"] = orientation
    self.start_position = start_position
    self.direction = (0,1) if orientation == "vertical" else (1,0)
    x_end_pos = start_position[0]+(self.size-1)*self.direction[0]
    y_end_pos = start_position[1]+(self.size-1)*self.direction[1]
    self.end_position = (x_end_pos, y_end_pos)

  def to_string(self):
    return str(self.__dict__)