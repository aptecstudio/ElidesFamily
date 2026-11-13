import 'dart:ui';

import 'character_rig.dart';

/// One arm in a frame.
class ArmFrame {
  const ArmFrame({
    required this.points,
    required this.kind,
    required this.handRot,
    required this.front,
    this.fold,
  });

  factory ArmFrame.fromPose(ArmPose pose) => ArmFrame(
    points: pose.points,
    kind: pose.kind,
    handRot: pose.handRot,
    front: pose.front,
    fold: pose.fold,
  );

  final List<Offset> points;
  final String kind;

  /// Degrees; null means "follow the arm".
  final double? handRot;
  final bool front;

  /// See [ArmPose.fold].
  final double? fold;

  ArmFrame copyWith({List<Offset>? points}) => ArmFrame(
    points: points ?? this.points,
    kind: kind,
    handRot: handRot,
    front: front,
    fold: fold,
  );

  /// Smooth blend: the curve moves point by point; the hand shape and the
  /// layer switch halfway, when the arm is in motion.
  static ArmFrame lerp(ArmFrame a, ArmFrame b, double t) {
    final rot = (a.handRot == null && b.handRot == null)
        ? null
        : lerpDouble(a.handRot ?? b.handRot!, b.handRot ?? a.handRot!, t);
    return ArmFrame(
      points: [
        for (var i = 0; i < 4; i++) Offset.lerp(a.points[i], b.points[i], t)!,
      ],
      kind: t < 0.5 ? a.kind : b.kind,
      handRot: rot,
      front: t < 0.5 ? a.front : b.front,
      fold: t < 0.5 ? a.fold : b.fold,
    );
  }
}

/// A sparkle with its current opacity.
class SparkleFrame {
  const SparkleFrame(this.data, this.opacity);

  final SparkleData data;
  final double opacity;
}

/// Everything the painter needs to draw one frame of a character.
///
/// Built by blending two poses ([CharacterFrame.lerp]) and then adding the
/// procedural layers of the controller (breathing, blinking, gaze, actions).
class CharacterFrame {
  const CharacterFrame({
    required this.lift,
    required this.lean,
    required this.shadow,
    required this.arms,
    required this.eyes,
    required this.look,
    required this.browsFrom,
    required this.browsTo,
    required this.browsT,
    required this.mouthFrom,
    required this.mouthTo,
    required this.mouthT,
    required this.tilt,
    required this.blush,
    required this.sparkles,
    required this.marks,
    this.breathe = 0,
    this.headBob = 0,
    this.tailAngle = 0,
    this.squash = 0,
    this.time = 0,
  });

  factory CharacterFrame.fromPose(PoseData pose) => CharacterFrame(
    lift: pose.lift,
    lean: pose.lean,
    shadow: pose.shadow,
    arms: {
      for (final e in pose.arms.entries) e.key: ArmFrame.fromPose(e.value),
    },
    eyes: pose.eyes,
    look: pose.look,
    browsFrom: pose.brows,
    browsTo: pose.brows,
    browsT: 1,
    mouthFrom: pose.mouth,
    mouthTo: pose.mouth,
    mouthT: 1,
    tilt: pose.tilt,
    blush: pose.blush ? 1 : 0,
    sparkles: [for (final s in pose.sparkles) SparkleFrame(s, 1)],
    marks: pose.marks ? 1 : 0,
  );

  /// Vertical offset of the whole body (negative is up).
  final double lift;

  /// Body rotation in degrees around the feet.
  final double lean;

  /// Horizontal radius of the ground shadow.
  final double shadow;
  final Map<String, ArmFrame> arms;

  /// Left and right eye kind.
  final List<String> eyes;

  /// Gaze offset of the irises.
  final Offset look;
  final String browsFrom;
  final String browsTo;
  final double browsT;
  final String mouthFrom;
  final String mouthTo;
  final double mouthT;

  /// Head rotation in degrees.
  final double tilt;

  /// Blush opacity, 0..1.
  final double blush;
  final List<SparkleFrame> sparkles;

  /// Opacity of the surprise marks, 0..1.
  final double marks;

  /// Breathing: relative stretch of the upper body.
  final double breathe;

  /// Vertical offset of the head.
  final double headBob;

  /// Tail swing in degrees.
  final double tailAngle;

  /// Squash (> 0) or stretch (< 0) of the whole body, e.g. when landing.
  final double squash;

  /// Seconds since the character appeared (twinkling sparkles).
  final double time;

  CharacterFrame copyWith({
    double? lift,
    double? lean,
    double? shadow,
    Map<String, ArmFrame>? arms,
    List<String>? eyes,
    Offset? look,
    double? tilt,
    double? blush,
    double? breathe,
    double? headBob,
    double? tailAngle,
    double? squash,
    double? time,
  }) => CharacterFrame(
    lift: lift ?? this.lift,
    lean: lean ?? this.lean,
    shadow: shadow ?? this.shadow,
    arms: arms ?? this.arms,
    eyes: eyes ?? this.eyes,
    look: look ?? this.look,
    browsFrom: browsFrom,
    browsTo: browsTo,
    browsT: browsT,
    mouthFrom: mouthFrom,
    mouthTo: mouthTo,
    mouthT: mouthT,
    tilt: tilt ?? this.tilt,
    blush: blush ?? this.blush,
    sparkles: sparkles,
    marks: marks,
    breathe: breathe ?? this.breathe,
    headBob: headBob ?? this.headBob,
    tailAngle: tailAngle ?? this.tailAngle,
    squash: squash ?? this.squash,
    time: time ?? this.time,
  );

  /// Blends two frames. Brows and mouth cross-fade from the visible one in
  /// [a] to the one in [b]; the eyes switch halfway.
  static CharacterFrame lerp(CharacterFrame a, CharacterFrame b, double t) {
    final sideKeys = {...a.arms.keys, ...b.arms.keys};
    return CharacterFrame(
      lift: lerpDouble(a.lift, b.lift, t)!,
      lean: lerpDouble(a.lean, b.lean, t)!,
      shadow: lerpDouble(a.shadow, b.shadow, t)!,
      arms: {
        for (final k in sideKeys)
          k: ArmFrame.lerp(a.arms[k] ?? b.arms[k]!, b.arms[k] ?? a.arms[k]!, t),
      },
      eyes: t < 0.5 ? a.eyes : b.eyes,
      look: Offset.lerp(a.look, b.look, t)!,
      browsFrom: a.browsT < 0.5 ? a.browsFrom : a.browsTo,
      browsTo: b.browsTo,
      browsT: t,
      mouthFrom: a.mouthT < 0.5 ? a.mouthFrom : a.mouthTo,
      mouthTo: b.mouthTo,
      mouthT: t,
      tilt: lerpDouble(a.tilt, b.tilt, t)!,
      blush: lerpDouble(a.blush, b.blush, t)!,
      sparkles: [
        for (final s in a.sparkles)
          if (s.opacity * (1 - t) > 0.01)
            SparkleFrame(s.data, s.opacity * (1 - t)),
        for (final s in b.sparkles)
          if (s.opacity * t > 0.01) SparkleFrame(s.data, s.opacity * t),
      ],
      marks: lerpDouble(a.marks, b.marks, t)!,
      time: b.time,
    );
  }
}
