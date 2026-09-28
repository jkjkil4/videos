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

#let legacy(body) = {
  set text(gray)
  body
}

#let li = math.macron

#import "@preview/zebraw:0.6.1": *
#show: zebraw

#set page(numbering: "1")

我们先来一个简单的例子，先展示箱子的一个面，我们最终需要让这个面显示到摄像机画面上，也就是将这个面的三维坐标，转换到画面上的二维坐标。

#note[接下来的部分，跟随流程图块进行演示]
在开始进行 3D#note[读作三维] 绘图时，我们首先在 Python 中创建一个模型矩阵。这个模型矩阵包含了位移、缩放与旋转操作，他们会被应用到物体的所有顶点上，以*变换*它们到全局的世界空间。让我们变换一下我们的平面，将其绕着 x 轴旋转，使它看起来像放在地上一样。这个模型矩阵看起来是这样的：

```python
model = glm.mat4(1)
model = glm.rotate(model, glm.radians(-55.0), glm.vec3(1.0, 0.0, 0.0))
```#note[在画面上简单标注一下 rotate 各个部分的含义]

通过将顶点坐标乘以这个模型矩阵，我们将该顶点坐标变换到『世界坐标』，我们的这个面看起来就像是倒下去了一些似的。

接下来我们需要创建一个观察矩阵。#note[这里让摄像机出现在原点]我们想要在场景里稍微往后移动#note[将摄像机往后移动的动画]，以使得物体变成可见的。要想在场景里面移动，先仔细想一想下面这个句子：

- 将摄像机向后移动，和将整个场景向前移动是一样的

这正是观察矩阵所做的，我们以相反于摄像机移动的方向移动整个场景#note[移动整个场景]。由于我们的摄像机朝着 z 轴的正方向移动了，所以我们会通过将场景沿着 z 轴负方向平移来实现视野变换，从而让摄像机处于原点位置观察世界。

在下一个教程中我们将会详细讨论如何让摄像机在场景中实现更复杂的移动，就目前来说，观察矩阵是这样的：

```python
view = glm.mat4(1)
# 注意，这里朝着我们期望移动的相反方向移动场景
view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))
```#note[简单标注说明一下 vec3 的 z 分量]

最后我们需要做的是定义一个投影矩阵。我们希望在场景中使用透视投影，所以像这样声明一个投影矩阵：

```python
projection = glm.mat4(1)
projection = glm.perspective(glm.radians(45.0), screenWidth, screenHeight, 0.1, 100.0)
```

这个投影矩阵的视野区域，就对应我们前面所说的锥形平截头体，0.1 表示这个近平面，100 表示这个远平面，而这个 45 度角，即为锥形在竖直方向的张角，也称为“视野”。如果这个角度越大，这个视野范围就会越夸张，在这里我们设置为 45 度即可。

既然我们已经创建了这些变换矩阵，我们应该将它们传入着色器。首先，让我们在顶点着色器中声明这些 uniform 变换矩阵，然后将它们乘以顶点坐标：

```glsl
#version 330 core

in vec3 in_point;
...
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // 注意乘法要从右向左读
    gl_Position = projection * view * model * vec4(in_point, 1.0);
}
```

我们还应将矩阵传入着色器：

```python
prog['model'].write(model.to_bytes())
prog['view'].write(view.to_bytes())
prog['projection'].write(projection.to_bytes())
```
#note[备注【这通常在每次的渲染迭代中进行，因为变换矩阵会经常变动】]

我们的顶点坐标已经使用模型、观察和投影矩阵进行变换了#note[在流程图块中高亮]，最终的物体应该会：#note[用动画高亮以下各个特点]

- 稍微向后倾斜至地板方向

- 离我们有一点距离

- 有透视效果，也就是顶点越远，变得越小

它看起来就像是一个 3D#note[读作三维] 的平面，静止在一个虚构的地板上，如果你遇到什么问题，可以参考一下完整的源代码。
