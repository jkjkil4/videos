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

#let note(body) = {
  set text(size: 0.9em)
  box(stroke: blue, inset: 8pt, body)
}

= 你好，三角形

== 图形渲染管线

在 OpenGL 中，任何事物都在 3D 空间中，而屏幕和窗口却是 2D 像素数组#pin(1)

#lp(1, scale: 1.5, offset-dy: -2pt, body-dy: -24pt)[
  显示一个三维坐标轴（红绿蓝），显示相机轮廓

  视野转到相机的位置闪一下“像素数组”
]

这导致 OpenGL 的大部分工作都是关于把 3D 坐标转变为适应你屏幕的 2D 像素#pin(2)

#lp(2, offset-dy: -2pt, body-dy: -16pt)[
  在 xOy 平面上显示一个矩形，显示把这个矩形投射到摄像机画面的线条
]

3D 坐标转为 2D 坐标的处理过程是由 OpenGL 的图形渲染管线#text(size: 0.7em, gray)[（Graphics Pipeline，大多译为管线，实际上指的是一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程）]管理的#pin(3)

#lp(3, scale: 1.5, offset-dy: -2pt, body-dy: -8pt)[
  弄一个管道样子的东西
]

#note[
  2D坐标和像素也是不同的，2D坐标精确表示一个点在2D空间中的位置，而2D像素是这个点的近似值，2D像素受到你的屏幕/窗口分辨率的限制
]

图形渲染管线可以被划分为两个主要部分：第一部分把你的 3D 坐标转换为屏幕上的 2D 坐标，#pin(4)第二部分是把 2D 坐标转变为实际的有颜色的像素

#p(4)[
  把这两个过程和场景中的画面对应上
]

图形渲染管线具有并行执行的特性，当今大多数#pin(5)显卡都有成千上万的小处理核心，它们在 GPU 上为每一个（渲染管线）阶段运行各自的小程序，从而在图形渲染管线中快速处理你的数据

#p(5)[
  弄很多并列的管道，用 `ShowPassingFlash` 闪“数据流”
]

这些小程序叫做着色器（Shader），规定了 3D 坐标是如何转换到 2D 坐标，以及 2D 坐标如何#pin(6)转变为实际像素的

#p(6)[
  Shader 从上（或者下）指向那些对应的管道

  这里的 Shader 用灰色显示
]

有些着色器可以由开发者配置，因为允许用 #highlight[OpenGL 着色器语言（OpenGL Shading Language, GLSL）]编写着色器来代替默认的，这样#pin(7)就能够更细致地控制图形渲染管线中的特定部分了

#p(7)[
  用蓝色的 Shader 顶掉原来的 Shader
]

在之后我们再具体研究 GLSL，在这一节我们先了解一下基本的概念，并且使用最简单的例子画出一个三角形#pin(8)

#lp(8, scale: 2.2)[
  淡化其它内容，突出 GLSL 的部分
]

#image("assets/pipeline.png")

这是图形渲染管线每个阶段的抽象展示

要注意蓝色部分代表的是我们可以注入自定义#pin(1)的着色器的部分

#p(1)[
  高亮一下
]

如你所见，图形渲染管线包含很多部分，每个部分都将在转换顶点数据到最终像素这一过程中处理各自特定的阶段#pin(2)

我概括性地解释一下渲染管线的每个部分，让你对图形渲染管线的工作方式有个大概了解

注意这只是概括性的哈，一些具体处理不太懂很正常，之后我们还要具体再学的，这里只是过一遍流程让你有个整体的概念

#lp(2, scale: 2, offset-dy: -2pt, body-dy: -8pt)[
  用阴影框过一遍这几个流程
]

#line(length: 100%, stroke: gray)

首先，我们以数组的形式传递 3 个 3D 坐标作为图形渲染管线的输入，用来表示一个三角形

这个数组叫做顶点数据（Vertex Data），它是一#pin(3)系列顶点的集合

#p(3)[
  ShowCreationThenFadeOutAround
]

一个顶点（Vertex）的数据是用顶点属性（Vertex Attribute）表示的，它可以包含任何我们想用的数据，但是简单起见，我们还是假定每个顶点只由一个 3D 位置和一些颜色值组成的吧#pin(4)

#p(4)[
  在点的旁边显示 $(x,y,z)$ 以及 $(r,g,b)$
]

#note[
  为了让OpenGL知道我们的坐标和颜色值构成的到底是什么，OpenGL需要你去指定这些数据所表示的渲染类型。我们是希望把这些数据渲染成一系列的点？一系列的三角形？还是仅仅是一个长长的线？做出的这些提示叫做图元(Primitive)，任何一个绘制指令的调用都将把图元传递给OpenGL。这是其中的几个：`GL_POINTS`、`GL_TRIANGLES`、`GL_LINE_STRIP`
]

图形渲染管线的第一个部分是顶点着色器（Vertex Shader），它把一个单独的顶点作为输入，并允许你将这个顶点进行一些操作和变换（之后会具体解释），以及对顶点属性进行一些基本处理

几何着色器是可选的（也就是可以不写），允许我们根据顶点着色器传递过来的点，去生成新的几何结构

片段着色器的主要目的是计算一个像素的最终颜色，这也是所有 OpenGL 高级效果产生的地方。通常，片段着色器包含 3D 场景的数据（比如光照、阴影、光的颜色等等），这些数据可以被用来计算最终像素的颜色

并且，由于大部分传递给片段着色器的数据都会被插值，所以即使前面传入的是分散的点，这里也会由于插值的缘故得到连续的坐标和颜色

#note[
  OpenGL 中的一个片段是 OpenGL 渲染一个像素所需的所有数据

  片段着色器是处理单个像素的，我们会对屏幕上的每一个像素都使用一遍片段着色器
]

#line(length: 100%, stroke: gray)

可以看到，图形渲染管线非常复杂，它包含很多可配置的部分。然而，对于大多数场合，我们只需要配置顶点和片段着色器就行了

几何着色器是可选的，通常使用它默认的着色器就行了

#line(length: 100%, stroke: gray)

在现代OpenGL中，我们必须定义至少一个顶点着色器和一个片段着色器（因为GPU中没有默认的顶点/片段着色器）

出于这个原因，刚开始学习现代OpenGL的时候可能会非常困难，因为在你能够渲染自己的第一个三角形之前已经需要了解一大堆知识了

在本节结束你最终渲染出你的三角形的时候，你也会了解到非常多的图形编程知识

== 顶点输入

开始绘制图形之前，我们需要先给 OpenGL 输入一些顶点数据。OpenGL 是一个 3D 图形库，所以在 OpenGL 中我们指定的所有坐标都是 3D 坐标（x、y 和 z）

OpenGL 仅当最终输出的 3D 坐标在 3 个轴（x、y和z）上的值在 -1.0 到 1.0 的范围内时才处理它，所有在这个范围内的坐标叫做#highlight[标准化设备坐标(Normalized Device Coordinates)]，此范围内的坐标最终显示在屏幕上（在这个范围以外的坐标则不会显示）

由于我们希望渲染一个三角形，我们一共要指定三个顶点，每个顶点都有一个 3D 位置。我们会将它们以标准化设备坐标的形式（OpenGL 的可见区域）定义为一个 numpy 数组

```py
vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], dtype='f4')
```

它定义了三个坐标

这里 `dtype='f4'` 表示每个坐标分量都是用 4 字节的浮点数（`float`）存储的

明确每个分量所占的字节数很重要，因为使用 GPU 进行图形渲染涉及到传递规定长度的数据

由于 OpenGL 是在 3D 空间中工作的，而我们渲染的是一个2D三角形，所以这里将它这几个顶点的z坐标都设置为 0.0，从而使它看上去像是 2D 的

#line(length: 100%, stroke: gray)

// 现在让我们了解一下标准化设备坐标与屏幕上位置的关系（对于视口(viewport)对应全屏幕的情况）

当显示到窗口上时，我们现在看到的这个标准化设备坐标会直接被拉伸到视口上，在我们的例子中便是拉伸到全窗口画面

这也意味着它与通常的屏幕坐标不同，它的 y 轴正方向为向上，$(0,0)$ 坐标在屏幕的中心，而不是在左上角

// 屏幕的最左边就是 $x=-1.0$，最右边就是 $x=1.0$；同理，最下边是 $y=-1.0$，最上#pin(1)边是 $y=1.0$

// #p(1)[
//   用一个点在这几个地方移动，表示一下这几个位置
// ]

最终你希望所有（变换过的）坐标都在这个坐标空间中，否则它们就不可见了

#line(length: 100%, stroke: gray)

现在我们再来看之前定义的这组顶点数据

```py
vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], dtype='f4')
```

它定义的这三个顶点分别对应屏幕上的这三个#pin(2)位置

#p(2)[
  弄矩形框分别框住 vertices 的三个坐标，并将矩形框变换成屏幕上的点
]

为了将这组顶点数据发送给 GPU，我们通过#highlight[顶点缓冲对象(Vertex Buffer Object, VBO)]管理这个内存，它会在 GPU 内存（通常被称为显存）中储存大量顶点。使用这些缓冲对象的好处是我们可以一次性的发送一大批数据到显卡上，而不是每个顶点发送一次

从 CPU 把数据发送到显卡相对较慢，所以只要可能我们都要尝试尽量一次性发送尽可能多的数据

当数据发送至显卡的内存中后，顶点着色器几乎能立即访问顶点，这是个非常快的过程，并且在下一次渲染时也可以直接使用，而不用再次传递

顶点缓冲对象是我们在 OpenGL 教程中第一个出现的 OpenGL 对象，由于 moderngl 做了易用的封装，所以我们这样就可以创建一个在 GPU 上的顶点数据

```py
vbo = ctx.buffer(vertices.tobytes())
```

由于我们要发送给 GPU 的是原始字节数据，所以我们先使用 `vertices.tobytes()` 将 numpy 数组转为字节数据，然后再传递给 `ctx.buffer` 就得到 `vbo` 了

这里稍微提一下，`ctx.buffer` 有个参数是 `dynamic`，如果你需要经常修改这个 `vbo` 的顶点数据，将其置为 `dynamic=True` 会比较有用，这样就能提示显卡把数据放在能够高速写入的内存部分

对于大部分的情况，我们忽略这个就行了

#line(length: 100%, stroke: gray)

接下来我们创建顶点着色器和片段着色器来真正处理这些数据

如果我们打算做渲染的话，现代 OpenGL 需要我们至少设置一个顶点和一个片段着色器

对着色器更详细的讨论会放在之后的几节，我们现在先简要介绍一下着色器以及配置两个非常简单的着色器来绘制我们第一个三角形

== 顶点着色器

顶点着色器(Vertex Shader)是几个可编程着色器中的一个

我们需要做的第一件事是用着色器语言 GLSL (OpenGL Shading Language) 编写顶点着色器，然后编译这个着色器，这样我们就可以在程序中使用它了。这是一个非常基础的 GLSL 顶点着色器的源代码：

#{
  set text(size: 0.7em)
  ```glsl
  #version 330 core

  in vec3 in_vert;

  void main()
  {
      gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);
  }
  ```
}

可以看到，GLSL 看起来很像 C语言。每个着色器都起始于一个版本声明

OpenGL 3.3 以及和更高版本中，GLSL 版本号和 OpenGL 的版本是匹配的（比如说 GLSL 420 版本对应于 OpenGL 4.2 ）#pin(1)

#lp(1)[
  高亮一下提到的这几个地方
]

我们同样明确表示我们会使用核心模式

下一步，使用in关键字，在顶点着色器中声明所有的输入顶点属性(Input Vertex Attribute)

GLSL 有一个向量数据类型，它包含 1 到 4 个 float 分量，包含的数量可以从它的后缀数字看出来

```glsl
float
vec2 // 2 个 float
vec3 // 3 个 float
vec4 // 4 个 float
```

现在我们只关心位置(Position)数据，所以我们只需要一个顶点属性 `in_vert`，由于每个顶点都有一个 3D 坐标，所以我们给他的类型是 `vec3`

#note[
  *向量(Vector)*

  在图形编程中我们经常会使用向量这个数学概念，因为它简明地表达了任意空间中的位置和方向，并且它有非常有用的数学属性。在GLSL中一个向量有最多4个分量，每个分量值都代表空间中的一个坐标，它们可以通过 `vec.x`、`vec.y`、`vec.z` 和 `vec.w` 来获取。注意 `vec.w` 分量不是用作表达空间中的位置的（我们处理的是 3D 不是 4D），而是用在所谓透视除法(Perspective Division)上。我们会在后面的教程中更详细地讨论向量。
]

为了设置顶点着色器的输出，我们必须把位置数据赋值给预定义的 `gl_Position` 变量（这是 OpenGL 约定好的），它在幕后是 `vec4` 类型的。在 `main` 函数的最后，我们将 `gl_Position` 设置的值会成为该顶点着色器的输出

由于我们的输入是一个 3 分量的向量，我们必须把它转换为 4 分量的。我们可以把 `vec3` 的数据作为 `vec4` 构造器的参数，同时把 `w` 分量设置为 `1.0`（我们会在后面解释为什么）来完成这一任务

当前这个顶点着色器可能是我们能想到的最简单的顶点着色器了，因为我们对输入数据什么都没有处理就把它传到着色器的输出了

在真实的程序里输入数据通常都不是标准化设备坐标，所以我们首先必须先把它们转换至 OpenGL 的可视区域内

== 片段着色器

片段着色器(Fragment Shader)是第二个也是最后一个我们打算创建的用于渲染三角形的着色器。片段着色器所做的是计算像素最后的颜色输出

```glsl
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
```

片段着色器只需要一个输出变量，这个变量是一个 4 分量向量，它表示的是最终的输出颜色

这个 4 分量向量的前 3 个分量正是我们上一节提到的 RGB 值，这里的最后一个分量则表示“不#pin(1)透明度(Alpha)”，这整个则是通过 RGBA 形式表示的颜色

#p(1)[
  放一个背景视频，右边有个半透明的纯色矩形，矩形旁边带一个 Alpha 条
]

一般而言这里的 `FragColor` 是要我们编写程序通过顶点、颜色、光照计算出来的值。为了让事情更简单，在这里我们让片段着色器一直输出不透明度(Alpha)为 1.0（也就是完全不透明）的橘黄色 `(1.0, 0.5, 0.2)` #box(width: 0.8em, height: 0.8em, fill: color.rgb(100%, 50%, 20%))

#pagebreak()

== 着色器程序

我们将上面提到的顶点着色器和片段着色器存储在字符串中

#{
  set text(size: 0.7em)
  ```py
  vertex_shader = '''
  #version 330 core

  in vec3 in_vert;

  void main()
  {
      gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);
  }
  '''

  fragment_shader = '''
  #version 330 core

  out vec4 FragColor;

  void main()
  {
      FragColor = vec4(1.0, 0.5, 0.2, 1.0);
  }
  '''
  ```
}

为了能够让 OpenGL 使用它，我们必须在运行时动态编译它的源代码，在这里我们传给 `ctx.program` 就行了

#{
  set text(size: 0.8em)
  ```py
  prog = ctx.program(vertex_shader, fragment_shader)
  ```
}

它会将 GLSL 代码进行编译，并链接为#highlight[着色器程序对象(Shader Program Object)]

这样的一个着色器程序定义了我们之前提到的图形渲染管线中的流程

== 顶点数组对象

现在，我们已经把输入顶点数据发送给了GPU，并指示了GPU如何在顶点和片段着色器中处理它，我们要将这些东西，也就是前面弄好的顶点缓冲(VBO)和着色器程序，打包到一起，将这些状态存储在#highlight[顶点数组对象(Vertex Array Object, VAO)]中

```py
vao = ctx.vertex_array(prog, vbo, "in_vert")
```

这行代码创建的顶点数组对象表示了一个将 `vbo` 对应的顶点数据，通过着色器程序 `prog` 进行渲染的过程

最后的 `"in_vert"` 表示将顶点数据与着色器程序的 `"in_vert"` 关联，因为我们写明了 `"in_vert"` 的类型是 `vec3`，所以在渲染时，它会把顶点数据中的每三个值作为一组，传递给顶点着色器，这也就是我们期望的“每三个值表示一个坐标”

#line(length: 100%, stroke: gray)

如果你有在 C++ 中写过 OpenGL 程序，你可能会发现这里没有使用 `glVertexAttribPointer` 和 `glEnableVertexAttribArray` 链接顶点属性，这其实是 moderngl 的封装帮我们做完了

但其实 moderngl 的 vertex_array 也可以手动指定顶点属性的链接方式，不过我们这里暂时用不到

#line(length: 100%, stroke: gray)

我们在渲染循环中，\
调用 `vao.render(mgl.TRIANGLES)` 来绘制图元

`render` 的参数是我们打算绘制的 OpenGL 图元的类型。由于我们在一开始时说过，我们希望绘制的是一个三角形，所以这里传递 `mgl.TRIANGLES` 给它

现在尝试运行，如果没有问题的话，你就能看到这样的结果，一个橘黄色的三角形

如果出现了任何错误，回头检查一下代码

如果你的输出和这个看起来不一样，你可能做错了什么，你可以查看一下源码，检查你是否遗漏了什么东西
