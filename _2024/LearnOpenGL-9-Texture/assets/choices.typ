#set page(width: auto, height: auto, fill: black)
#set text(fill: white)

#let center-box(body) = context {
  box(move(body, dy: measure(body).height / 2 - 0.5em))
}

#{
  show raw: set text(fill: rgb("#4ec9b0"))
  `mgl`
}.#center-box(
  box(
    fill: rgb("#9A72AC").transparentize(30%),
    inset: 2pt,
    width: 6.8em
  )[
    #set par(spacing: -0.3em)
    #set text(fill: rgb("#9cdcfe"))
    `NEAREST` \
    #set align(center)
    #move(dx: 3pt, dy: 2pt, text(fill: white)[\/]) \
    #set align(right)
    `LINEAR`
  ]
)`_`#center-box(
  box(
    fill: rgb("#C55F73").transparentize(30%),
    inset: 2pt,
    width: 13.6em
  )[
    #set par(spacing: -0.3em)
    #set text(fill: rgb("#9cdcfe"))
    `MIPMAP_NEAREST` \
    #set align(center)
    #move(dx: 2.5pt, dy: 2pt, text(fill: white)[\/]) \
    #set align(right)
    `MIPMAP_LINEAR`
  ]
)
