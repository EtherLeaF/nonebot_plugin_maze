<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# Nonebot_Plugin_Maze

_✨ 基于OneBot适配器的[NoneBot2](https://v2.nonebot.dev/)交互式解迷宫插件 ✨_
  
</div>

## 功能

- 可指定大小与算法生成迷宫
- 发送方向与步数解迷宫
- 游戏过程中可随时退出

## 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_maze
```

- 使用 pip

```
pip install nonebot_plugin_maze
```

## 获取插件帮助

- 可选择接入[nonebot-plugin-PicMenu](https://github.com/hamo-reid/nonebot_plugin_PicMenu)以便用户获取插件相关信息与用法。

## 如何使用

### .env 配置项

```ini
min_maze_rows = 13            # 迷宫最小行数
max_maze_rows = 35            # 迷宫最大行数
min_maze_cols = 13            # 迷宫最小列数
max_maze_cols = 35            # 迷宫最大列数
default_maze_rows = 18        # 迷宫默认生成行数
default_maze_cols = 27        # 迷宫默认生成列数
maze_movement_key = "ULDR"    # 迷宫移动方向键
```

各配置项的含义与默认值如上。
  
- 对于以上配置项，规定需同时满足```min_maze_rows <= default_maze_rows <= max_maze_rows```以及```min_maze_cols <= default_maze_cols <= max_maze_cols```。

- 因此，在修改一些配置项时可能强制需要连着某些其他的配置项一起修改。


- 同时，建议不要把最小行数/列数设置为小于10的值，以免引发未知错误

  - 也建议不要把最大行数/列数设置过大，例如50以上，第一是因为资源占用问题，~~第二是因为生成个那么大的迷宫有谁愿意玩啊喂~~


- 可遵循```上左下右```的格式修改移动方向键，例如```WASD```，规定方向键***只能为字母***。

### 开始游戏

使用以下命令触发，需加上命令前缀！

```
maze [-r --rows <ROWS>] [-c --cols <COLUMNS>] [-m --method <ALGORITHM>]
```

- 可使用```-r```规定迷宫的行数，```-c```规定迷宫的列数

    - 以上两项参数的范围和默认值参考```.env```文件中的相关配置项。

- 可使用```-m```规定迷宫的生成算法，目前支持```DFS```，```Prim```，```Kruskal```三种算法，默认值为```Kruskal```，检测此参数时对大小写不敏感。

### 如何进行游戏

~~在用户发送指令获取到初始迷宫后，我们终于可以愉快地开始游戏了！~~

用户需要持续发送***操作序列***以在迷宫中移动，直到解开迷宫。

要知道***操作序列***是什么，首先要定义***操作***。

***注：以下定义使用默认参数```maze_movement_key = "ULDR"```***

- 我们定义一个操作的格式为```方向+步数```，用正则表达就是```[UDLR]\d*```，用阳间方法表达的话就是```U(up)|D(down)|L(left)|R(right) + steps```，```步数```可以留空以表示一步。
- 例如```R```，```D3```，```L1```就是几个合法的操作，分别表示右移一步，下移三步，左移一步。

    - 为避免频繁数格子的问题，我们定义```一步```为沿该方向的路径***一直走***，直到遇见死路或走到岔路口。

***有了操作是什么，我们定义操作序列为```n(n≥1)```个操作组合而成的字符串。***

游戏中觉得太耗时间？迷宫太难解不出来？不想玩了？

- 可以在游戏过程中随时发送```结束```或者```quit```以结束游戏并获取参考解法。

## 演示

只用文字描述往往十分吃力，废话不多说，上Demo：

<div align="left">
  <img src="https://user-images.githubusercontent.com/100039483/168439968-624e4cdf-ae94-485d-9113-740a0b1993a7.png" width="500" />
</div>

<div align="left">
  <img src="https://user-images.githubusercontent.com/100039483/168439976-e31bad3b-c774-498c-8705-2d27bf87a4cb.png" width="500" />
</div>
