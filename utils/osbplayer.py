import os

from janim.imports import *
from osbparser import *
from osbparser.interpolator import ObjectInterpolator


class OsbPlayer(Timeline):
    CONFIG = Config(
        output_dir=':/videos'
    )

    osb_path: str | None = None
    audio_path: str | None = None

    osu_depth = 0
    info_depth = -1
    show_info = False
    global_offset = 0

    def construct(self) -> None:
        assert self.osb_path is not None

        osb = OsuStoryboard.from_file(find_file(self.osb_path))

        factor1 = Config.get.pixel_width / 640
        factor2 = Config.get.pixel_height / 480
        factor = min(factor1, factor2)
        osu_width = 640 * factor
        osu_height = 480 * factor
        offsetx = (Config.get.pixel_width - osu_width) / 2
        offsety = (Config.get.pixel_height - osu_height) / 2

        scale_factor = Config.get.pixel_to_frame_ratio / Config.get.default_pixel_to_frame_ratio

        def map_x_from_osu(x: float) -> float:
            with self.with_config():
                return -Config.get.frame_x_radius \
                    + (x * factor + offsetx) * Config.get.pixel_to_frame_ratio

        def map_y_from_osu(y: float) -> float:
            with self.with_config():
                return -Config.get.frame_y_radius \
                    + (Config.get.pixel_height - (y * factor + offsety)) * Config.get.pixel_to_frame_ratio

        def parse_obj(obj: Object) -> list[DataUpdater]:
            imgs = None
            if isinstance(obj, Sprite):
                img = ImageItem(obj.file, depth=self.osu_depth)
                img.points.scale(scale_factor)
            elif isinstance(obj, Animation):
                root, ext = os.path.splitext(obj.file)
                imgs = [
                    ImageItem(f'{root}{i}{ext}', depth=self.osu_depth)
                        .points.scale(scale_factor)
                        .r
                    for i in range(obj.frame_count)
                ]
                img = imgs[0]
            else:
                assert False

            offset = ORIGIN.copy()

            if obj.origin in (Origin.TopLeft, Origin.CentreLeft, Origin.BottomLeft):
                offset += img.points.box.width / 2 * RIGHT
            elif obj.origin in (Origin.TopRight, Origin.CentreRight, Origin.BottomRight):
                offset += img.points.box.width / 2 * LEFT

            if obj.origin in (Origin.TopLeft, Origin.TopCentre, Origin.TopRight):
                offset += img.points.box.height / 2 * DOWN
            elif obj.origin in (Origin.BottomLeft, Origin.BottomCentre, Origin.BottomRight):
                offset += img.points.box.height / 2 * UP

            # offset *= factor
            img.points.shift(offset)

            flatten = obj.flatten()
            obj_start = flatten.get_start()
            classified = flatten.classify()
            ips = ObjectInterpolator(classified)

            for cmd in classified[CmdParameter]:
                if cmd.parameter == Parameter.A:
                    log.warning(f'Unsupported {cmd.parameter}, at line {cmd.lineno}')

            def updater(data: ImageItem, p: UpdaterParams) -> None:
                t = p.global_t * 1000

                if imgs is not None:
                    subimg_idx = int(t - obj_start // obj.frame_delay)
                    if obj.looptype is LoopType.LoopForever:
                        subimg_idx %= obj.frame_count
                    else:
                        subimg_idx = min(subimg_idx, len(imgs) - 1)
                    data.image.become(imgs[subimg_idx].image)

                scale = factor * ips.scale(t)
                vsx, vsy = ips.vector_scale(t)

                if ips.h_flag(t):
                    vsx *= -1
                if ips.v_flag(t):
                    vsy *= -1

                data.points.scale([scale * vsx, scale * vsy, 0], about_point=ORIGIN)
                data.points.rotate(-ips.rotate(t), about_point=ORIGIN)

                x, y = obj.x, obj.y
                xx, yy = ips.move(t)
                if xx is not None:
                    x = xx
                if yy is not None:
                    y = yy
                xx, yy = ips.movex(t), ips.movey(t)
                if xx is not None:
                    x = xx
                if yy is not None:
                    y = yy

                data.points.shift([
                    map_x_from_osu(x),
                    map_y_from_osu(y),
                    0
                ])
                data.color.set(np.array(ips.colour(t)) / 255, ips.fade(t))

            result: list[DataUpdater] = []
            for start, end in classified.visible_ranges():
                if start == end:
                    continue
                start /= 1000
                end /= 1000
                result.append(
                    DataUpdater(
                        img,
                        updater,
                        hide_at_begin=False,
                        show_at_end=False,
                        become_at_end=False,
                        rate_func=linear,
                        at=self.global_offset + start,
                        duration=end - start
                    )
                )
            return result

        if self.audio_path is not None:
            self.play_audio(Audio(self.audio_path), delay=self.global_offset)

        updater_anims: list[DataUpdater] = []
        for obj in osb.events.objects:
            updater_anims.extend(parse_obj(obj))

        if self.show_info:
            txt = Text(
                f'osu! storyboard: {os.path.basename(self.osb_path)}\n',
                font_size=16
            )
            txt.points.to_border(UL)

            rect = SurroundingRect(
                txt,
                stroke_alpha=0,
                fill_alpha=0.5,
                color=BLACK
            )

            Group(rect, txt).show().depth.arrange(self.info_depth)

        self.play(*updater_anims)
        self.forward()
