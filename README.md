# conda-tui

#### 介绍
conda是常用的Python环境管理工具，但conda相关命令冗长繁多、难以记忆，导致很多用户常常遗忘命令的写法，处于一种“边查边用”的状态，降低了工作效率。

Anaconda公司虽然推出了GUI工具Anaconda Navigator，使用户能够以图形化方式管理conda环境，但Anaconda Navigator启动速度慢、运行速度慢，用户体验较差。

本项目提供了Anaconda Navigator核心功能的TUI实现，软件完全在终端中运行，与Anaconda Navigator相比速度有明显提升，同时还可以在没有图形环境的系统中使用。软件界面与Anaconda Navigator中“Environments”选项卡的内容相似，操作便捷，易于上手。本项目兼容Windows、Linux和Mac系统，为不同平台的用户提供了一致的用户体验。

![screenshot](./screenshot.jpg)

#### 软件架构
使用Python中的[textual库](https://textual.textualize.io/)开发TUI应用


#### 安装教程

1.  克隆本仓库，或下载zip压缩包并解压
2.  将本项目所在文件夹添加到PATH环境变量中。对于Windows系统，可以在“高级系统设置”-“环境变量”中设置。对于Linux/Mac系统，可以根据您使用的shell修改对应的配置文件（例如，如果使用bash，则修改.bashrc文件，如果使用zsh，则修改.zshrc文件），并重启终端或使用source命令刷新配置文件
3.  对于Linux/Mac系统，通过`chmod +x ./condat`为目录中的condat文件赋予执行权限
4.  在终端中输入`condat`即可启动软件。注意，首次启动时，会在项目所在目录下创建一个Python虚拟环境并在其中安装textual库，后续使用时会自动跳过该步骤。

