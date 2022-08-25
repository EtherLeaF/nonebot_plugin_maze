import re

from nonebot import get_driver
from nonebot.rule import ArgumentParser

from .config import Config


def load_config():
    maze_config = Config.parse_obj(get_driver().config.dict())
    DEFAULT_MAZE_ROWS, DEFAULT_MAZE_COLS = maze_config.default_maze_rows, maze_config.default_maze_cols
    MIN_MAZE_ROWS, MAX_MAZE_ROWS = maze_config.min_maze_rows, maze_config.max_maze_rows
    MIN_MAZE_COLS, MAX_MAZE_COLS = maze_config.min_maze_cols, maze_config.max_maze_cols
    MAZE_MOVEMENT_KEY = maze_config.maze_movement_key

    assert (
        MIN_MAZE_ROWS <= DEFAULT_MAZE_ROWS <= MAX_MAZE_ROWS and
        MIN_MAZE_COLS <= DEFAULT_MAZE_COLS <= MAX_MAZE_COLS
    ), "设置的迷宫行列数默认值需介于设置的迷宫行列数的最小值与最大值之间！"
    assert (
        MAZE_MOVEMENT_KEY.isalpha()
        and len(MAZE_MOVEMENT_KEY) == 4
    ), "需将迷宫方向键设置为四个字母！"

    return (
        DEFAULT_MAZE_ROWS, DEFAULT_MAZE_COLS,
        MIN_MAZE_ROWS, MAX_MAZE_ROWS,
        MIN_MAZE_COLS, MAX_MAZE_COLS,
        MAZE_MOVEMENT_KEY.upper()
    )


default_rows, default_cols = load_config()[:2]
MAZE_MOVEMENT_KEY = load_config()[-1]
maze_args_parser = ArgumentParser()
maze_args_parser.add_argument('-r', '--rows', type=int, default=default_rows)
maze_args_parser.add_argument('-c', '--cols', type=int, default=default_cols)
maze_args_parser.add_argument('-m', '--method', type=str, default='kruskal')


def analyze_op_sequence(op_seq_str: str):
    parsed_seq = re.findall(rf"[{MAZE_MOVEMENT_KEY}]-?\d*", op_seq_str.upper())
    assert parsed_seq, "未检测到合法的操作序列！"

    op_seq = []
    steps = 0
    for op in parsed_seq:
        if len(op) == 1:
            direction, step = op, 1
        else:
            direction, step = op[0], int(op[1:])

        assert step <= 10, "你确定要一直往同一个方向走这么远吗？操作撞墙也是会计入步数的哦"
        assert step > 0, f"暂时不知道怎么走{step}步呢..."

        op_seq.append([direction, step])
        steps += step
        assert steps <= 50, "单个操作序列总步数不可大于50！"

    return op_seq
