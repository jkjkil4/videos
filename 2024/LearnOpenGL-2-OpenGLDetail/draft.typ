#import "@preview/pinit:0.1.3": *

#show heading: set text(fill: blue)

#set page(
  margin: (
    right: 50%
  )
)

#show heading.where(level: 2): t => box(fill: blue.lighten(75%), t)

#set par(justify: true, leading: 0.8em)
#set text(font: "Noto Serif CJK SC")

#let p(pin-name, body, ..args) = pinit-point-to(
  fill: blue.lighten(75%),
  pin-dy: -3pt,
  offset-dy: -2pt,
  body-dy: -4pt,
  pin-name,
  ..args,
  {
    set text(fill: blue)
    box(
      fill: blue.lighten(90%),
      inset: 4pt,
      body
    )
  }
)

#let lp(pin-name, body, scale: 1, ..args) = p(
  pin-name,
  offset-dx: 70pt * scale,
  offset-dy: 5pt * scale,
  ..args,
  body
)

#let note(body) = box(stroke: blue, inset: 4pt, body)

= OpenGL 具体介绍

这一节，我们会对 OpenGL 的一些基本知识进行介绍，虽然主要是一些文字内容，但是这对你理解 OpenGL 是什么、怎么用有一定的帮助。

== OpenGL 背景知识

在前一节中我们提到，可以使用 OpenGL 与显卡进行交互，进行快速的大批量图形渲染#pin(1)。所以说一般而言，OpenGL 被认为是一个 API（Application Programming Interface，应用程序编程接口），包含了一系列可以操作图形、图像的函数#pin(2)。然而，OpenGL 本身其实并不是一个 API，它仅仅是一个由 #link("www.khronos.org")[Khronos 组织] 制定并维护的规范（Specification）#pin(3)。

#p(1)[
  左边的框里放一些基本的 OpenGL 函数，右边放一个显卡，中间用一些线路表示数据交换
]
#lp(2, scale: 3, offset-dy: 3pt)[
  框拉长显示出更多的 OpenGL 函数
]
#lp(3, offset-dy: 0pt)[
  显示一个文件袋的图样
]

OpenGL 规范严格规定了每个函数该如何执行，以及它们的输出值#pin(4)。至于内部具体每个函数是如何实现的，将由编写 OpenGL 库的开发者自行决定，只要我们作为用户在调用它们的时候不会感受到功能的差异就行了。

#lp(4, scale: 2)[
  左边箭头，右边箭头
]

实际的 OpenGL 库的开发者通常是显卡的#pin(5)生产商。你购买的显卡所支持的 OpenGL 版本都为这个系列的显卡专门开发的。当你使用 Apple 系统的时候，OpenGL 库是由 Apple 自身维护的。在 Linux 下，有显卡生产商提供的 OpenGL 库，也有一些爱好者改编的版本#pin(6)。这也意味着任何时候 OpenGL 库表现的行为与规范规定的不一致时，基本都是库的开发者留下的 bug。

#p(5)[
  左边系统，右边OpenGL

  在不同系统间切换显示
]
#lp(6, scale: 1.4)[
  右边 OpenGL 图标后面多显示几个
]

#note[
  由于 OpenGL 的大多数实现都是由显卡厂商编写的，当产生一个 bug 时通常可以通过升级显卡驱动来解决。这些驱动会包括你的显卡能支持的最新版本的 OpenGL，这也是为什么总是建议你偶尔更新一下显卡驱动。
]

#note[
  所有版本的OpenGL规范文档都被公开的寄存在 Khronos 那里。你有兴趣的话可以找到OpenGL3.3（我们将要使用的版本）的规范文档。如果你想深入到 OpenGL 的细节（只关心函数功能的描述而不是函数的实现），这是个很好的选择。如果你想知道每个函数具体的运作方式，这个规范也是一个很棒的参考。
]#pin(7)

#p(7)[
  我觉得这两段直接把文字丢屏幕上就好了
]

#pagebreak()

== OpenGL 核心模式与立即渲染模式

早期的 OpenGL 使用#highlight[立即渲染模式]（Immediate Mode，也就是固定渲染管线），这个模式下绘制图形很方便，但是由于 OpenGL 的大多数功能都被库隐藏起来，开发者很少有控制 OpenGL 如何进行计算的自由。#pin(1)

#lp(1, offset-dy: 0pt, body-dy: -16pt)[
  左边放 OpenGL 图标，先向右上方连出“立即渲染模式”
]

而开发者迫切希望能有更多的灵活性，OpenGL3.2 开始，规范文档开始废弃#pin(2)立即渲染模式，并鼓励开发者在 OpenGL 的#highlight[核心模式]下#pin(3)进行开发，这个分支的规范完全移除了旧的特性。

#lp(2)[
  使“立即渲染模式”的部分变暗
]
#p(3, offset-dy: 10pt)[
  向右下方连出“核心模式”
]

立即渲染模式就像一台有着基本功能的机器#pin(4)，略去了很多内部的运作细节。与之相反，核心模式给了我们定制这个机器的机会，我们能够定制#pin(5)这个机器中的每一个零件，给了我们更高的灵活性，并且通过这种方式将更多的任务交给了 GPU，充分发挥其并行计算的优势。#pin(6)

#p(4, body-dy: -10pt)[
  大概做一个“给机器一个东西，出来另一个东西的演示”
]
#p(5)[
  淡化机器外壳，各种零件缩小淡入，有把各种零件塞进去的感觉
]
#lp(6, offset-dy: -5pt)[
  使机器在z方向变成一排，展现出批量处理的感觉
]

这也是为什么我们的教程面向 OpenGL3.3 的核心模式。虽然上手更困难，但这份努力是值得#pin(7)的。

#p(7)[
  Write("OpenGL3.3")

  一秒后直接显示一个√
]

由于更高版本的 OpenGL 都是基于 3.3 的#pin(8)，没有改动核心架构。因此，所有的概念和技术在现代 OpenGL 版本里都保持一致，这也正是我们面向 OpenGL3.3 进行学习的原因。所有 OpenGL 更高的版本都是在 3.3 的基础上引入了额外的#pin(9)功能，当你的经验足够，你可以轻松使用来自更高版本 OpenGL 的新特性。

#lp(8)[
  把 3.3 弄成地基的样子
]
#p(9)[
  把额外的功能表示成几个方块叠到 3.3 的上面，大概一个塔的样子
]

但是，使用新版本的 OpenGL 特性时，只有新一代的显卡能够支持你的应用程序。这也是为什么大多数开发者基于较低版本的 OpenGL 编写程序，并只提供选项启用新版本的特性。#pin(10)

#p(10)[
  搞个勾选框的示意
]

== 状态机

OpenGL 自身是一个巨大的状态机（State Machine）：一系列的变量描述 OpenGL 此刻应当如何运行。

假设我们想告诉 OpenGL 去画线段而不是三角形，我们通过改变一些上下文变量来改变 OpenGL 状态，从而告诉 OpenGL 如何去绘图。一旦我们改变了 OpenGL 的状态为绘制线段，下一个绘制命令就会画出线段而不是三角形。

当使用 OpenGL 的时候，我们会遇到一些#highlight[状态设置函数]（State-changing Function），这类函数将会改变上下文。以及#highlight[状态使用函数]（State-using Function），这类函数会根据当前 OpenGL 的状态执行一些操作。

只要你记住 OpenGL 本质上是个大状态机，就能更容易理解它的大部分特性。#pin(1)

#lp(1, body-dy: -16pt)[
  我感觉这一节可以表现成一个“仪表盘”的形式，并且可以给摄像机加一点三维角
]

== 其它

#note[
  在 LearnOpenGL 原文中，还提及了“扩展”和“对象”的小节，由于我们的侧重不在此或与我们将要使用的 ModernGL 无关，故略去。若对这部分内容感兴趣，可以阅读原文章。
]
