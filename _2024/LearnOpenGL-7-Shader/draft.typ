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
#show raw: set text(font: ("Consolas", "Noto Sans S Chinese"), cjk-latin-spacing: none)

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

= 着色器

在“你好，三角形”这节的教程中提到，着色器(Shader)是运行在 GPU 上的小程序。这些小程序作为图形渲染管线的某个特定部分而运行。

从基本意义上来说，着色器只是一种把输入转化为输出的程序。着色器也是一种非常独立的程序，因为它们之间不能相互通信；它们之间唯一的沟通只有通过输入和输出。

前面的教程里我们简要地触及了一点着色器的皮毛，并了解了如何恰当地使用它们。现在我们会用一种更加广泛的形式详细解释着色器，特别是 OpenGL 着色器语言，也就是 GLSL。

== GLSL

着色器是使用一种类似C语言，叫作 GLSL 的语言写成的。GLSL 是为图形计算量身定制的，它包含一些针对向量和矩阵操作的有用特性。

```glsl
#version version_number

in 类型 输入变量名;
in 类型 输入变量名;

out 类型 输出变量名;

uniform 类型 uniform名;

void main()
{
    // 处理输入并进行一些图形操作
    ...
    // 输出处理过的结果到输出变量
    输出变量名 = 经过各种乱七八糟处理后得到的东西;
}
```

着色器的开头总是要声明版本，接着是输入变量和输出变量，以及 uniform 和 main 函数。每个着色器的入口点都是 main 函数，在这个函数中我们处理所有的输入变量，并将结果输出到输出变量中。如果你不知道什么是 uniform 也不用担心，我们后面会进行讲解。

== 数据类型

和其它编程语言一样，GLSL 有数据类型来指定变量的种类。

#p(0)[
  用箭头指出它们的中文含义，不用读出来
]

GLSL 中包含 C 等其它语言大部分的基础数据类型：`float`、`double`、`int`、`uint` 和 `bool`。#pin(0)

GLSL 也有两种容器类型，它们会在这个教程中使用很多，分别是向量(Vector)和矩阵(Matrix)，其中矩阵我们会在之后的教程里再讨论，现在我们先介绍一下 GLSL 中的向量类型。

=== 向量

GLSL 中的向量是一个可以包含 2、3 或者 4 个分量的容器，分量的类型可以是前面默认基础类型的任意一个。

比如我们在之前绘制三角形的时候提到的，`vecn` 就是包含 `n` 个 float（浮点数）分量的向量，例如 `vec2` 就是包含 2 个浮点数分量，`vec3` 就是包含 3 个。

同样的，还有 `dvecn`、`ivecn`、`uvecn` 和 `bvecn` 分别对应不同数据类型的向量，根据需要使用即可，但是这些类型的向量中，我们最常用到的还是包含浮点数类型的 `vecn`。

一个向量的分量可以通过 `vec.x` 这种方式获取，这里 `x` 是指这个向量的第一个分量。你可以分别使用 `.x`、`.y`、`.z` 和 `.w` 来获取它的第 1、2、3、4 个分量。GLSL 也允许你对颜色使用 `rgba`，或是对纹理坐标使用 `stpq` 访问相同的分量。

#note[
  无论你使用 `xyzw`、`rgba` 还是 `stpq` 获取分量，它们在本质上是没有区别的，你可以把它们看成是一种别名。
]

向量这一数据类型也允许一些有趣而灵活的分量选择方式，叫做重组(Swizzling)。重组允许这样的语法：

```glsl
vec2 someVec;
vec4 differentVec = someVec.xyxx;
vec3 anotherVec = differentVec.zyw;
vec4 otherVec = someVec.xxxx + anotherVec.yxzy;
```

你可以使用上面 4 个字母任意组合来创建一个同类型的新向量。

并且也可以把一个向量作为一个参数传给不同的向量构造函数，以减少需求参数的数量：

```glsl
vec2 vect = vec2(0.5, 0.7);
vec4 result = vec4(vect, 0.0, 0.0);
vec4 otherResult = vec4(result.xyz, 1.0);
```

比如说下面这段第二行 `result` 向量的构造，`vect` 本身已经是一个 `vec2` 向量了，所以我们只需要再填入两个分量，就可以完成 `vec4` 向量的构造。

必要的话你可以暂停来观察一下这几行代码是#pin(0)如何起作用的。

#p(0)[
  显示暂停进度条
]

向量是一种灵活的数据类型，我们可以把它用在各种输入和输出上。在教程中你也可以看到很多新颖的管理向量的例子。

== 输入与输出

虽然着色器是各自独立的小程序，但是它们都是一个整体的一部分，出于这样的原因，我们希望每个着色器都有输入和输出，这样才能进行数据交流和传递。

GLSL 定义了 `in` 和 `out` 关键字专门来实现这个目的。每个着色器使用这两个关键字设定输入和输出。//，只要一个输出变量与下一个着色器阶段的输入匹配，它就会传递下去。但在顶点和片段着色器中会有点不同。


顶点着色器应当接收的是一种特殊形式的输入，否则就会效率低下。它的特殊之处在于，它从顶点数据中直接接收输入，就像之前我们使用 `in_vert` 来绑定顶点数据和顶点着色器的输入一样。

顶点着色器的每个输入变量也叫顶点属性(Vertex Attribute)。我们能声明的顶点属性是有上限的，它一般由硬件来决定。OpenGL确保至少有16个包含4分量的顶点属性可用，但是有些硬件或许允许更多的顶点属性，你可以查询 GL_MAX_VERTEX_ATTRIBS 来获取具体的上限：

```py
import moderngl

ctx = moderngl.create_standalone_context()
print(ctx.info['GL_MAX_VERTEX_ATTRIBS'])
```

直接运行这一小段代码，通常情况下它至少会返回16个，大部分情况下够用了。

#note[
  在 C++ 传递 OpenGL 顶点属性可能更倾向于使用类似于 `layout (location = 0)`  的标识符，但是这里我们使用 ModernGL 推荐的方式
]

另一个例外是片段着色器，它需要一个 `vec4` 颜色输出变量，因为片段着色器需要生成一个最终输出的颜色。

嗯，只要这个变量是一个 `vec4` 类型的就行了，命名无所谓。

如果你在片段着色器没有定义输出颜色，OpenGL 会把你的物体渲染为黑色（或白色）。

这两个过程是输入和输出中的例外情况，他们是渲染管线从外部获取输入，以及将结果传递出去的过程。

当我们打算从一个着色器向另一个着色器发送数据时，我们必须在发送方着色器中声明一个输出，在接收方着色器中声明一个类似的输入。当类型和名字都一样的时候，OpenGL 就会把两个变量链接到一起，它们之间就能发送数据了。

为了展示这具体是如何工作的，我们会稍微改动一下《你好，三角形》那节的着色器，让顶点着色器为片段着色器决定颜色。

*顶点着色器*

```glsl
#version 330 core

in vec3 in_vert;

out vec4 v_color; // 指定一个传递给片段着色器的输出

void main()
{
    gl_Position = vec4(in_vert, 1.0); // 注意我们把一个 vec3 作为 vec4 构造器的参数，这样就会比之前更简洁（这句注释好像有点长，不在视频里出现了）
    v_color = vec4(0.5, 0.0, 0.0, 1.0); // 把输出变量设置为暗红色
}
```

*片段着色器*

```glsl
#version 330 core

in vec4 v_color;  // 从顶点着色器传来的输入变量（名称相同，类型相同）

out vec4 FragColor;

void main()
{
    FragColor = v_color;
}
```

因为前面介绍了“重组语法”，所以这里我们把一个 `vec3` 作为 `vec4` 构造器的参数，这样就会比之前更简洁。

你可以看到我们在顶点着色器中声明了一个 `v_color` 作为 `vec4` 输出，并在片段着色器中声明了一个类似的 `v_color`，由于它们名字相同且类型相同，片段着色器中的 `v_color` 就和顶点着色器中的 `v_color` 链接了。

#note[
  这里的命名是随意的，只是我习惯把“顶点(#strong[V]ertex)着色器传递出去的东西”加上 `v_` 的前缀。
]

由于我们在顶点着色器中将颜色设置为暗红色，最终的片段也是暗红色的，所以我们运行程序就会有这样的结果：（录屏）

这一部分的代码放在这个链接里了，有什么问题的话可以参考（贴链接）

这样我们成功地从顶点着色器向片段着色器发送了数据。让我们更上一层楼，看看能否从应用程序中直接给片段着色器发送一个颜色！

== Uniform

Uniform 是另一种从我们的应用程序在 CPU 上传递数据到 GPU 上的着色器的方式，但 uniform 和顶点数据有些不同。首先，uniform 是全局的，它可以被着色器程序的任意着色器阶段访问。其次，无论你把 uniform 值设置成什么，uniform 会一直保存他们的数据，直到它们被重置或更新。

要在 GLSL 中声明 uniform，我们只需在着色器中使用 `uniform` 关键字，并带上类型和名称。这样我们就可以在着色器中使用新声明的 uniform。

我们这次来试着通过 uniform 设置三角形的颜色：

```glsl
#version 330 core

uniform vec4 ourColor;   // 在Python代码中设定这个变量

out vec4 FragColor;

void main()
{
    FragColor = ourColor;
}
```

我们在片段着色器中声明了一个 uniform `vec4` 的 `ourColor`，并把片段着色器的输出颜色设置为 uniform 值的内容。因为 uniform 是全局变量，我们可以在任何着色器中定义它们，而无需通过顶点着色器作为中介传递过来。由于这里我们的顶点着色器用不到这个 uniform，所以我们不在那里定义它，只在片段着色器这里定义。

#note[
  如果你声明了一个 uniform 却在 GLSL 代码中没用过，编译器会静默移除这个变量，导致最后编译出的版本中并不会包含它，这可能导致几个非常麻烦的错误，记住这点！
]

这个 uniform 现在还是空的，我们还没有给他添加任何数据，我们在 Python 代码中这样就可以设置着色器程序的 uniform 值了：

```py
prog['ourColor'] = (0.5, 0.0, 0.0, 1.0)
```

这和前面一样，会显示一个暗红色的三角形（录屏）。

为了让它有趣一点，现在我们让它随着时间改变颜色：

```py
time_value = glfw.get_time()
green_value = (math.sin(time_value) / 2.0) + 0.5
prog['ourColor'] = (0.0, green_value, 0.0, 1.0)
```

我们通过 `glfw.get_time()` 获取运行的秒数，然后我们使用 `sin` 函数让绿色在 0.0 到 1.0 之间改变，并且将其传递给叫作 `ourColor` 的 uniform。#pin(1)

我们把这段放进渲染循环中，就可以在每一次迭代中更新这个 uniform，这样就会使得这个三角形动态地改变颜色。

这里使用了 `math.sin` 记得在文件开头导入一下 `math` 库，这是自带的，不用另外安装

在绘制三角形前更新 uniform 的值，如果你正确更新了，你会看到你的三角形逐渐由绿变黑再变回绿色：（录屏）

如果你在哪遇到了问题，可以参考一下这节的源码（贴链接）
