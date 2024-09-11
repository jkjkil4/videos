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

= 更多顶点属性（彩色三角形）

在前面的教程中，我们了解了如何填充 VBO、以及如何将着色器程序与 VBO 绑定为一个 VAO。这次，我们同样打算把颜色数据加进顶点数据中。我们将把颜色数据添加为 3 个 float 值到 `vertices` 数组中。

我们这样把三角形的三个角分别指定为红色、绿色和蓝色：

```py
vertices = np.array([
     # 位置            # 颜色
     0.5, -0.5, 0.0,  1.0, 0.0, 0.0,    # 右下
    -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,    # 左下
     0.0,  0.5, 0.0,  0.0, 0.0, 1.0     # 顶部
], dtype='f4')
```

由于现在有更多的数据要发送到顶点着色器，我们有必要去调整一下顶点着色器，使它能够多接受一个颜色值作为输入：

```glsl
#version 330 core

in vec3 in_vert;    // 输入一个位置
in vec3 in_color;   // 输入一个颜色

out vec3 v_color;   // 向片段着色器输出一个颜色

void main()
{
    gl_Position = vec4(in_vert, 1.0);
    v_color = in_color;
}
```

在顶点着色器这里，我们将 `v_color` 直接设置为从顶点数据那里得到的输入颜色

在片段着色器这里，我们不再使用 uniform 来传递片段的颜色了，而是使用从顶点着色器传递过来的 `v_color`：

```glsl
#version 330 core

in vec3 v_color;

out vec4 FragColor;

void main()
{
    FragColor = vec4(v_color, 1.0);
}
```

因为我们添加了另一个顶点属性，并且更新了 VBO 的内存，我们必须更改一下 VAO 中关于顶点属性绑定的声明：

```py
vao = ctx.vertex_array(prog, vbo, 'in_vert', 'in_color')
```

可以发现，这里我们加了一个对 `in_color` 属性的绑定，这表明将顶点数据传递给顶点着色器时，首先读取一个位置属性，然后再读取一个颜色属性，作为一个顶点的输入，再依照这样的方式读取完三个顶点的属性。

这样顶点着色器就能正确的读取我们的顶点数据，运行程序，你应该会看到这样的结果：（录屏）

如果出现了什么问题，你可以参考这节的源代码：（贴链接）

#line(length: 100%, stroke: gray)

这个三角形可能与你想象的有点不同，因为我们只提供了三个颜色，而不是我们现在看到的大调色板。

这是在片段着色器中进行所谓片段插值的结果。当渲染一个三角形时，光栅化阶段通常会造成比原指定顶点更多的片段，光栅会根据每个片段相对于三角形形状的相对位置，插值片段着色器的所有输入变量（对，所有，无论是颜色还是位置或者是你传递的某个向量），这也就导致了这个三角形的三个顶点是我们设置的三个颜色，而中间的部分是这三个颜色的过渡。
