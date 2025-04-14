import os
import sys

sys.path.append(os.path.dirname(__file__))

import json
# from pprint import pprint

from janim.imports import *
# from objprint import objprint
from simai_py import *

type Time = float
type BPM = float

CENTRAL_SPACING_FACTOR = 0.25

NOTE_RADIUS = 0.25
EFFECT_LAYER = -5
SLIDE_LAYER = -7
NOTE_LAYER = -10

ANCHORS_A = np.array([
    [1.26, 3.07], [3.07, 1.27], [3.05, -1.26], [1.29, -3.07], 
    [-1.29, -3.07], [-3.08, -1.26], [-3.08, 1.29], [-1.27, 3.1],  
]) * 0.9
ANCHORS_B = np.array([
    [0.62, 1.51], [1.51, 0.62], [1.5, -0.62], [0.61, -1.48],
    [-0.61, -1.51], [-1.53, -0.61], [-1.5, 0.64], [-0.64, 1.54],
])
ANCHORS_C = np.array([[0, 0]])
ANCHORS_D = ANCHORS_A @ np.array(rotation_about_z(TAU / 16))[:2, :2].T
ANCHORS_E = np.array([
    [0, 2.31], [1.63, 1.63], [2.31, 0], [1.63, -1.63],
    [0, -2.31], [-1.63, -1.63], [-2.31, 0], [-1.63, 1.63],
]) * 0.95

ANCHORS = {
    NoteGroup.ASensor: ANCHORS_A,
    NoteGroup.BSensor: ANCHORS_B,
    NoteGroup.CSensor: ANCHORS_C,
    NoteGroup.DSensor: ANCHORS_D,
    NoteGroup.ESensor: ANCHORS_E,
}


chart_cache: dict[str, MaiChart] = {}


def get_chart(path: str) -> MaiChart:
    if path in chart_cache:
        return chart_cache[path]
    data = json.load(open(path, 'rt'))
    chart = MaiChart.deserialize(data)
    chart_cache[path] = chart
    return chart


class SimaiPlayer(Timeline):
    speed = 8
    global_offset = 0

    CONFIG = Config(
        font='Noto Sans S Chinese',
    )

    def construct(self):
        if os.path.exists('11663/pv.mp4'):
            video = Video('11663/pv.mp4', alpha=0.5, height=6).show()
            self.schedule(self.global_offset, video.start)
        else:
            log.warning('11663/pv.mp4 未找到，铺面无视频')

        # ImageItem('overlay.jpg', height=8.1, alpha=0.5).show()

        if os.path.exists('11663/track.mp3'):
            audio_t = self.play_audio(Audio('11663/track.mp3'), delay=self.global_offset)
        else:
            audio_t = None
            log.warning('11663/track.mp3 未找到，铺面无音频')

        border = Circle(radius=3.5).show()
        border.points.flip().rotate(-2.5 * TAU / 8)
        central = border.points.box.center

        border_dots = DotCloud(*border.points.get_anchors(), radius=0.1).show()

        chart = get_chart(find_file('11663_inote5.json'))

        anims = []

        for collection in reversed(chart.note_collections):
            # TODO: parsing EachStyle
            each = len(collection.notes) > 1
            slide_each = len([
                note
                for note in collection.notes
                if note.is_star
            ]) > 1

            for note in reversed(collection.notes):
                if note.styles == NoteStyles.Mine:
                    print('note.styles == Mine')
                    print(note)
                match note.type, note.is_star:
                    case NoteType.Tap | NoteType.Break, False:
                        target = border.points.get_anchors()[note.location.index]
                        anims += [
                            TapNoteItem(note, central, target, each)
                                .create_updater(collection.time, self.speed),
                            TapComboEffect(note, target)
                                .create_updater(collection.time)
                        ]
                    case NoteType.Hold, _:
                        assert not note.is_star
                        target = border.points.get_anchors()[note.location.index]
                        end_time = collection.time + note.length
                        anims += [
                            HoldNoteItem(note, central, target, each)
                                .create_updater(collection.time, end_time, self.speed),
                            TapComboEffect(note, target)
                                .create_updater(end_time)
                        ]
                    case NoteType.Touch, _:
                        assert not note.is_star
                        anims += [
                            TouchNoteItem(note, each)
                                .create_updater(collection.time),
                            TouchComboEffect(note)
                                .create_updater(collection.time)
                        ]
                        if note.styles & NoteStyles.Fireworks:
                            anims.append(
                                FireworkEffect(note)
                                    .create_updater(collection.time)
                            )
                    case NoteType.Tap | NoteType.Break, True:
                        target = border.points.get_anchors()[note.location.index]
                        anims += [
                            *[
                                SlideItem(
                                    path, 
                                    SlideItem.slide_path_to_vpath(border.points.get_anchors(), path, note.location), 
                                    slide_each or len(note.slide_paths) > 1
                                ).create_updater(collection.time, path.delay, path.duration)

                                for path in note.slide_paths
                            ],
                            TapStarNoteItem(note, central, target, each)
                                .create_updater(collection.time, self.speed),
                            TapComboEffect(note, target)
                                .create_updater(collection.time),
                        ]

        tip = Text('前排提示：星星的形状只实现了直线和圆弧，\n其它的形状均被渲染为直线', font_size=16, depth=-20).show()
        tip.points.to_border(UL)
        
        self.play(*anims, at=self.global_offset)
        if audio_t is not None:
            self.forward_to(audio_t.end)


class TapNoteItem(Circle):
    note_styles = {
        (NoteStyles.None_, False): dict(
            stroke_color=['#f3387a', '#f1b1dd'] * 4 + ['#f3387a'],
            glow_color=BLACK
        ),
        (NoteStyles.Ex, False): dict(
            stroke_color=['#f3387a', '#f1b1dd'] * 4 + ['#f3387a'],
            glow_color='#f6a1d1'
        ),
        (NoteType.Break, False): dict(
            stroke_color=['#f67d03', '#ffbb19'] * 4 + ['#f67d03'],
            glow_color=BLACK
        ),
        (NoteStyles.None_, True): dict(
            stroke_color=['#f3b500', '#ffeb0b'] * 4 + ['#f3b500'],
            glow_color=BLACK
        ),
        (NoteStyles.Ex, True): dict(
            stroke_color=['#f3b500', '#ffeb0b'] * 4 + ['#f3b500'],
            glow_color='#ffe80a'
        ),
        (NoteType.Break, True): dict(
            stroke_color=['#f67d03', '#ffbb19'] * 4 + ['#f67d03'],
            glow_color=BLACK
        ),
    }

    def __init__(self, note: Note, central: np.ndarray, target: np.ndarray, each: bool):
        super().__init__(
            NOTE_RADIUS, 
            stroke_radius=0.06, 
            glow_alpha=2,
            depth=NOTE_LAYER,
            **self.note_styles[(NoteType.Break if note.type == NoteType.Break else note.styles, each)]
        )
        self.central = central
        self.target = target

    def create_updater(self, time: float, speed: float) -> DataUpdater[Self]:
        duration = get_norm(self.target - self.central) / speed
        return DataUpdater(
            self,
            lambda data, p: 
                data.points.move_to(
                    interpolate(
                        self.central, self.target, 
                        p.alpha if p.alpha > CENTRAL_SPACING_FACTOR else CENTRAL_SPACING_FACTOR
                    )
                ).scale(
                    p.alpha / CENTRAL_SPACING_FACTOR if p.alpha < CENTRAL_SPACING_FACTOR else 1
                ),
            hide_at_end=True,
            become_at_end=False,
            rate_func=linear,
            at=time - duration,
            duration=duration
        )
    

class TapComboEffect(RegularPolygon):
    def __init__(self, note: Note, target: np.ndarray):
        rot = -TAU / 16 + TAU / 12 + (note.location.index) * (-TAU / 8 + PI / 2)
        super().__init__(
            radius=0.65,
            start_angle=rot,
            color='#e4b05e',
            depth=EFFECT_LAYER
        )
        self.points.move_to(target)

    def create_updater(self, time: float) -> DataUpdater:
        return DataUpdater(
            self,
            lambda data, p:
                data.points.scale(math.cos(p.alpha * TAU))
                    .r.stroke.fade(p.alpha),
            rate_func=linear,
            hide_at_end=True,
            become_at_end=False,
            at=time,
            duration=0.25
        )
    

class HoldNoteItem(VItem):
    def __init__(self, note: Note, central: np.ndarray, target: np.ndarray, each: bool):
        super().__init__(
            depth=NOTE_LAYER,

            stroke_radius=0.06,
            stroke_color=TapNoteItem.note_styles[(NoteStyles.None_, each)]['stroke_color'],

            glow_alpha=2,
            glow_color=('#fad306'if each else '#f289bc') if note.is_ex else BLACK
        )
        self.central = central
        self.target = target

    @staticmethod
    def unit_vector(angle: float) -> np.ndarray:
        return np.array([
            math.cos(angle),
            math.sin(angle),
            0
        ])

    def create_updater(self, t1: float, t2: float, speed: float) -> DataUpdater:
        vect = self.target - self.central
        
        duration = get_norm(vect) / speed
        grow_duration = duration * CENTRAL_SPACING_FACTOR

        angle = angle_of_vector(vect)
        radius = NOTE_RADIUS * 2 / math.sqrt(3)

        def updater(data: HoldNoteItem, p: UpdaterParams) -> None:
            elapsed = p.global_t - p.range.at
            alpha1 = clip(elapsed / duration, CENTRAL_SPACING_FACTOR, 1)
            alpha2 = clip((elapsed - (t2 - t1)) / duration, CENTRAL_SPACING_FACTOR, 1)
            point1 = interpolate(self.central, self.target, alpha1)
            point2 = interpolate(self.central, self.target, alpha2)
            data.points.set_as_corners([
                *[
                    point1 + radius * self.unit_vector(angle + i * PI / 3)
                    for i in range(-1, 2)
                ],
                *[
                    point2 + radius * self.unit_vector(angle + PI + i * PI / 3)
                    for i in range(-1, 2)
                ]
            ]).close_path()

            if elapsed < grow_duration:
                data.points.scale(elapsed / grow_duration)
            

        return DataUpdater(
            self,
            updater,
            rate_func=linear,
            hide_at_end=True,
            become_at_end=False,
            at=t1 - duration,
            duration=duration + t2 - t1,
            skip_null_items=False
        )
    

class TouchNoteItem(Group):
    def __init__(self, note: Note, each: bool):
        super().__init__(
            VItem().points.set_as_corners([ORIGIN, UR, UL, ORIGIN]).r,
            VItem().points.set_as_corners([ORIGIN, DR, DL, ORIGIN]).r,
            VItem().points.set_as_corners([ORIGIN, UR, DR, ORIGIN]).r,
            VItem().points.set_as_corners([ORIGIN, UL, DL, ORIGIN]).r,
            depth=NOTE_LAYER,
            stroke_radius=0.06,
            stroke_color=(
                ['#f3c70d', '#f6ef16', '#f6ef16', '#f6ef16', '#f3c70d']
                if each
                else ['#006fe3', '#05c6fc', '#05c6fc', '#05c6fc', '#006fe3']
            ),
            glow_alpha=2,
            glow_color=BLACK
        )
        self.anchor = np.array([*ANCHORS[note.location.group][note.location.index], 0])
        self.points.scale(0.3).move_to(self.anchor)

    def create_updater(self, time: float) -> DataUpdater:
        duration = 0.6
        return DataUpdater(
            self,
            lambda data, p: data.points.shift(
                ((1-p.alpha) * 0.2 + 0.1) 
                * normalize(data.points.box.center - self.anchor)
            ),
            rate_func=ease_in_quart,
            hide_at_end=True,
            become_at_end=False,
            root_only=False,
            at=time - duration,
            duration=duration,
        )
    

class TouchComboEffect(Circle):
    def __init__(self, note: Note):
        super().__init__(
            radius=0.3,
            fill_color='#faff74',
            fill_alpha=0.5,
            stroke_alpha=0,
            depth=EFFECT_LAYER
        )
        self.points.move_to([*ANCHORS[note.location.group][note.location.index], 0])
    
    def create_updater(self, time: float) -> DataUpdater:
        return DataUpdater(
            self,
            lambda data, p:
                data.points.scale(1 + p.alpha)
                    .r.fill.fade(p.alpha),
            hide_at_end=True,
            become_at_end=False,
            at=time,
            duration=0.15
        )
    

class FireworkEffect(Text):
    def __init__(self, note: Note):
        super().__init__(
            '贼TM炫酷的特效',
            font_size=64,
            fill_alpha=0.5,
            depth=EFFECT_LAYER
        )
        self.points.move_to([*ANCHORS[note.location.group][note.location.index], 0])
    
    def create_updater(self, time: float) -> Rotating:
        return Rotating(
            self, 
            TAU, 
            at=time, 
            duration=0.5,
            hide_at_end=True,
            become_at_end=False
        )
    

class TapStarNoteItem(VItem, MarkedItem):
    def __init__(self, note: Note, central: np.ndarray, target: np.ndarray, each: bool):
        match note.type, note.is_ex, each:
            case (NoteType.Break, _, _) | (_, False, True):
                styles = TapNoteItem.note_styles[(note.type, each)]
            case _, _, _:
                styles = dict(
                    stroke_color=['#006fe3', '#05c6fc'] * 5 + ['#006fe3'],
                    glow_color=BLACK
                )
        if note.is_ex:
            styles['glow_color'] = styles['stroke_color'][1]
        super().__init__(
            stroke_radius=0.06, 
            glow_alpha=2,
            depth=NOTE_LAYER,
            **styles
        )
        self.points.set_as_corners(
            np.array([
                (1.00, 0.00, 0),
                (0.40, 0.29, 0),
                (0.31, 0.95, 0),
                (-0.15, 0.48, 0),
                (-0.81, 0.59, 0),
                (-0.50, 0.00, 0),
                (-0.81, -0.59, 0),
                (-0.15, -0.48, 0),
                (0.31, -0.95, 0),
                (0.40, -0.29, 0),
                (1.00, 0.00, 0),
            ]) * NOTE_RADIUS * 1.4
        )
        self.mark.set_points([ORIGIN])
        self.central = central
        self.target = target

    def create_updater(self, time: float, speed: float) -> DataUpdater[Self]:
        duration = get_norm(self.target - self.central) / speed
        return DataUpdater(
            self,
            lambda data, p: 
                data.mark.set(
                    interpolate(
                        self.central, self.target, 
                        p.alpha if p.alpha > CENTRAL_SPACING_FACTOR else CENTRAL_SPACING_FACTOR
                    )
                ).r.points.scale(
                    p.alpha / CENTRAL_SPACING_FACTOR if p.alpha < CENTRAL_SPACING_FACTOR else 1
                ).rotate(
                    TAU * p.alpha,
                    about_point=data.mark.get()
                ),
            hide_at_end=True,
            become_at_end=False,
            rate_func=linear,
            at=time - duration,
            duration=duration
        )
    

class SlideItem(VItem):
    def __init__(self, slide_path: SlidePath, path: np.ndarray, each: bool):
        if slide_path.type == NoteType.Break or each:
            stroke_color = TapNoteItem.note_styles[(NoteType.Tap if slide_path.type == NoteType.Slide else slide_path.type, each)]['stroke_color']
        else:
            stroke_color = '#05c6fc'
        super().__init__(
            stroke_radius=0.3,
            depth=SLIDE_LAYER,
            stroke_alpha=[0.75, 0.2],
            stroke_color=stroke_color,
        )
        self.points.set(path)
    
    def create_updater(self, time: float, delay: float, duration: float) -> DataUpdater[Self]:
        fadein_duration = 0.3
        def updater(data: VItem, p: UpdaterParams):
            elapsed = p.global_t - p.range.at
            if elapsed < fadein_duration:
                data.stroke.fade(1 - elapsed / fadein_duration)
            else:
                data.points.pointwise_become_partial(
                    data, 
                    max(0, (elapsed - fadein_duration - delay) / duration), 
                    1
                )

        return DataUpdater(
            self,
            updater,
            hide_at_end=True,
            become_at_end=False,
            rate_func=linear,
            at=time - fadein_duration,
            duration=delay + duration + fadein_duration,
        )
    
    @staticmethod
    def slide_path_to_vpath(anchors: np.ndarray, path: SlidePath, note_location: Location) -> np.ndarray:
        def location_to_point(location: Location) -> np.ndarray:
            if location.group == 0:
                return anchors[location.index]
            return np.array([*ANCHORS[location.group][location.index], 0])
        builder = PathBuilder(start_point=location_to_point(note_location))
        prev_loc = note_location
        # builder.line_to(location_to_point(path.start_location))
        for segment in path.segments:
            # for key, value in SlideType.__members__.items():
            #     if segment.slide_type == value:
            #         print(key)
            for vert in segment.vertices:
                loc = Location(vert.index, vert.group)
                point = location_to_point(loc)
                match segment.slide_type:
                    case SlideType.RingCw:
                        if loc.index == prev_loc.index:
                            builder.arc_to(-point, -PI)
                            builder.arc_to(point, -PI)
                        else:
                            steps = loc.index + 8 - prev_loc.index if loc.index < prev_loc.index else loc.index - prev_loc.index
                            builder.arc_to(point, -steps / 8 * TAU)
                    case SlideType.RingCcw:
                        if loc.index == prev_loc.index:
                            builder.arc_to(-point, PI)
                            builder.arc_to(point, PI)
                        else:
                            steps = prev_loc.index + 8 - loc.index if prev_loc.index < loc.index else prev_loc.index - loc.index
                            builder.arc_to(point, steps / 8 * TAU)
                    case _:
                        builder.line_to(point)
                prev_loc = loc

        return builder.get()
