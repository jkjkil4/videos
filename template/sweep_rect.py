from __future__ import annotations

from janim.imports import *


class SweepRect(SurroundingRect):
    def __init__(self, *items: Points, direction=..., color=YELLOW, alpha=0.25, **kwargs):
        super().__init__(
            Group(*items),
            fill_alpha=alpha,
            stroke_alpha=0,
            color=color,
            depth=1,
            **kwargs
        )

        if direction is ...:
            w, h = self.points.box.size
            direction = RIGHT if w > h else DOWN

        self.direction = np.array(direction)
        self.dim = np.where(self.direction != 0)[0][0]

    def anim_in(self, rate_func=rush_from, **kwargs):
        return DataUpdater(
            self,
            lambda data, p: data.points.stretch(p.alpha, dim=self.dim, about_edge=-self.direction),
            rate_func=rate_func,
            become_at_end=False,
            **kwargs,
            name='SweepRect in'
        )

    def anim_out(self, rate_func=rush_into, **kwargs):
        return DataUpdater(
            self,
            lambda data, p: data.points.stretch(1 - p.alpha, dim=self.dim, about_edge=self.direction),
            rate_func=rate_func,
            hide_at_end=True,
            become_at_end=False,
            **kwargs,
            name='SweepRect out'
        )

    def ins(*rects: SweepRect, **kwargs):
        return AnimGroup(
            *[rect.anim_in() for rect in rects],
            **kwargs
        )

    def outs(*rects: SweepRect, **kwargs):
        return AnimGroup(
            *[rect.anim_out() for rect in rects],
            **kwargs
        )
