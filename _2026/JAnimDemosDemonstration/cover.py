# ruff: noqa
# fmt: off
import sys

sys.path.append('.')

from janim.imports import *

from _2026.JAnimDemosDemonstration.code import Demo7, Demo3, Demo4, Demo6

with reloads():
    from template import *
from template import *


class Center(Timeline):
    def construct(self) -> None:
        bg = FrameRect(fill_alpha=1, fill_color=BLACK, stroke_alpha=0).show()
        tl = Demo7().build().to_playback_control_item().seek(2.57).show()

        demo7_effect = SimpleFrameEffect(
            tl,
            shader="""
            vec2 texcoord = v_texcoord;

            // 缩放
            texcoord -= 0.5;
            texcoord *= JA_FRAME_RADIUS;
            texcoord *= 0.8;
            texcoord /= JA_FRAME_RADIUS;
            texcoord += 0.5;

            // 获取颜色
            f_color = frame_texture(texcoord);
            """,
            uniforms=[
                'vec2 JA_FRAME_RADIUS'
            ]
        ).show()

        # demo2_effect = SimpleFrameEffect(
        #     tl,
        #     shader="""
        #     // 向中间挤压
        #     vec2 texcoord = v_texcoord;
        #     if (texcoord.x < 0.5) {
        #         texcoord.x -= 0.1;
        #     } else {
        #         texcoord.x += 0.1;
        #     }

        #     // 缩放
        #     texcoord -= 0.5;
        #     texcoord *= JA_FRAME_RADIUS;
        #     texcoord *= 1.1;
        #     texcoord /= JA_FRAME_RADIUS;
        #     texcoord += 0.5;

        #     // 获取颜色
        #     f_color = frame_texture(texcoord);
        #     """,
        #     uniforms=[
        #         'vec2 JA_FRAME_RADIUS'
        #     ]
        # ).show()

        self.forward(tl.duration)


class Cover(Timeline):
    def construct(self) -> None:
        tl_left = Demo4().build().to_playback_control_item().seek(0.5).show()
        clip_left = TransformableFrameClip(tl_left, clip=(0.5, 0, 0, 0), offset=(-0.5, 0)).show()

        tl_right = Demo3().build().to_playback_control_item().seek(2.5).show()
        clip_right = TransformableFrameClip(tl_right, clip=(0, 0, 0.5, 0), offset=(0.5, 0)).show()

        tl = Demo6().build().to_playback_control_item().seek(3.8).show()

        tl_center = Center().build().to_item().show()
        clip_center = RectClip(tl_center, anchor=ORIGIN, border=True).show()
        clip_center.points.set_size(8, 8).rotate(-20 * DEGREES)

        self.forward(10)
