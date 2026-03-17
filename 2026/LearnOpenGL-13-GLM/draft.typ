#import "@preview/marginalia:0.3.1" as marginalia: note, notefigure, wideblock

#set page(margin: 0pt)

#show: marginalia.setup.with(
  inner: ( far: 5mm, width: 15mm, sep: 5mm ),
  outer: ( far: 20mm, width: 60mm, sep: 10mm ),
  // top: 2.5cm,
  // bottom: 2.5cm,
  // book: false,
  // clearance: 12pt,
)

#let sep = wideblock(line(length: 100%))

#let note = note.with(numbering: (..i) => h(2pt) + box(numbering("1", ..i), fill: blue.lighten(75%)) + h(2pt))

#set text(font: "Noto Serif CJK SC", lang: "zh", region: "cn")

#let tip = box.with(stroke: gray, inset: 6pt, radius: 4pt, width: 100%)

#let li = math.macron

#import "@preview/zebraw:0.6.1": *
#show: zebraw

#set page(numbering: "1")

现在我们已经解释了变换背后的所有理论，是时候将这些知识利用起来了。在 Python 中我们使用 `glm` 库就能很轻松地创建各种变换矩阵，包括我们刚刚讲的“缩放矩阵”“位移矩阵”“旋转矩阵”，还包括很多其它的，我们之后会介绍到。

为了使用 glm 库，我们用 `pip install pyglm` 安装一下，接着使用

```py
from pyglm import glm
```

便可以导入并使用了

我们来看看是否可以利用我们刚学的变换知识把一个向量 $vec(1, 0, 0)$ 位移 $vec(1, 1, 0)$ 个单位

```py
from pyglm import glm

vec = glm.vec4(1, 0, 0, 1)

trans = glm.mat4(1)
trans = glm.translate(trans, glm.vec3(1, 1, 0))

vec = trans * vec
print(vec)
```

这段代码分为这几个部分，先是定义向量，以及矩阵，最后是将矩阵作用到向量上并验证结果。

`glm` 的功能都可以通过 `glm.` 访问，这里我们使用 `glm.vec4` 创建一个 $vec(1, 0, 0)$ 向量，还记得前一节我们一直写的 $vec(x, y, z, 1)$ 吧，所以我们在这里也把齐次坐标设定为 $1$#note[用箭头指一下]

接下来使用 `glm.mat4` 定义一个 4x4 矩阵，这里传入 1 表示对角线用 1 填充，所以这里我们的 `trans` 是一个单位矩阵；下一步是使其成为一个位移矩阵，这里是通过传递给 `glm.translate` 函数来完成这个工作的，这里做的就是将你给出的矩阵，乘上位移矩阵，得到最终的矩阵。

最后，我们把矩阵作用到向量上，输出最后的结果，如果你仍记得位移矩阵是如何工作的，得到的向量应当是 $vec(1 + 1, 0 + 1, 0 + 0)$ 即 $vec(2, 1, 0)$，没错，它确实会输出这样的结果，这个位移矩阵确实符合我们预期。

#sep

我们来做些更有意思的事情，让我们来旋转和缩放之前那个教程中的“开心的箱子”

```py
trans = glm.mat4(1)
trans = glm.rotate(trans, glm.radians(90), glm.vec3(0, 0, 1))
trans = glm.scale(trans, glm.vec3(0.5, 0.5, 0.5))
```

这里我们能看到两个矩阵变换，一个是 `rotate`，旋转，另一个是 `scale`，缩放。

我们关注一下这两个函数的参数#note[边讲解边演示矩阵]：

- 对于 `rotate` 函数，也就是旋转，正如我们前面所说的，需要提供一个旋转角度以及旋转轴#note[高亮对应部分]。由于 GLM 使用弧度制的角度，所以我们使用 `glm.radians` 将 90 度角转化为弧度；由于我们现在是在二维 xy 平面上旋转，所以这里我们指定旋转轴为 $z$ 轴，即向量 $vec(0,0,1)$

- 对于 `scale` 函数，也就是缩放，传入一个向量表示在各个坐标方向#note[示意一下坐标方向]上的缩放倍率即可

需要留意的是，因为 `glm` 的这些函数是依次右乘的，所以当我们把最终的 `trans` 矩阵作用到向量上时，效果是先缩放（`scale`） 再旋转（`rotate`）#note[分别高亮矩阵示意以及代码]，和代码的顺序不同。

我们现在有了最终的矩阵 `trans`，下一个大问题是：如何把矩阵传递给着色器？我们之前接触过 GLSL 中的向量类型，`vec2` `vec3` `vec4`，同样，GLSL 中也有矩阵类型，即 `mat2` `mat3` `mat4`，这里我们使用 `mat4` 类型。

我们修改顶点着色器让其接收一个 `mat4` 类型的 `uniform` 变量，再用矩阵 uniform 乘以位置向量，然后在代码中设置这个 `uniform` 的矩阵值了。这里为了将 GLM 的矩阵传递作为 ModernGL 的 uniform 值，我们直接使用 `.write` 写入矩阵的字节数据即可。

我们总结一下上面做的事情，我们创建了一个变换矩阵，在顶点着色器中声明了一个 `uniform`，并把矩阵发送给了着色器，着色器会变换我们的顶点坐标，最后的结果应该看起来像这样

#align(center)[（实机演示）]

很好！我们的箱子向左侧旋转，并是原来的一半大小#note[在一旁附上前面的矩阵代码作为参照]，所以变换成功了。

#sep

我们现在做些更有意思的，看看我们是否可以让箱子随着时间旋转，同时顺便把箱子移到窗口的右下角。

要让箱子随着时间推移旋转，我们必须在渲染循环中更新变换矩阵，因为它在每一次渲染迭代中都要更新。我们使用 GLFW 的时间函数#note[高亮]来获取不同时间的角度

```py
trans = glm.mat4(1)
trans = glm.translate(trans, glm.vec3(0.5, -0.5, 0))
trans = glm.rotate(trans, glfw.get_time(), glm.vec3(0, 0, 1))
```

要记住的是，前面的例子中我们可以在任何地方声明变换矩阵，但是现在我们必须在每一次迭代中创建它，从而保证我们能够不断更新旋转角度。虽然我们每次都重新创建变换矩阵，但这是正常的，通常在渲染场景时，我们总会有多个变换矩阵，它们需要每帧用新值重新创建。

在这里我们先把箱子围绕原点 $(0,0,0)$ 旋转；之后，我们把旋转过后的箱子移到屏幕的右下角。

接下来运行代码，如果你做对了，你将看到这的结果：

#align(center)[（实机演示）]

我们做到了实现一个位移过的箱子，并且它会一直转，一个变换矩阵就做到了！现在你能感觉到为什么矩阵在图形领域是一个如此重要的工具了。我们可以定义无限数量的变换，而把他们组合为仅仅一个矩阵，并且如果愿意的话我们还可以重复使用它。在着色器中使用矩阵可以省去重新定义顶点数据的功夫，它也能够节省处理时间，因为我们没有一直重新发送我们的数据（这是个非常慢的过程）。

矩阵变换的组合非常丰富，在一开始可能需要一段时间来了解，只有不断地尝试和实验这些变换，你才能快速地掌握它们。

在后续的学习中，我们会讨论怎样使用矩阵为顶点定义不同的坐标空间，这将是我们进入实时 3D#note[读作三维] 图像的第一步！
