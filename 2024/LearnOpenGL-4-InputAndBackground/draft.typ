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

== 输入

我们同样希望能够在 GLFW 中实现一些输入控制，这可以通过使用 GLFW 的几个输入函数来完成

我们用到 `glfw.get_key` 函数，它需要一个窗口以及一个按键作为输入，我们可以通过这个函数检查特定的按键是否按下

这里我们创建一个 process_input 函数，我们把处理输入的代码都写在这里面/*，保持代码的整洁*/

```py
def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
```

这里我们检查用户是否按下了键盘左上角的 ESC 键，所以我们向 `glfw.get_key` 传入 `glfw.KEY_ESCAPE`，表示想检查这个按键的状态

此时，如果我们没有按下，`glfw.get_key` 会返回 `glfw.RELEASE`，不会命中这个条件判断

如果我们按下了 ESC 键，`glfw.get_key` 就会返回 `glfw.PRESS`，条件成立，那么就通过 `glfw.set_window_should_close` 函数将这个窗口标记为需要关闭，那么对于渲染循环而言，下一次的循环条件检测就会失败，退出这个循环使得程序结束

我们在渲染循环中调用 `process_input`，这就给我们一个非常简单的方式来检测特定的键是否被按下，并在每一帧做出处理

== 背景颜色

现在我们可以开始进行画面渲染了

我们把渲染操作的代码插到循环的这里，因为我们想让这些渲染指令在每次渲染都能被执行

为了测试一切都正常工作，我们使用一个自定义的颜色清空屏幕. 在每个新的渲染迭代开始的时候我们总是希望清屏，否则我们仍会看见上一次的渲染结果（这可能是你想要的效果，但通常来说不是）. 我们可以使用 `ctx.clear` 来清空屏幕的颜色缓冲，简单来说，我们可以给这个函数传入0到1之间的RGB颜色分量，比如 `(0.0, 1.0, 0.0)` 就是完全只有绿色分量，表现为纯绿色，在这里我们写上 `(0.2, 0.3, 0.3)` 这个颜色

运行程序，可以看到我们将屏幕设置为了类似黑板的深蓝绿色

你可以在简介的链接中找到这部分的完整源代码

在这两节中，我们创建了基本的窗口，了解了如何处理用户按键输入，并调整了窗口的填充颜色

在下一节，我们会向这个窗口上绘制更为具体的东西

// #pagebreak()
#line(length: 100%, stroke: gray)

完整代码

#note[
  TODO
]

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

# 处理输入
def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

# 渲染循环
while not glfw.window_should_close(window):
    # 输入
    process_input(window)

    # 渲染指令
    ctx.clear(0.2, 0.3, 0.3)

    # 处理事件、交换缓冲
    glfw.poll_events()
    glfw.swap_buffers(window)

# 终止 GLFW
glfw.terminate()
```
