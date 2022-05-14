from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    min_maze_rows: int = 13
    max_maze_rows: int = 35
    min_maze_cols: int = 13
    max_maze_cols: int = 35
    default_maze_rows: int = 18
    default_maze_cols: int = 27
