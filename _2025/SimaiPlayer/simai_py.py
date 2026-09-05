from __future__ import annotations

from typing import Self
from enum import IntEnum, IntFlag
from dataclasses import dataclass


@dataclass
class MaiChart:
    finish_timing: float
    note_collections: list[NoteCollection]
    timing_change: list[TimingChange]
    
    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            data['FinishTiming'],
            [NoteCollection.deserialize(collection) for collection in data['NoteCollections']],
            [TimingChange.deserialize(change) for change in data['TimingChanges']],
        )


@dataclass
class NoteCollection:
    each_style: EachStyle | int
    time: float
    notes: list[Note]

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            data['eachStyle'],
            data['time'],
            [Note.deserialize(note) for note in data['notes']]
        )
    

class EachStyle(IntEnum):
    Default = 0
    ForceBroken = 1
    ForceEach = 2


@dataclass
class Note:
    location: Location
    styles: NoteStyles | int
    appearance: NoteAppearance | int
    type: NoteType | int
    
    length: float | None

    slide_morph: SlideMorph | int
    slide_paths: list[SlidePath]

    is_ex: bool
    is_star: bool

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            Location.deserialize(data['location']),
            data['styles'],
            data['appearance'],
            data['type'],
            data['length'],
            data['slideMorph'],
            [SlidePath.deserialize(path) for path in data['slidePaths']],
            data['IsEx'],
            data['IsStar'],
        )
    

@dataclass
class Location:
    index: int
    group: NoteGroup | int

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            data['index'],
            data['group'],
        )
    

class NoteGroup(IntEnum):
    Tap = 0
    ASensor = 1
    BSensor = 2
    CSensor = 3
    DSensor = 4
    ESensor = 5


class NoteStyles(IntFlag):
    None_ = 0
    Ex = 1 << 0
    Fireworks = 1 << 1
    Mine = 1 << 2


class NoteAppearance(IntEnum):
    Default = 0
    ForceNormal = 1
    ForceStar = 2
    ForceStarSpinning = 3


class NoteType(IntEnum):
    Tap = 0
    Touch = 1
    Hold = 2
    Slide = 3
    Break = 4
    ForceInvalidate = 5


class SlideMorph(IntEnum):
    FadeIn = 0
    SuddenIn = 1


@dataclass
class SlidePath:
    start_location: Location
    segments: list[SlideSegment]

    delay: float
    duration: float

    type: NoteType

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            Location.deserialize(data['startLocation']),
            [SlideSegment.deserialize(segment) for segment in data['segments']],
            data['delay'],
            data['duration'],
            data['type'],
        )


@dataclass
class SlideSegment:
    vertices: list[Location]
    slide_type: SlideType | int

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            [Location.deserialize(vertex) for vertex in data['vertices']],
            data['slideType'],
        )


class SlideType(IntEnum):
    StraightLine = 0
    RingCw = 1
    RingCcw = 2
    Fold = 3
    CurveCw = 4
    CurveCcw = 5
    ZigZagS = 6
    ZigZagZ = 7
    EdgeFold = 8
    EdgeCurveCw = 9
    EdgeCurveCcw = 10
    Fan = 11


@dataclass
class TimingChange:
    time: float
    tempo: float
    subdivisions: float

    seconds_per_bar: float
    seconds_per_beat: float

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        return cls(
            data['time'],
            data['tempo'],
            data['subdivisions'],
            data['SecondsPerBar'],
            data['SecondsPerBeat'],
        )
