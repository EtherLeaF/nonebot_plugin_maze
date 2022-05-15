import re
from io import BytesIO
from argparse import Namespace

from PIL import Image, ImageDraw

from nonebot import get_driver
from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.params import State, ShellCommandArgs
from nonebot.rule import ArgumentParser
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from .Maze import Maze
from .config import Config


maze_config = Config.parse_obj(get_driver().config.dict())
DEFAULT_MAZE_ROWS, DEFAULT_MAZE_COLS = maze_config.default_maze_rows, maze_config.default_maze_cols
MIN_MAZE_ROWS, MAX_MAZE_ROWS = maze_config.min_maze_rows, maze_config.max_maze_rows
MIN_MAZE_COLS, MAX_MAZE_COLS = maze_config.min_maze_cols, maze_config.max_maze_cols
assert MIN_MAZE_ROWS <= DEFAULT_MAZE_ROWS <= MAX_MAZE_ROWS and MIN_MAZE_COLS <= DEFAULT_MAZE_COLS <= MAX_MAZE_COLS, \
    "设置的迷宫行列数默认值需介于设置的迷宫行列数的最小值与最大值之间！"

maze_args_parser = ArgumentParser()
maze_args_parser.add_argument('-r', '--rows', type=int, default=DEFAULT_MAZE_ROWS)
maze_args_parser.add_argument('-c', '--cols', type=int, default=DEFAULT_MAZE_COLS)
maze_args_parser.add_argument('-m', '--method', type=str, default='kruskal')
maze_game = on_shell_command("maze", priority=30, parser=maze_args_parser, block=True)


@maze_game.handle()
async def _init_maze(event: MessageEvent, state: T_State = State(), args: Namespace = ShellCommandArgs()):
    user_id = event.get_user_id()

    if args.method.lower() not in ('dfs', 'prim', 'kruskal'):
        await maze_game.finish("迷宫生成算法填写有误，目前支持DFS，Prim，Kruskal三种算法！", at_sender=True)

    try:
        maze = Maze(width=args.cols, height=args.rows)
    except AssertionError as e:
        await maze_game.finish(str(e), at_sender=True)

    maze_image = Image.new("RGB", size=(maze.cell_width * maze.width, maze.cell_width * maze.height), color="#F2F2F2")
    maze_draw = ImageDraw.Draw(maze_image)

    if args.method.lower() == 'dfs':
        await maze.generate_matrix_dfs()
    elif args.method.lower() == 'prim':
        await maze.generate_matrix_prim()
    else:
        await maze.generate_matrix_kruskal()

    await maze.draw_maze(maze_draw, maze.matrix, maze.path, maze.movement_list)
    buf = BytesIO()
    maze_image.save(buf, format="png")
    await maze_game.send("请通过连续发送操作序列解开迷宫！" + MessageSegment.image(buf.getvalue()), at_sender=True)
    buf.close()

    state[f"maze_{user_id}"] = maze


@maze_game.got("op_sequence")
async def _handle_maze(event: MessageEvent, state: T_State = State()):
    user_id = event.get_user_id()
    maze: Maze = state[f"maze_{user_id}"]
    maze_image = Image.new("RGB", size=(maze.cell_width * maze.width, maze.cell_width * maze.height), color="#F2F2F2")
    maze_draw = ImageDraw.Draw(maze_image)
    if "结束" in str(state["op_sequence"]) or "quit" in str(state["op_sequence"]):
        await maze.show_answer(maze_draw)
        buf = BytesIO()
        maze_image.save(buf, format="png")
        await maze_game.finish("游戏结束！参考解法如下：" + MessageSegment.image(buf.getvalue()), at_sender=True)
    elif "[CQ:" in str(state["op_sequence"]):
        await maze_game.reject()

    op_seq = re.findall(r"[UDLR]\d*", str(state["op_sequence"]).upper())
    if not op_seq:
        await maze_game.reject("未检测到合法的操作序列！", at_sender=True)

    ops = []
    cnt = 0
    for op in op_seq:
        if len(op) == 1:
            t = 1
        else:
            op, t = op[0], int(op[1:])

        if t > 10:
            await maze_game.reject("你确定要一直往同一个方向走这么远吗？操作撞墙也是会计入步数的哦", at_sender=True)
        elif t <= 0:
            await maze_game.reject(f"暂时不知道怎么走{t}步呢...", at_sender=True)

        ops.append([op, t])
        cnt += t
        if cnt > 50:
            await maze_game.reject("单个操作序列总步数不可大于50！")

    for op in ops:
        for i in range(op[1]):
            is_reached, step_used = await maze.event_handler(op[0], maze_draw)

    buf = BytesIO()
    maze_image.save(buf, format="png")
    if is_reached:
        await maze_game.finish(f"恭喜你成功解开了迷宫！\n共消耗步数: {step_used}" +
                               MessageSegment.image(buf.getvalue()), at_sender=True)
    else:
        await maze_game.reject(MessageSegment.image(buf), at_sender=True)
