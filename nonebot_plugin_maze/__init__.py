# @Env: Python3.10
# -*- coding: utf-8 -*-
# @Author  : T_EtherLeaF
# @Email   : thetapilla@gmail.com
# @Software: PyCharm

from argparse import Namespace

from nonebot.plugin import on_shell_command
from nonebot.typing import T_State
from nonebot.params import State, ShellCommandArgs
from nonebot.adapters.onebot.v11 import MessageEvent

from .__main__ import init_maze, handle_maze
from .utils import maze_args_parser
from .metadata import *


maze_game = on_shell_command("maze", priority=30, parser=maze_args_parser, block=True)


@maze_game.handle()
async def _init_maze(event: MessageEvent, state: T_State = State(), args: Namespace = ShellCommandArgs()):
    await init_maze(matcher=maze_game, event=event, state=state, args=args)


@maze_game.got("op_seq")
async def _handle_maze(event: MessageEvent, state: T_State = State()):
    await handle_maze(matcher=maze_game, event=event, state=state)
