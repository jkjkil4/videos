#import "@preview/pinit:0.2.0": *

#show heading: set text(fill: blue)

#set page(
  margin: (
    right: 50%
  )
)

#show heading.where(level: 2): t => box(fill: blue.lighten(75%), t)

#set par(justify: true, leading: 0.8em)
#set text(font: "Noto Serif CJK SC")
#show raw: set text(font: ("Consolas", "LXGW WenKai Lite"))

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

#let note(body) = {
  set text(size: 0.9em)
  box(stroke: blue, inset: 8pt, body)
}

= 元素缓冲对象

在上一节我们使用三个顶点渲染了一个三角形。

在渲染顶点这一话题上我们还有最后一个需要讨论的东西——索引缓冲对象(Index Buffer Object，IBO)，也叫元素缓冲对象(Element Buffer Object，EBO)。

== 渲染一个矩形

要解释索引缓冲对象的工作方式最好还是举个例子：假设我们不再绘制一个三角形而是绘制一个矩形。由于 OpenGL 主要处理三角形，我们可以绘制两个三角形来组成一个矩形。这会生成下面的顶点的集合：#pin(0)

#lp(0)[
  使用矩形框框住对应的顶点数据，使用圆圈圈出这个位置，依次展示
]

```py
vertices = np.array([
    # 第一个三角形
    0.5, 0.5, 0.0,      # 右上角
    0.5, -0.5, 0.0,     # 右下角
    -0.5, 0.5, 0.0,     # 左上角
    # 第二个三角形
    0.5, -0.5, 0.0,     # 右下角
    -0.5, -0.5, 0.0,    # 左下角
    -0.5, 0.5, 0.0      # 左上角
], dtype='f4')
```

由于使用 `mgl.TRIANGLES` 的选项渲染时，会将每三个顶点渲染为一个三角形，所以这六个顶点就会绘制出两个三角形，在这里也就构成了一个矩形。

可以发现，有几个顶点叠加了。我们指定了右下角两次，左上角也是两次！

本来只有4个顶点的矩形却用了6个顶点来表示，这样就产生了50%的额外开销。当我们有包括上千个三角形的模型之后这个问题会更糟糕，这会产生一大堆浪费。

更好的解决方案是只储存不同的顶点，并设定绘制这些顶点的顺序。

这样子我们只要储存4个顶点就能绘制矩形了，之后只要指定绘制的顺序就行了。如果 OpenGL 提供这个功能就好了，对吧？

值得庆幸的是，索引缓冲对象的工作方式正是如此。 IBO是一个缓冲区，就像一个顶点缓冲区对象一样，它存储 OpenGL 用来决定要绘制哪些顶点的索引。这种所谓的索引绘制(Indexed Drawing)正是我们问题的解决方案。

我们先把重复的去掉，定义不重复的 4 个顶点，并且从 0 开始按顺序索引这些顶点

```py
vertices = np.array([
    0.5, 0.5, 0.0,      # 右上角
    0.5, -0.5, 0.0,     # 右下角
    -0.5, -0.5, 0.0,    # 左下角
    -0.5, 0.5, 0.0      # 左上角
], dtype='f4')

vbo = ctx.buffer(vertices.tobytes())

indices = np.array([
    0, 1, 3,    # 第一个三角形
    1, 2, 3     # 第二个三角形
], dtype='i4')

ibo = ctx.buffer(indices.tobytes())
```

接着我们就可以给出绘制出矩形所需的索引

另外需要注意的是，和 VBO 类似，这里我们指定 IBO 的数据类型是 `'i4'`，表示每个索引使用 4 字节的整数(int)存储。

我们把这个索引缓冲通过 `index_buffer=ibo` 的方式传递给 vao。这样设置后，这个 vao 在渲染时就会参照这个索引缓冲渲染出两个三角形//：//#pin(1)

// - 前一组 (0,1,3) 将右上角、右下角、左上角作为一组渲染为一个三角形
// - 后一组 (1,2,3) 则将右下角、左下角、左上角作为一组渲染为一个三角形

// #p(1)[
//   在讲后一个三角形的时候把前一个三角形淡化，讲完之后取消淡化
// ]

现在运行代码，你看到的还是这个橘黄色的矩形。

如果你遇到了什么问题，可以参考一下这里给出的源码。
