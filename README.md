<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">
  
# Nonebot_Plugin_Maze
  
_✨ 基于OneBot适配器的[NoneBot2](https://v2.nonebot.dev/)交互式解迷宫插件 ✨_
  
</div>

## 功能

- 可指定大小与算法生成迷宫
- 以文字消息作为交互形式解迷宫
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

## 如何使用

### .env 配置项

```ini
min_maze_rows = 13            # 迷宫最小行数
max_maze_rows = 35            # 迷宫最大行数
min_maze_cols = 13            # 迷宫最小列数
max_maze_cols = 35            # 迷宫最大列数
default_maze_rows = 18        # 迷宫默认生成行数
default_maze_cols = 27        # 迷宫默认生成列数
```

各配置项的含义与默认值如上。
  
- 对于以上配置项，规定需同时满足```min_maze_rows <= default_maze_rows <= max_maze_rows```以及```min_maze_cols <= default_maze_cols <= max_maze_cols```。

- 因此，在修改一些配置项时可能强制需要连着某些其他的配置项一起修改。


- 同时，建议不要把最小行数/列数设置为小于10的值，以免引发未知错误

  - 也建议不要把最大行数/列数设置过大，例如50以上，第一是因为资源占用问题，~~第二是因为生成个那么大的迷宫有谁愿意玩啊喂~~

### 开始游戏

使用以下命令触发，需加上命令前缀！

```
maze [-r --rols <ROWS>] [-c --cols <COLUMNS>] [-m --method <ALGORITHM>]
```

- 可使用```-r```规定迷宫的行数，```-c```规定迷宫的列数

    - 以上两项参数的范围和默认值参考```.env```文件中的相关配置项。

- 可使用```-m```规定迷宫的生成算法，目前支持```DFS```，```Prim```，```Kruskal```三种算法，默认值为```Kruskal```，检测此参数时对大小写不敏感。

### 如何进行游戏

~~在用户发送指令获取到初始迷宫后，我们终于可以开始愉快地游戏了！~~

用户需要持续发送操作序列以在迷宫中移动，直到解开迷宫。

至于操作序列是什么，让我们先来定义操作。

- 我们定义一个操作的格式为```方向+步数```，用正则表达就是```[UDLR]\d*```，用阳间方法表达的话就是```U(up)|D(down)|L(left)|R(right) + steps```，```步数```可以留空以表示一步。
- 例如```R```，```D3```，```L1```就是几个合法的操作，分别表示右移一步，下移三步，左移一步。

    - 注意：单个操作中步数大于10是不合法的，例如```D11```，~~```R18```~~
    - 识别操作时对大小写不敏感
    - 为避免频繁数格子的问题，我们定义```一步```为向该方向的路径一直走，直到遇见死路或走到岔路口，<u>有可能拐弯</u>。

有了操作是什么，我们就可以定义操作序列了。

- 顾名思义，操作序列就是```n(n≥1)```个操作组合而成的序列，以字符串的形式表达。
- 例如```R2D3RU2LD2R4```就是一个合法的操作序列，含义不必赘述。

    - 注意：单个操作序列中所有操作步数总和不可大于50，例如```R10D10R10U10L10D```是不合法的。

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
