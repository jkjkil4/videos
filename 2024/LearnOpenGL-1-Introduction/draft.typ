
#import "@preview/pinit:0.1.3": *

#show heading: set text(fill: blue)

#set page(
  margin: (
    right: 50%
  )
)

#show heading.where(level: 2): t => box(fill: blue.lighten(75%), t)

#set par(justify: true)
#set text(font: ("Consolas", "KaiTi"))

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

= LearnOpenGL

#link("https://learnopengl-cn.github.io/")

= 写在前面

原 Learn-OpenGL 教程在 C++ 中进行 OpenGL 开发教学，本教程使用 Python 的 ModernGL 进行教学，
因为我认为这样更好地理解 OpenGL 的运作机制，而不用关心一些繁琐的步骤。

= 正文

== 前言：什么是 OpenGL？

OpenGL 全称 Open Graphics Library#pin(1)

#p(1)[
  大概做成OpenGL放上面，全称放下面的呈现方式
]

它是用来做什么的呢？

我们编写的大多数代码是在CPU上执行的，在CPU上执行通用的任务十分方便#pin(2)

#lp(2)[
  做一个简易动画，有点像图灵机那样的（然而最后做成 IO 了）
]

但是，当我们需要进行图形渲染时，比如一个1920x1080的游戏画面，CPU 需要面对2073600个像素，甚至你命令它要在一秒内完成几十遍这样的任务！#pin(3)

#p(3)[
  爆掉的动画
]

这时候就轮到GPU登场了：因为渲染时，每个像素点的流程是基本一致的（尽管结果不一样），类似于批量化流水线，GPU 通过特制的并行计算#pin(4)，大大提高渲染效率。

#p(4)[
  并行计算的动画，大概是“一批数据拿来”，每次使用同样的“工具”批量处理，然后这样执行下去（最后做成直接引视频了）
]

但是，我们并不能直接用C++、Python等语言去编写GPU程序，GPU无法执行我们交给CPU执行的如此复杂的程序，因为GPU是为了高效并行计算而特制的#pin(5)，自然无法执行通用的程序。

#p(5, offset-dx: 180pt, offset-dy: 4pt)[
  大概弄一个“程序”交给CPU欣然接受，交给GPU直接被甩开的动画
]

因此，我们就可以使用OpenGL进行编程，告诉GPU要如何处理提供给它的数据#pin(6)，并得到渲染完的图像。

#lp(6)[
  弄一个GLSL被GPU接受的动画
]

所以说，我们可以使用OpenGL进行高效的图像渲染和处理。#pin(7)

#p(7)[
  弄一个由顶点生成图像的动画？不知道好不好做（我觉得可以用立方体作例子）
]

#v(20pt)

当然，不是只有OpenGL提供了调用GPU的能力，还有DirectX和vulkan等。#pin(8)

#p(8)[
  这段作为脚注即可？淡化显示
]

无论你学习OpenGL是为了学业，找工作，或仅仅是因为兴趣，这里都将能够教会你现代(Core-profile) OpenGL的知识，欢迎来到OpenGL的世界！

== 你选择这个教程的原因

在互联网上，有关学习OpenGL的有成千上万的文档与资源#pin(9)，然而其中有很多的资源仅仅讨论了OpenGL的立即渲染模式（Immediate Mode，通常会说旧 OpenGL），亦或是不完整，缺少适当的文档，甚至是仅仅不适合你的口味。

#lp(9, scale: 2.6)[
  显示一个显示屏形状，排一堆文档，然后提到旧文档以及不合适的文档的时候，对它们作淡化
]

#p(10, offset-dx: 200pt)[
  左边代码右边效果，概览一下
]

如果你很享受提供手把手指导的教程，以及提供清晰例子#pin(10)的教程，那么这个教程很可能就很适合你，这个教程旨在让那些没有图形编程经验的人们能够理解，又让那些有经验的读者有阅读下去的兴趣。

== 你将学会什么呢？

这个教程的核心是现代 OpenGL。学习（和使用）现代OpenGL需要用户对图形编程以及 OpenGL 的幕后运作#pin(11)有非常好的理解才能在编程中有很好的发挥。

#lp(11, scale: 2.5)[
  前面写出“现代 OpenGL”，把这两点从这里引出
]

所以，我们会首先讨论核心的图形学概念，OpenGL怎样将像素绘制到屏幕上#pin(12)，以及如何利用黑科技做出一些很酷的效果。

#lp(12)[
  显示一个屏幕，扫出一堆像素
]

除了核心概念之外，我们还会讨论许多有用的技巧，它们都可以用在你的程序中，比如说在场景中移动，做出漂亮的光照，加载建模软件导出的自定义模型，做一些很酷的后期处理技巧等。#pin(13)

#p(13)[
  考虑从 LearnOpenGL 后面的教程中拿些视频来
]

#pin(100)#box[最后，我们也将会使用我们已学的知识从头开始做一个小游戏，让你真正体验一把图形编程的魅力。]#pin(101)

#pinit-highlight(100, 101)
#p(101)[
  存疑
]

== 前置知识

由于 OpenGL 是一个图形 API，并不是一个独立的平台，它需要一个编程语言来工作，在这里我们使用的是 Python。所以，有一定的 Python 基础在学习这个教程中是必不可少的。当然，我仍将尝试解释大部分用到的概念，所以，你并不一定要是一个 Python 专家才能来学习。不过，请确保你至少应该能写个比 ``Hello World`` 复杂的程序。

除此之外，我们也将用到一些数学知识（线性代数、几何、三角学），同样我也会尝试解释这些概念，虽然可能会用容易理解的方式，但是这些解释都是不全面的。所以，在必须的时候，我会链接一些不错的资料，他们会将这些概念解释地更加全面。

不要被必须的数学知识吓到了，几乎所有的概念只要有基础的数学背景都可以理解。我也会将数学的内容压缩至极限。大部分的功能甚至都不需要你理解所有的数学知识，因为数学是底层原理，而大多数情况下已经有别人替我们完成了这部分，只要你会使用就行，但是知道它的原理也不是一件坏事。
