from pymusicxml import *

l = [
    PartGroup([
        Part("Oboe", [
            Measure([
                Note("G#4", 0.75),
                Rest(0.25)
            ], time_signature=(1, 4), directions_with_displacements=[
                (MetronomeMark(1.5, 80), 0),
                (TextAnnotation("rit.", italic=True), 1.0),
                (MetronomeMark(1.0, 60), 3.5)
            ]),
            Measure([
                Tuplet([
                    Note("c5", 0.5),
                    Note("bb4", 0.25),
                    Note("a4", 0.25),
                    Note("b4", 0.25),
                ], (5, 4)),
                Note("f4", 2, directions=TextAnnotation("with gusto!")),
                Rest(1)
            ], clef="mezzo-soprano", barline="end")
        ]),
        Part("Clarinet", [
            Measure([
                Tuplet([
                    Note("c5", 0.5),
                    Note("bb4", 0.25, notehead="x"),
                    Note("a4", 0.25),
                    Note("b4", 0.25),
                ], (5, 4)),
                Note("f4", 2),
                Rest(1)
            ], time_signature=(4, 4)),
            Measure([
                Note("d5", 1.5),
                BeamedGroup([
                    Note("f#4", 0.25),
                    Note("A#4", 0.25)
                ]),
                Chord(["Cs4", "Ab4"], 1.0),
                Rest(1.0)
            ], barline="end")
        ])
    ]),
    Part("Bassoon", [
        Measure([
            BarRest(4)
        ], time_signature=(4, 4), clef="bass"),
        Measure([
            [
                BeamedGroup([
                    Rest(0.5),
                    Note("d4", 0.5, notehead="open mi", notations=[StartGliss(1), StartSlur()]),
                    Note("Eb4", 0.5, notations=[StopGliss(1), StartGliss(2)]),
                    Note("F4", 0.5, notations=[StopGliss(2), StopSlur()]),
                ]),
                Note("Eb4", 2.0)
            ],
            None,
            [
                Rest(1.0),
                Note("c4", 2.0),
                Note("Eb3", 0.5),
                Rest(0.5)
            ]
        ], barline="end")
    ])]

directions_with_displacements = [
    (MetronomeMark(1.5, 80), 0),
    (MetronomeMark(1.0, 60), 3.5)
]

p = Part("Oboe", [
    Measure([
        Note("g4", 0.75),
        Rest(0.25)
    ], time_signature=(1, 4)),
    Measure([
        Tuplet([
            Note("c5", 0.5),
            Note("bb4", 0.25),
            Note("a4", 0.25),
            Note("b4", 0.25),
        ], (5, 4)),
        Note("f4", 2),
        Rest(1)
    ], clef="mezzo-soprano", barline="end")])

s: Score = Score(title="Directly Created MusicXML", composer="HTMLvis")
s.append(p)
s.export_to_file("DirectExample.musicxml")
