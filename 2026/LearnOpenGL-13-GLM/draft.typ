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

#set page(numbering: "1")

现在我们已经解释了变换背后的所有理论，是时候将这些知识利用起来了。在 Python 中我们使用 `glm` 库就能很轻松地创建各种变换矩阵，包括我们刚刚讲的“缩放矩阵”“位移矩阵”“旋转矩阵”，还包括很多其它的，我们之后会介绍到。
