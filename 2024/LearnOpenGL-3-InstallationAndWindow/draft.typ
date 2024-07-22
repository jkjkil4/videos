#import "@preview/pinit:0.1.3": *

#show heading: set text(fill: blue)

#show heading.where(level: 2): t => box(fill: blue.lighten(75%), t)

#set par(justify: true, leading: 0.8em)
#set text(font: "Noto Serif CJK SC")

#show raw: set text(font: ("Source Code Pro", "Noto Sans S Chinese"))

#show raw: r => {
  if r.block {
    box(fill: luma(95%), inset: 8pt, radius: 4pt, width: 100%, r)
  } else {
    r
  }
}

#let note(body) = box(
  fill: yellow.lighten(85%),
  inset: 8pt,
  width: 100%,
  body
)

#let in-janim(body) = box(
  fill: blue.lighten(85%),
  inset: 8pt,
  width: 100%,
  body
)

#box(stroke: luma(20%), width: 100%, inset: 8pt)[
  这是视频文字稿，文案修改自

  #{
    set text(0.8em)
    [
      https://learnopengl-cn.github.io/01%20Getting%20started/03%20Hello%20Window/
    ]
  }

  #set text(0.7em)

  #note[黄色背景表示备注]

  #in-janim[蓝色背景表示使用动画演示]

  #box(fill: luma(95%), inset: 8pt, radius: 4pt, width: 100%)[
    灰色背景表示代码块
  ]
]

= 安装与创建窗口

== moderngl 与 GLFW

moderngl 是在 Python 中对 OpenGL 的封装，他与另一个 Python 库 PyOpenGL 不同的是，PyOpenGL 仅仅是对 C 中的 OpenGL 函数的绑定，而 moderngl 做了许多易用的封装，使其更符合 Python 中的使用习惯.

在我们画出出色的效果之前，首先肯定得创建一个窗口，这样才能方便看到渲染结果对吧！然而，这在每个操作系统上都是不一样的，OpenGL 有意的将这些操作抽象（Abstract）出去. 这意味着我们不得不自己处理创建窗口，以及处理用户输入.

幸运的是，有一些库已经提供了我们所需的功能，其中一部分是特别针对 OpenGL 的. 这些库节省了我们书写操作系统相关代码的时间，提供给我们一个窗口用来渲染，在这里我们使用的是 GLFW. 当然，学习完 OpenGL 后，你也可以尝试用其它的库来创建窗口，比如在 Python 中常见的有 pyglet、pygame、pyside6 等，并且 moderngl 自己也做了一个叫作 moderngl-window 的扩展库.

总而言之，我们将使用 moderngl 来创建与使用 OpenGL 上下文，并且使用 GLFW 创建窗口进行显示.

== 安装

首先，请确保你安装的是 3.7 或更高版本的 Python，如果不是的话，你可以尝试以下方式：

#in-janim[
  - 使用 anaconda 等工具创建更高版本的虚拟环境（推荐）
  - 卸载并安装更高版本
]

我使用的编辑器是 vscode，这里我在终端输入 `python --version` 检查当前使用的 Python 版本，显示 Python 3.12，是 3.7 及以上的，没有问题.

如果你用了 anaconda 之类的工具，可能得切换一下虚拟环境.

// 如果你用了 anaconda 之类的工具，记得在右下角这里切换虚拟环境

// - （注1：需要当前编辑的是 .py 文件才会有这个选项，你可以先创建一个）
// - （注2：需重新打开当前终端才能进入切换后的环境）

接着，使用这个命令

```sh
pip install moderngl glfw
```

安装 moderngl 和 glfw，我这里使用镜像下载.

```sh
pip install moderngl glfw -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

所以在后面加上了清华镜像源的链接.

== 创建窗口

安装好 moderngl 和 GLFW 后，我们就可以正式开始编写代码.

新建一个 .py Python 文件，我们先把 moderngl 和 GLFW 导入一下.

```py
import glfw
import moderngl as mgl
```

因为我感觉 moderngl 有点太长了，所以我用 `as` 给它起了“mgl”的简写.

glfw 不是一上来就能用的，我们要先初始化一下.

```py
# 检查 glfw 是否成功初始化
if not glfw.init():
    raise Exception('GLFW出错')
```

在正常情况下，`glfw.init()` 成功初始化后会返回 `True`，所以我们加上一个 `not` 取反来表示当 glfw 初始化失败时，抛出“GLFW出错”的报错.

接下来我们创建一个窗口对象，这个窗口对象存放了所有和窗口相关的数据，而且会被GLFW的其他函数频繁地用到.

```py
# 创建窗口
window = glfw.create_window(800, 600, "LearnOpenGL", None, None)

# 检查是否成功创建窗口
if not window:
    glfw.terminate()
    raise Exception('窗口出错')
```

`create_window` 函数需要窗口的宽和高作为它的前两个参数. 第三个参数表示这个窗口的标题，这里我们使用"LearnOpenGL"，当然你也可以使用你喜欢的名称. 最后两个参数我们暂时忽略.

#in-janim[
  用动画演示一下宽高以及窗口标题的含义
]

创建完窗口我们就可以通知 GLFW 将我们窗口的上下文设置为当前线程的主上下文了，

```py
glfw.make_context_current(window)
```

并且使用

```py
ctx = mgl.create_context()
```

得到这个上下文对象，我们可以通过它控制窗口上的画面.

#pagebreak()

== 视口

在我们开始渲染之前还有一件重要的事情要做，我们必须告诉OpenGL渲染区域的尺寸大小，即视口（Viewport），这样OpenGL才只能知道怎样根据窗口大小显示数据和坐标.

// 我们可以通过

```py
ctx.viewport = (0, 0, 800, 600)
```

// 来设置视口的位置.

在这四个参数中，前两个参数控制视口左下角的位置. 第三个和第四个参数控制渲染视口的宽度和高度（像素）.

#in-janim[
  大概弄一个带有滑动条的演示，滑动条控制上面四个参数
]

我们将视口的大小设置得比GLFW窗口的小，这样子之后所有的OpenGL渲染将会在一个更小的区域中显示，这样子的话我们也可以将一些其它元素显示在OpenGL视口之外.

#note[
  “这样子的话我们也可以将一些其它元素显示在OpenGL视口之外”

  我没搞懂这句是什么意思

  是指留出的地方还可以画别的吗？
]

一般而言，当用户改变窗口的大小的时候，视口也应该被调整. 我们可以对窗口注册一个回调函数（Callback Function），它会在每次窗口大小被调整的时候被调用.

具体来说，我们先写一个函数

```py
def framebuffer_size_callback(window, width, height):
    ctx.viewport = (0, 0, width, height)
```

这个函数接受三个参数，这是 GLFW 约定好的

- 第一个是 `window`，表示是哪个窗口的大小改变了，这里我们用不到
- `width` 和 `height` 这两个整数表示窗口新的大小

我们注册这个函数，告诉 GLFW，我们希望每当窗口大小改变的时候调用这个函数：

```py
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
```

当窗口被第一次显示的时候，`framebuffer_size_callback` 也会被调用

#note[
  LearnOpenGL CN 原页面提到

  “对于视网膜（Retina）显示屏，`width` 和 `height` 都会明显比原输入值更高一点”

  但是我对这并不是很了解
]

#pagebreak()

== 准备好你的窗口

我们可不希望只绘制一个图像之后我们的应用程序就立即退出并关闭窗口. 我们希望程序在我们主动关闭它之前不断绘制图像并能够接受用户输入. 因此，我们需要在程序中添加一个 `while` 循环，我们可以把它称之为#highlight[渲染循环]（Render Loop），它能在我们点击关闭按钮之前一直保持运行.

我们用几行代码实现一个简单的渲染循环：

```py
while not glfw.window_should_close(window):
    glfw.swap_buffers()
    glfw.poll_events()
```
- `glfw.window_should_close` 函数在我们每次循环的开始前检查一次 GLFW 是否被要求退出（例如按了关闭键之后）

  如果是的话，该函数返回 `True`，这个渲染循环将停止运行，之后我们就可以关闭应用程序

- `glfw.poll_events` 函数检查有没有触发什么事件（比如键盘输入、鼠标移动等）、更新窗口状态，并调用对应的回调函数进行处理，比如我们在前面就注册了一个响应窗口大小改变的回调函数

- `glfw.swap_buffers` 函数会交换颜色缓冲，也就是更新窗口上显示的内容

== 最后一件事

当窗口关闭，渲染循环结束后，我们需要正确释放/删除之前分配的所有资源

我们可以在最后调用 `glfw.terminate` 函数来完成

```py
glfw.terminate()
```

这样便能清理所有的资源并正确地退出应用程序

== 运行

现在你可以尝试运行这个程序了，如果没有做错的话，那么就会出现一个非常无聊的黑色窗口

如果没有出现，或者你想要我编写好的这些代码，请在简介中点开这一节的代码

#pagebreak()

完整代码

#{
  set text(size: 0.8em)
  [
    https://jkjkil4.github.io/posts/LearnOpenGL_3_InstallationAndWindow/
  ]
}

```py
# 导入需要的库
import glfw
import moderngl as mgl

# 初始化 GLFW
if not glfw.init():
    raise Exception('GLFW出错')

# 创建窗口
window = glfw.create_window(800, 600, 'LearnOpenGL', None, None)
if not window:
    glfw.terminate()
    raise Exception('窗口出错')

# 获得上下文
glfw.make_context_current(window)
ctx = mgl.create_context()

# 视口
def framebuffer_size_callback(window, width, height):
    ctx.viewport = (0, 0, width, height)

glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# 渲染循环
while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)

# 终止 GLFW
glfw.terminate()
```
