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

#let note(body) = box(stroke: blue, inset: 4pt, body)

= OpenGL 具体介绍

== OpenGL 背景知识

在前一节中，我们提到，可以使用 OpenGL 与显卡进行交互，进行快速的大批量图形渲染。所以说，一般而言，OpenGL 被认为是一个 API（Application Programming Interface，应用程序编程接口），包含了一系列可以操作图形、图像的函数。然而，OpenGL 本身其实并不是一个 API，它仅仅是一个由 #link("www.khronos.org")[Khronos 组织] 制定并维护的规范（Specification）。

OpenGL 规范严格规定了每个函数该如何执行，以及它们的输出值。至于内部具体每个函数是如何实现的，将由编写 OpenGL 库的开发者自行决定，只要其功能和结果与规范相匹配就行（也就是，我们作为用户在调用它们的时候不会感受到功能的差异）。

实际的 OpenGL 库的开发者通常是显卡的生产商。你购买的显卡所支持的 OpenGL 版本都为这个系列的显卡专门开发的。当你使用 Apple 系统的时候，OpenGL 库是由 Apple 自身维护的。在 Linux 下，有显卡生产商提供的 OpenGL 库，也有一些爱好者改编的版本。这也意味着任何时候 OpenGL 库表现的行为与规范规定的不一致时，基本都是库的开发者留下的 bug。

#note[
  由于 OpenGL 的大多数实现都是由显卡厂商编写的，当产生一个 bug 时通常可以通过升级显卡驱动来解决。这些驱动会包括你的显卡能支持的最新版本的 OpenGL，这也是为什么总是建议你偶尔更新一下显卡驱动。
]

所有版本的OpenGL规范文档都被公开的寄存在 Khronos 那里。你有兴趣的话可以找到OpenGL3.3（我们将要使用的版本）的规范文档。如果你想深入到 OpenGL 的细节（只关心函数功能的描述而不是函数的实现），这是个很好的选择。如果你想知道每个函数具体的运作方式，这个规范也是一个很棒的参考。
