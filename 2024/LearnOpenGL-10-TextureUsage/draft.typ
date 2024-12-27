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

== 加载与创建纹理

我们介绍完了纹理的基本知识，了解了纹理环绕方式、纹理过滤以及多级渐远纹理。

现在我们编写实际代码，加载图像并创建 OpenGL 纹理对象。

图像有多种格式，常见的有 ".jpg" ".png" 等格式，在这里我们使用 pillow 库来读取。

我们首先要在命令行里使用

```sh
pip install pillow
```

来安装 pillow 库，安装后我们便在代码的开头加上

```py
from PIL import Image
```

来导入 pillow 库中图像相关的功能。

下面的教程中，我们会使用一张木箱的图片（请从简介该节的链接中查找），将其和代码文件放到一个目录中，使用

```py
img = Image.open("container.jpg")
```

来载入这个木箱的图像，我们可以通过 `img.size` 得到一个元组（也就是包含了两个值的序列），它表示这个图像的宽高；以及 `img.tobytes()` 得到图像的字节数据，这样可以方便我们传递给 OpenGL。

接着，使用

```py
texture = ctx.texture(img.size, components=3, data=img.tobytes())
```

便可以创建一个 OpenGL 纹理对象。这里我们给 `ctx.texture` 传递 `img.size` 告诉 OpenGL 这个纹理的尺寸，传递 `components=3` 表明这是使用三分量的 `RGB` 形式存储的图像数据，接着便是传递 `img.tobytes()` 将图像数据提供给它。

#note[
  注意，这里我们本身就已经是以 `RGB` 的形式载入图像，因此不用额外的转换，对于其它的，例如带透明度通道的 `.png` `RGBA` 图像，你可以选择对不同的图像配置不同的 components，或者使用类似于 `.convert('RGBA')` 的方式把图像都统一成一种格式
]

此时，只有基本级别(Base-level)的纹理图像被加载了，如果要使用多级渐远纹理，我们需要使用 `texture.build_mipmaps()` 来生成它们，这会为这个纹理自动生成所有需要的多级渐远纹理。

== 应用纹理

后面的这部分我们会使用 `第6节 索引缓冲对象` 中最后一部分使用索引缓冲对象(IBO)绘制矩形的代码，你可以把那个代码复制进来（贴个链接），我们以这个为基础来给这个矩形附着上纹理渲染。

为了渲染纹理，我们需要告知 OpenGL 如何采样纹理，所以我们必须更新顶点数据，加上纹理坐标：

```py
# 顶点数据
vertices = np.array([
#   ----- 位置 -----   - 纹理坐标 -
      0.5,  0.5, 0.0,  1.0, 1.0,   # 右上
      0.5, -0.5, 0.0,  1.0, 0.0,   # 右下
    -0.5, -0.5, 0.0,  0.0, 0.0,   # 左下
    -0.5,  0.5, 0.0,  0.0, 1.0    # 左上
], dtype='f4')
```

由于我们添加了额外的新顶点属性，我们必须向 OpenGL 注明我们新的顶点格式：

```py
vao = ctx.vertex_array(prog, vbo, 'in_vert', 'in_texcoord', index_buffer=ibo)
```

接着我们需要调整顶点着色器使其能够接受这两个顶点属性，并把坐标传递给片段着色器：

```glsl
#version 330 core

in vec3 in_vert;
in vec2 in_texcoord;

out vec2 v_texcoord;

void main()
{
    gl_Position = vec4(in_vert, 1.0);
    v_texcoord = in_texcoord;
}
```

片段着色器也应该能访问纹理对象，但是我们怎样才能做到这一点呢？

GLSL 有一个供纹理对象使用的内建数据类型，叫做采样器(Sampler)，它以纹理类型作为后缀，比如 `sampler1D`、`sampler3D`，或在我们的例子中的 `sampler2D`。

我们可以简单声明一个 `uniform sampler2D` 把一个纹理添加到片段着色器中，稍后我们会把纹理赋值给这个 uniform：

```glsl
#version 330 core

in vec2 v_texcoord;

uniform sampler2D ourTexture;

out vec4 FragColor;

void main()
{
    FragColor = texture(ourTexture, v_texcoord);
}
```

我们使用 GLSL 内置的 `texture` 函数来采样纹理的颜色，它第一个参数是纹理采样器，第二个参数是对应的纹理坐标。`texture` 函数会使用之前设置的纹理参数对响应的颜色值进行采样。这个片段着色器的输出就是，插值后的纹理坐标上，经过纹理过滤后的颜色。

#p(0)[
  中间显示一列的位置值，左边 Python 对象，右边 GLSL uniform
]

现在只剩下在绘制之前绑定纹理了，我们将 GLSL 中的这个纹理 uniform 和 Python 中的#pin(0)这个纹理对象都绑定到位置 0 上，这样我们就标识了片段着色器中会使用到的这个纹理对象。

如果你跟着这个教程正确地做完了，运行程序就会看到这样的图像：（录屏）

如果你的矩形是全黑或全白的，你可以检查一下有没有哪写错了，或者对照一下我提供的参考代码（贴链接）

// #note[
//   ？如果你的纹理代码不能正常工作或者显示是全黑，请继续阅读，并一直跟进我们的代码到最后的例子，它是应该能够工作的。在一些驱动中，必须要对每个采样器uniform都附加上纹理单元才可以，这个会在下面介绍。
// ]

我们还可以把得到的纹理颜色与顶点颜色混合，来获得更有趣的效果。我们这里再给每个顶点传入一个颜色属性：

#{
  set text(size: 0.8em)
  ```py
  # 顶点数据
  vertices = np.array([
  #   ----- 位置 -----  ---- 颜色 ----   - 纹理坐标 -
       0.5,  0.5, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0,   # 右上
       0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,   # 右下
      -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0,   # 左下
      -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0    # 左上
  ], dtype='f4')
  ```
}

当然，我们还要注明新的顶点格式：

```py
vao = ctx.vertex_array(prog, vbo, 'in_vert', 'in_color', 'in_texcoord', index_buffer=ibo)
```

更新顶点着色器与片段着色器：

```glsl
#version 330 core

in vec3 in_vert;
in vec3 in_color;
in vec2 in_texcoord;

out vec3 v_color;
out vec2 v_texcoord;

void main()
{
    gl_Position = vec4(in_vert, 1.0);
    v_color = in_color;
    v_texcoord = in_texcoord;
}
```

```glsl
#version 330 core

in vec3 v_color;
in vec2 v_texcoord;

uniform sampler2D ourTexture;

out vec4 FragColor;

void main()
{
    FragColor = texture(ourTexture, v_texcoord) * vec4(v_color, 1.0);
}
```

这里我们只需把纹理颜色与顶点颜色在片段着色器中相乘来混合二者的颜色：

```glsl
FragColor = texture(ourTexture, v_texcoord) * vec4(v_color, 1.0);
```

最终运行的效果应当会得到顶点颜色和纹理颜色的混合色：（录屏）

我猜你会说我们的箱子喜欢跳70年代的迪斯科。（这句话用 LearnOpenGL-CN 网页录屏放吧）

== 纹理单元

在前面，我们向 GLSL 中的纹理 uniform 和 Python 中的纹理对象都绑定了位置 0，这样它们就关联了起来。

一个纹理的位置值通常称为一个纹理单元(Texture Unit)，纹理单元的主要目的是让我们通过分别绑定不同的位置值，以便在着色器中可以使用多于一个的纹理。

#note[
  OpenGL 至少保证有 16 个纹理单元供你使用，也就是说你可以使用从 0 到 15 的位置值。
]

当我们需要同时使用两个纹理时，我们编辑片段着色器来接收另一个采样器：

```glsl
#version 330 core

in vec2 v_texcoord;

uniform sampler2D texture1;
uniform sampler2D texture2;

out vec4 FragColor;

void main()
{
    FragColor = mix(texture(texture1, v_texcoord), texture(texture2, v_texcoord), 0.2);
}
```

最终输出颜色现在是两个纹理的结合。

GLSL 内置的 `mix` 函数需要接受两个值作为参数，并对它们根据第三个参数进行线性插值。如果第三个值是 `0.0`，它会返回第一个输入；如果是 `1.0`，会返回第二个输入值。`0.2` 会返回 80% 的第一个输入颜色和 20% 的第二个输入颜色，即返回两个纹理的混合色。

我们现在需要载入并创建另一个纹理，这里我们使用一张“你学习 OpenGL 时的面部表情”图片。注意这个图片是 `.png` 格式的，它还带有一个alpha不透明度通道，我们需要使用 `components=4` 来注明这点，表明它的像素是用 `RGBA` 形式存储的。

与绑定第一个纹理的过程类似

```py
prog['texture1'] = 0
texture1.use(0)
```

第二个纹理可以使用这样的代码

```py
prog['texture2'] = 1
texture2.use(1)
```

完成这些之后，运行程序应该就能看到这样的效果：（录屏）

你可能注意到纹理上下颠倒了！这是因为 OpenGL 要求 y 轴 `0.0` 坐标是在图片的底部的，但是图片的 y 轴 `0.0` 坐标通常在顶部。

为了解决这点，我们可以直接翻转图像的 `y` 轴：`.transpose(Image.FLIP_TOP_BOTTOM)`

如果你看到了一个开心的箱子，你就做对了。你可以对比一下源代码（贴链接）。

前面提到使用 `.transpose` 翻转图像是 LearnOpenGL 中的方法，我不太喜欢这种，我们把前面的 `.transpose` 先删了，其实对调纹理坐标的 `y` 轴也能达到同样的方式，对吧？我更喜欢这种方式
