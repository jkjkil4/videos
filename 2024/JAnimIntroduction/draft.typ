#set text(font: "Noto Sans S Chinese", fill: white)
#set par(justify: true)
#set page(height: auto, fill: black)
#show heading: h => box(h, fill: blue.lighten(10%), inset: 5pt, radius: 2pt)

#let content(body) = box(
  stroke: blue.lighten(50%),
  inset: 8pt,
  width: 100%,
  body
)

= JAnim - 编写开源动画引擎的一次尝试

== 什么是 JAnim？

不少人可能听说过 manim，一个数学动画库，我之前的这几期视频就是用 manim 做的。但是，manim(gl) 毕竟偏向于是 Grant Sanderson 的个人项目，所以在使用的时候经常会遇到不太顺手的地方。于是，在对 manim 的源码进行了细致的挖掘后，我决定编写一个自己的动画库，便有了 JAnim。

== 与其它工具的对比

在进行详细的介绍之前，我会将 JAnim 与其它“类 manim”工具进行横向对比

#align(
  center,
  box(fill: red.lighten(20%), inset: 8pt)[
    有主观倾向，请自行甄别
  ]
)

#align(
  center,
  box(fill: blue.lighten(20%), inset: 8pt)[
    该段模仿了 manim3 的介绍视频
  ]
)

#set enum(numbering: "#1")

+ 文档

  + manimce
  + janim
  + manimgl

+ 社区

  + manimce
  + manimgl
  + janim

+ 功能多样性

  + manimce
  + manimgl
  + janim

+ Python 版本支持

  + manimgl: 3.7+
  + manimce: 3.8+
  + janim: 3.12+

+ 平台支持

  + manimgl: Windows Linux MacOS
  + manimce: Windows Linux MacOS
  + janim: 只有我的电脑

+ 维护

  + manimce: 社区维护
  + janim: 我来维护
  + manimgl: 自 2022.4.12 的 1.6.1 版后便没有新的发布包（github 上有 Grant 的最新更新，但是已经产生了相当大的差异）

#line(length: 100%, stroke: white)

接下来，我们主要谈 JAnim 功能的优缺点，因此不涉及入门教程的部分（你可以在文档中看到目前较为简略的入门教程和样例）。

== JAnim 有什么功能

JAnim 在很大程度上受到 manim 的启发，因此，大部分的基础功能，例如几何形状插值、文字书写等效果都是足够完善的。

并且 JAnim 也解决了 manim 中的一些痛点:

#content[
  在 JAnim 中，你可以使用 depth 指定绘制的优先级，保证层级关系。
]

#content[
  在 JAnim 中，你可以使用 prepare 预先设置之后会进行的动画，而不在时间上前进，这样给了你在这段时间上创建其它动画的机会。
]

#content[
  在 manim 中，许多动画方法会直接改动原物件的属性，例如 manim 中 `Transform(a, b)` 的运作原理是在动画过程中，将插值的结果直接设置到 a 对象上，由 a 来呈现插值的效果。

  JAnim 中的动画方法不会改动原物件的属性，它完全只是在这个区段中显示插值的效果，不会对 a 的属性产生影响。
]

#content[
  JAnim 的预览窗口下方提供了时间轴控件，你不仅可以前后调整进度，而且可以看到标注的动画起止时间。

  并且，在 JAnim 中，可以一键载入新的内容，而不必关掉窗口再次开启。

  你应该也看到了，可以直接插入音频和字幕，这样你就可以把配音的工作流整合到动画制作中。
]

== 目前的局限性

- JAnim 目前拥有的组件相对较少，一些功能不太完善。可能要等我有特定的需求后，你才能在 JAnim 看到对应的更新。

- #{[
  有一些语法会更啰嗦，比如：

  #table(
    columns: 2,
    inset: 6pt,
    stroke: white,
    fill: (x, y) => {
      if y == 0 {
        blue.lighten(20%)
      } else {
        none
      }
    },
    [manim], [janim],

    `.apply_points_function(...)`, `.points.apply_points_fn(...)`,
    `.next_to(...)`, `.points.next_to(...)`,
    `.set_color(...)`, `.color.set(...)`,
    `.set_stroke(...)`, `.stroke.set(...)`,
    `.set_fill(...)`, `.fill.set(...)`,
  )
  也就是要显式的写出“是在对哪个部分操作，是坐标数据，还是颜色数据？”，不过从另一个角度来看，这种显式语法也许是一种优点？
]}

- 不支持按步模拟，也就是没有提供“根据前一帧的内容决定后一帧”的功能，之后可能会支持。

- JAnim 目前只支持单声道音频（多声道的会先转换）。

- 我并没有对比过，但是我觉得 JAnim 的渲染效率更低。并且我觉得我写渲染器写得很草率，如果你去看这部分的源码应该就能感受到这一点。

- JAnim 没有足够的项目积累，有些潜在的问题需要进行更多的动画开发才能逐步发现。

== 一些实例

虽然说目前没有足够的项目积累，但是也有一些可供参考的实例

（展示样例）

我也整了点活

（展示 osbplayer）

#line(length: 100%, stroke: white)

以上就是对 JAnim 特性的介绍，如果你有兴趣，欢迎来提 issue 和 PR。

== 特别鸣谢

- Grant Sanderson: 他开发的 manim 是 JAnim 借鉴的原型

- ManimKindergarten 群友

- 凡人忆拾: 在他的 manim3 发布之前，JAnim 更偏向于是对 manim 的复刻，虽然提供了对增量动画的支持，但是仍无法自由地控制时间进度。在 manim3 发布后，我下定决心进行了大重构，形成了现在的架构。
