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

= 纹理

我们已经了解到，可以为每个顶点添加颜色来增加图形的细节，从而创建出有趣的图像。但是，如果想让图形看起来更真实，我们就必须有足够多的顶点，从而指定足够多的颜色。这将会产生很多额外开销，因为每个模型都会需求更多的顶点，每个顶点又需求一个颜色属性。

艺术家和程序员更喜欢使用纹理(Texture)。纹理是一个2D图片（甚至也有1D和3D的纹理），它可以用来添加物体的细节。

你可以想象纹理是一张绘有砖块的纸，无缝折叠贴合到你的3D的房子上，这样你的房子看起来就像有砖墙外表了。因为我们可以在一张图片上插入非常多的细节，这样就可以让物体非常精细而不用指定额外的顶点。

#note[
  除了图像以外，纹理也可以被用来储存大量的数据，这些数据可以发送到着色器上，但是这不是我们现在的主题。
]

== 纹理坐标

你会看到这是之前教程的那个三角形贴上了一张砖墙图片

#image("brick-triangle.png")

为了能够把纹理贴到三角形上，我们需要指定三角形的每个顶点各自对应纹理的哪个部分。这样每个顶点就会关联着一个纹理坐标(Texture Coordinate)，用来标明该从纹理图像#pin(0)的哪里采样颜色。

#p(0)[
  左边放原纹理，右边放纹理三角形，示意一下纹理映射
]

#pagebreak()

纹理坐标在x和y轴上，范围在0到1之间（注意我们使用的是2D纹理图像）。使用纹理坐标获取纹理颜色叫做采样(Sampling)#pin(1)。

#lp(1, offset-dy: -2pt, body-dy: -10pt)[
  先放一个坐标出来，然后指出这个坐标在纹理上的颜色
]

纹理坐标起始于 $(0, 0)$，也就是纹理图片的左下角，终止于 $(1, 1)$，即纹理图片的右上角#pin(2)。

#p(2)[
  从 $(0,0)$ 向两个方向发射线，汇聚到 $(1,1)$
]

配置在纹理坐标中的三个点后，我们就可以将纹理中的这块部分附着到最终显示出的三角形中，当我们改变纹理坐标中的这三个点，所附着的内容也会发生变化。

现在这个例子中，我们把三角形左下角顶点的纹理坐标设置为 $(0,0)$，这样它就能对应纹理的左下角；同理将右下方的顶点设置为 $(1,0)$；上顶点的坐标设置为 $(0.5, 1.0)$ 对应纹理的上中位置。

纹理坐标看起来就像这样：

```py
tex_coords = np.array([
    0.0, 0.0,   # 左下角
    1.0, 0.0,   # 右下角
    0.5, 1.0    # 上中
], dtype='f4')
```

我们只要给顶点着色器传递这三个纹理坐标就行了，在片段插值的帮助下，我们的三个顶点会经过插值后传入片段着色器，产生三角形区域内每个点的纹理坐标信息。

纹理采样可以采用几种不同的插值方式，所以我们需要自己告诉 OpenGL 该怎样对纹理采样。

接下来我们会认识与纹理有关的几个配置选项，我们先从“纹理环绕方式开始”

== 纹理环绕方式

纹理坐标的范围通常是从 $(0,0)$ 到 $(1,1)$，那如果我们把纹理坐标设置在范围之外会发生什么#pin(0)？

#p(0)[
  拉远镜头，范围之外放几个问号
]

OpenGL 默认的行为是重复这个纹理图像，也就是忽略浮点纹理坐标的整数部分。但 OpenGL 也提供了更多的选择

默认的是 `GL_REPEAT`，它会重复纹理图像。

这里我为了辨识度把外面的部分减淡了，实际情况中它们并没有变淡。

还有 `GL_MIRRORED_REPEAT`，和之前一样，但每次重复图片是镜像放置的

以及 `GL_CLAMP_TO_EDGE`，纹理坐标会被约束在0到1之间，超出的部分会重复纹理坐标的边缘，产生一种边缘被拉伸的效果。

最后是 `GL_CLAMP_TO_BORDER`，超出的坐标变为用户指定的边缘颜色。

#{
  set text(size: 0.8em)
  table(
    columns: (auto, 1fr)
  )[
    *环绕方式*
  ][
    *描述*
  ][
    `GL_REPEAT`
  ][
    对纹理的默认行为。重复纹理图像。
  ][
    `GL_MIRRORED_REPEAT`
  ][
    和 `GL_REPEAT` 一样，但每次重复图片是镜像放置的。
  ][
    `GL_CLAMP_TO_EDGE`
  ][
    纹理坐标会被约束在0到1之间，超出的部分会重复纹理坐标的边缘，产生一种边缘被拉伸的效果。
  ][
    `GL_CLAMP_TO_BORDER`
  ][
    超出的坐标为用户指定的边缘颜色。
  ]
}

在默认的情况下是 `GL_REPEAT`，这种行为下，OpenGL 会在超出的部分一直重复纹理图像。

比如这张“前进中的玛德琳”，当我们把右边这个纹理顶点继续向右挪，我们就能在右边再次看到玛德琳的身影。

刚刚讲的这几个是 OpenGL 中的标识，在 ModernGL 中，我们通过纹理的 `.repeat_x` 和 `.repeat_y` 进行控制，这也意味着你可以对纹理的两个方向分别设置重复方式。

他们默认都是 `True`，当你把对应方向的行为设置为 `False` 后，超出的部分会重复边缘的颜色，产生一种边缘被拉伸的效果，这也就是对应 `GL_CLAMP_TO_EDGE` 的行为。

上面提到的这两种行为是最为常见的，可以直接用 `.repeat_x` 和 `.repeat_y` 进行控制。

我们先不展开具体如何使用其余的两种行为了，`GL_CLAMP_TO_BORDER` 需要使用 `ctx.sampler` 进行配置，并且很遗憾的是，ModernGL 暂未支持 `GL_MIRRORED_REPEAT` 的配置。

== 纹理过滤

纹理坐标不依赖于分辨率/*(Resolution)*/，它可以是任意浮点值，所以 OpenGL 需要知道怎样通过这个纹理坐标合理地获取纹理像素#pin(0)。

#lp(0, scale: 1.5)[
  展示纹理坐标的一个点变换到包裹一个纹理像素的矩形
]

所以，OpenGL 提供了对于纹理过滤(Texture Filtering)的选项。纹理过滤有很多个选项，但是现在我们只讨论最重要的两种：`mgl.NEAREST` 和 `mgl.LINEAR`。

`mgl.NEAREST`（也叫临近过滤，Nearest Neighbor Filtering）是 OpenGL 默认的纹理过滤方式。当设置为 `mgl.NEAREST` 的时候，OpenGL 会选择中心点最接近纹理坐标的那个像素。可以观察这里我们移动纹理坐标时，所使用的纹理像素的变动。

`mgl.LINEAR`（也叫线性过滤，(Bi)linear Filtering）它会基于纹理坐标附近的纹理像素，计算出一个插值，近似出这些纹理像素之间的颜色。当一个纹理像素的中心距离纹理坐标越近，那么这个纹理像素的颜色对最终的样本颜色的贡献越大。你会看到在大多数情况下返回的颜色是邻近像素的混合色。

那么这两种纹理过滤方式有怎样的视觉效果呢？让我们看看在一个很大的物体上应用一张低分辨率的纹理会发生什么吧（因为这样可以使得纹理被充分地放大，每个纹理像素都能看大）

`mgl.NEAREST` 产生了颗粒状的团，我们能够清晰看到组成纹理的像素，而 `mgl.LINEAR` 能够产生更平滑的图案，更难看出单个的纹理像素。

相比而言，`mgl.LINEAR` 可以产生更真实的输出，但有些开发者更喜欢 8-bit 风格，所以他们会用 `mgl.NEAREST` 选项，这取决于特定的需求。

当进行缩小和放大操作的时候可以设置纹理过滤的选项，比如你可以在纹理被缩小的时候使用邻近过滤，被放大时使用线性过滤#pin(0)。

#lp(0)[
  左边放一个原大小的图，示意一下缩小和放大
]

这种操作我们需要使用

```py
texture.filter = (mgl.NEAREST, mgl.LINEAR)
```

来配置，前一个表示缩小时的处理方式，后一个表示放大时的过滤方式

== 多级渐远纹理

假设我们有一个包含很多物体的大房间，每个物体上都有纹理。

有些物体会很远，但其纹理会拥有与近处物体同样高的分辨率。由于远处的物体可能只产生很少的片段，OpenGL 从高分辨率纹理中为这些片段获取正确的颜色值就很困难，因为它需要对一个跨过纹理很大部分的片段只拾取一个纹理颜色。在小物体上这会产生不真实的感觉，更不用说它们使用高分辨率纹理时浪费内存带宽的问题了。

OpenGL 使用一种叫做多级渐远纹理(Mipmap)的概念来解决这个问题，它简单来说就是预先生成一系列的纹理图像，后一个纹理图像的大小是前一个的二分之一。

多级渐远纹理背后的理念很简单：距观察者的距离超过一定的阈值，OpenGL 会切换为其中特定尺寸的纹理，即最适合物体的距离的那个。#pin(1)由于距离远，解析度不高也不会被用户注意到。

#p(1)[
  右边的物体不断缩小，左边的多级渐远纹理相应切换
]

同时，多级渐远纹理另一加分之处是它的性能非常好。多级渐远纹理放在一起是长这个样子的：

#image("mipmaps.png")

手工为每个纹理图像创建一系列多级渐远纹理很麻烦，幸好 OpenGL 提供了直接生成多级渐远纹理的方式，我们直接使用

```py
texture.build_mipmaps()
```

就好了

在创建完一个纹理后调用它，OpenGL 就会承担接下来的所有工作了。后面的教程中你会看到该如何使用它。

在渲染中切换多级渐远纹理级别(Level)时，OpenGL 在两个不同级别的多级渐远纹理层之间会产生不真实的硬边界。

就像普通的纹理过滤一样，切换多级渐远纹理级别时你也可以在两个不同多级渐远纹理级别之间使用 `NEAREST` 和 `LINEAR` 过滤，这个标识（`mgl.LINEAR_MIPMAP_NEAREST`）的前半部分对应之前提到的纹理内的过滤方式，后半部分就是我们现在正在说的多级渐远纹理间的过滤方式。如果我们把后半部分改成 `LINEAR`，那么就会在两个多级渐远纹理之间进行线性插值，从而消除切换纹理时的突变。

显然，这个配置的前后两部分分别有两种选择，你就可以排列组合得到这四种纹理过滤方式：

#{
  set text(size: 0.8em)
  table(
    columns: (auto, 1fr)
  )[
    `mgl.NEAREST_MIPMAP_NEAREST`
  ][
    使用邻近插值进行纹理内的采样；使用最邻近的多级渐远纹理级别
  ][
    `mgl.LINEAR_MIPMAP_NEAREST`
  ][
    使用线性插值进行纹理内的采样；并使用最邻近的多级渐远纹理级别
  ][
    `mgl.NEAREST_MIPMAP_LINEAR`
  ][
    使用邻近插值进行纹理内的采样；在两个多级渐远纹理之间进行线性插值
  ][
    `mgl.LINEAR_MIPMAP_LINEAR`
  ][
    使用线性插值进行纹理内的采样；在两个多级渐远纹理之间使用线性插值
  ]
}

和前面设置纹理过滤的方式一样

```py
texture.filter = (mgl.LIENAR, mgl.LINEAR)
```

我们通过类似这样

```py
texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
```

的方式来设置多级渐远纹理的纹理过滤方式。

// 如果你对这段纹理过滤与多级渐远纹理的配置感到有点吃力，这里我推荐 \@phu004 的一期视频 https://www.bilibili.com/video/BV1N94y1b7DQ/

记得这里前面一个是配置缩小时的过滤选项，后面一个是放大时的过滤选项。

#note[
  一个常见的错误是，将放大过滤的选项设置为多级渐远纹理的选项之一。这样没有任何效果，因为多级渐远纹理主要是使用在纹理被缩小的情况下的，纹理放大不会使用多级渐远纹理。
]

== 加载与创建纹理

我们介绍完了纹理的基本知识，了解了纹理环绕方式、纹理过滤以及多级渐远纹理。

现在我们编写实际代码，加载图像并创建 OpenGL 纹理对象。

图像有多种格式，常见的有 ".jpg" ".png" 等格式，我们并不想为每一种格式都自己写一份解析的方式，另一个更好的选择是使用现成的图像读取库，在这里我们使用 pillow 库。

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

便可以创建一个 OpenGL 纹理对象。这里我们给 `ctx.texture` 传递 `img.size` 告诉 OpenGL 这个纹理的尺寸，传递 `components=3` 表明这是使用三分量的 `RGB` 形式存储的图像数据，接着便是传递 `img.tobytes()` 将图像数据提供给它，这就使得该纹理对象附加上了我们想要表示的图像。

#note[
  注意，这里我们载入的本身就已经是 `RGB` 格式的图像，因此不用额外的转换，对于其它的，例如带透明度通道的 `.png` `RGBA` 图像，你可以选择对不同的图像配置不同的 components，或者使用类似于 `.convert('RGBA')` 的方式把图像都统一成一种格式
]

此时，只有基本级别(Base-level)的纹理图像被加载了，如果要使用多级渐远纹理，我们需要使用 `texture.build_mipmaps()` 来生成它们，这会为这个纹理自动生成所有需要的多级渐远纹理。

== 应用纹理

后面的这部分我们会使用 `第6节 索引缓冲对象` 中最后一部分使用索引缓冲对象(IBO)绘制矩形的代码，你可以把那个代码复制进来（贴个链接），我们以这个为基础来给这个矩形附着上纹理渲染。

为了渲染纹理，我们需要告知 OpenGL 如何采样纹理，所以我们必须使用纹理坐标更新顶点数据：

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

如果你的矩形是全黑或全白的，你可以检查一下，或者对照一下我提供的参考代码（贴链接）

#note[
  ？如果你的纹理代码不能正常工作或者显示是全黑，请继续阅读，并一直跟进我们的代码到最后的例子，它是应该能够工作的。在一些驱动中，必须要对每个采样器uniform都附加上纹理单元才可以，这个会在下面介绍。
]

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

还有一种解决上下颠倒的方式是调整一下纹理坐标，其实我更青睐这种方式（）
