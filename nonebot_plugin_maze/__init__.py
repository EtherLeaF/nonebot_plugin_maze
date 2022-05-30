from io import BytesIO
from argparse import Namespace

from PIL import Image, ImageDraw

from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.params import State, ShellCommandArgs
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from .Maze import Maze
from .utils import maze_args_parser, analyze_op_sequence


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

    await maze.generate(args.method.lower())

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

    try:
        op_seq = analyze_op_sequence(str(state["op_sequence"]))
    except AssertionError as e:
        await maze_game.reject(str(e), at_sender=True)

    for op in op_seq:
        for i in range(op[1]):
            is_reached, step_used = await maze.event_handler(op[0], maze_draw)

    buf = BytesIO()
    maze_image.save(buf, format="png")
    if is_reached:
        await maze_game.finish(f"恭喜你成功解开了迷宫！\n共消耗步数: {step_used}" +
                               MessageSegment.image(buf.getvalue()), at_sender=True)
    else:
        await maze_game.reject(MessageSegment.image(buf), at_sender=True)
