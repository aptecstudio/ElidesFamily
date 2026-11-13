import 'dart:convert';
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

/// Animation rig of a character, exported from the draft scripts by
/// `tools/character-drafts/export_rig.py` (D-050).
///
/// It holds the PNG layers (head, dress, hands...), the vector data of the
/// parts drawn by code every frame (arms, legs, irises) and the poses. All
/// coordinates are in the 400×540 scene of the drafts.
class CharacterRig {
  CharacterRig._(Map<String, dynamic> json, this.images)
    : name = json['name'] as String,
      size = _size(json['size']),
      centerX = _d(json['centerX']),
      parts = {
        for (final e in (json['parts'] as Map<String, dynamic>).entries)
          e.key: _rect(e.value['rect']),
      },
      gradients = {
        for (final e in (json['gradients'] as Map<String, dynamic>).entries)
          e.key: RigGradient.fromJson(e.value as Map<String, dynamic>),
      },
      line = parseColor(json['line'] as String),
      limbStroke = _d(json['limbStroke']),
      limbFill = json['limbFill'] as String,
      arm = ArmStyle.fromJson(json['arm'] as Map<String, dynamic>),
      sleeve = SleeveStyle.fromJson(json['sleeve'] as Map<String, dynamic>),
      legs = [
        for (final l in json['legs'] as List)
          LegData.fromJson(l as Map<String, dynamic>),
      ],
      tailRoot = _offset(json['tailRoot']),
      headPivot = _offset(json['headPivot']),
      leanPivot = _offset(json['leanPivot']),
      shadow = ShadowStyle.fromJson(json['shadow'] as Map<String, dynamic>),
      eyes = EyeStyle.fromJson(json['eyes'] as Map<String, dynamic>),
      sparklePath = parseLinePath(json['sparkle']['d'] as String),
      marksPath = parseLinePath(json['marks']['d'] as String),
      marksColor = parseColor(json['marks']['color'] as String),
      marksWidth = _d(json['marks']['width']),
      poses = {
        for (final e in (json['poses'] as Map<String, dynamic>).entries)
          e.key: PoseData.fromJson(e.value as Map<String, dynamic>),
      };

  final String name;
  final Size size;

  /// Body axis: decides on which side the thumb of each hand goes.
  final double centerX;

  /// Rect of every PNG layer; for hands and feet it is relative to the point
  /// where they are attached.
  final Map<String, Rect> parts;
  final Map<String, ui.Image> images;
  final Map<String, RigGradient> gradients;
  final Color line;
  final double limbStroke;
  final String limbFill;
  final ArmStyle arm;
  final SleeveStyle sleeve;
  final List<LegData> legs;
  final Offset tailRoot;
  final Offset headPivot;
  final Offset leanPivot;
  final ShadowStyle shadow;
  final EyeStyle eyes;
  final Path sparklePath;
  final Path marksPath;
  final Color marksColor;
  final double marksWidth;
  final Map<String, PoseData> poses;

  static final Map<String, Future<CharacterRig>> _cache = {};

  /// Loads (once) the rig of [name], e.g. `elide`.
  static Future<CharacterRig> load(String name, {AssetBundle? bundle}) {
    return _cache.putIfAbsent(name, () => _load(name, bundle ?? rootBundle));
  }

  static Future<CharacterRig> _load(String name, AssetBundle bundle) async {
    final text = await bundle.loadString(
      'assets/animations/char_${name}_rig.json',
    );
    final json = jsonDecode(text) as Map<String, dynamic>;
    final images = <String, ui.Image>{};
    final parts = json['parts'] as Map<String, dynamic>;
    await Future.wait([
      for (final e in parts.entries)
        _image(bundle, e.value['file'] as String).then((img) {
          images[e.key] = img;
        }),
    ]);
    return CharacterRig._(json, images);
  }

  static Future<ui.Image> _image(AssetBundle bundle, String file) async {
    final data = await bundle.load(file);
    final codec = await ui.instantiateImageCodec(data.buffer.asUint8List());
    final frame = await codec.getNextFrame();
    return frame.image;
  }
}

/// SVG gradient in `objectBoundingBox` units, turned into a shader for the
/// bounds of the shape being filled.
class RigGradient {
  RigGradient.fromJson(Map<String, dynamic> json)
    : radial = json['type'] == 'radial',
      a = radialOrStart(json),
      b = json['type'] == 'radial'
          ? Offset(_d(json['r']), 0)
          : Offset(_d(json['x2']), _d(json['y2'])),
      colors = [
        for (final s in json['stops'] as List)
          parseColor(s[1] as String).withValues(alpha: _d(s[2])),
      ],
      stops = [for (final s in json['stops'] as List) _d(s[0])];

  final bool radial;

  /// Radial: center; linear: start point.
  final Offset a;

  /// Radial: (radius, 0); linear: end point.
  final Offset b;
  final List<Color> colors;
  final List<double> stops;

  static Offset radialOrStart(Map<String, dynamic> json) =>
      json['type'] == 'radial'
      ? Offset(_d(json['cx']), _d(json['cy']))
      : Offset(_d(json['x1']), _d(json['y1']));

  Shader shader(Rect bounds) {
    final m = Matrix4.identity()
      ..translateByDouble(bounds.left, bounds.top, 0, 1)
      ..scaleByDouble(bounds.width, bounds.height, 1, 1);
    return radial
        ? ui.Gradient.radial(a, b.dx, colors, stops, TileMode.clamp, m.storage)
        : ui.Gradient.linear(a, b, colors, stops, TileMode.clamp, m.storage);
  }
}

class ArmStyle {
  ArmStyle.fromJson(Map<String, dynamic> json)
    : w0 = _d(json['w0']),
      w1 = _d(json['w1']),
      bulge = _d(json['bulge']),
      handOffset = _d(json['handOffset']);

  final double w0;
  final double w1;
  final double bulge;

  /// Distance of the palm center beyond the end of the arm curve.
  final double handOffset;
}

class SleeveStyle {
  SleeveStyle.fromJson(Map<String, dynamic> json)
    : fill = json['fill'] as String,
      line = parseColor(json['line'] as String),
      t1 = _d(json['t1']),
      w0 = _d(json['w0']),
      w1 = _d(json['w1']),
      trim = json['trim'] == null ? null : parseColor(json['trim'] as String),
      trimLine = parseColor(json['trimLine'] as String),
      long = json['long'] as bool;

  final String fill;
  final Color line;

  /// Where the sleeve ends along the arm curve (0..1).
  final double t1;
  final double w0;
  final double w1;
  final Color? trim;
  final Color trimLine;
  final bool long;
}

class LegData {
  LegData.fromJson(Map<String, dynamic> json)
    : points = [for (final p in json['points'] as List) _offset(p)],
      w0 = _d(json['w0']),
      w1 = _d(json['w1']),
      bulge = _d(json['bulge']),
      foot = _offset(json['foot']);

  final List<Offset> points;
  final double w0;
  final double w1;
  final double bulge;
  final Offset foot;
}

class ShadowStyle {
  ShadowStyle.fromJson(Map<String, dynamic> json)
    : center = Offset(_d(json['cx']), _d(json['cy'])),
      ry = _d(json['ry']),
      color = parseColor(
        json['color'] as String,
      ).withValues(alpha: _d(json['opacity']));

  final Offset center;
  final double ry;
  final Color color;
}

/// Geometry of an open eye: iris center (x for the left eye), radii.
class IrisGeometry {
  IrisGeometry.fromJson(Map<String, dynamic> json)
    : x = _d(json['x']),
      y = _d(json['y']),
      r = _d(json['r']),
      pupil = _d(json['pupil']);

  final double x;
  final double y;
  final double r;
  final double pupil;
}

class EyeStyle {
  EyeStyle.fromJson(Map<String, dynamic> json)
    : x = [for (final v in json['x'] as List) _d(v)],
      cy = _d(json['cy']),
      rx = _d(json['rx']),
      ry = _d(json['ry']),
      line = parseColor(json['line'] as String),
      lineWidth = _d(json['lineWidth']),
      iris = json['iris'] as String,
      pupil = parseColor(json['pupil'] as String),
      open = {for (final k in json['open'] as List) k as String},
      geometry = {
        for (final e in (json['geometry'] as Map<String, dynamic>).entries)
          e.key: IrisGeometry.fromJson(e.value as Map<String, dynamic>),
      };

  /// Centers of the left and right eye.
  final List<double> x;
  final double cy;
  final double rx;
  final double ry;
  final Color line;
  final double lineWidth;
  final String iris;
  final Color pupil;

  /// Eye kinds with a visible iris.
  final Set<String> open;
  final Map<String, IrisGeometry> geometry;
}

class ArmPose {
  ArmPose.fromJson(Map<String, dynamic> json)
    : points = [for (final p in json['points'] as List) _offset(p)],
      kind = json['kind'] as String,
      handRot = json['handRot'] == null ? null : _d(json['handRot']),
      front = json['layer'] == 'front',
      fold = json['fold'] == null ? null : _d(json['fold']);

  /// Cubic Bezier from the shoulder to the wrist.
  final List<Offset> points;

  /// Hand: `back`, `palm`, `fist` or `thumb`.
  final String kind;

  /// Fixed hand rotation in degrees; null follows the arm.
  final double? handRot;

  /// Drawn in front of the head.
  final bool front;

  /// For a forearm that crosses in front of the upper arm: the point of the
  /// curve (0..1) after which it is drawn again over the sleeve.
  final double? fold;
}

class SparkleData {
  SparkleData(this.position, this.scale, this.color);

  SparkleData.fromJson(List<dynamic> json)
    : position = Offset(_d(json[0]), _d(json[1])),
      scale = _d(json[2]),
      color = parseColor(json[3] as String);

  final Offset position;
  final double scale;
  final Color color;
}

class PoseData {
  PoseData.fromJson(Map<String, dynamic> json)
    : lift = _d(json['lift']),
      lean = _d(json['lean']),
      shadow = _d(json['shadow']),
      arms = {
        for (final a in json['arms'] as List)
          (a as Map<String, dynamic>)['side'] as String: ArmPose.fromJson(a),
      },
      eyes = [for (final e in json['face']['eyes'] as List) e as String],
      look = _offset(json['face']['look']),
      brows = json['face']['brows'] as String,
      mouth = json['face']['mouth'] as String,
      tilt = _d(json['face']['tilt']),
      blush = json['face']['blush'] as bool,
      sparkles = [
        for (final s in json['sparkles'] as List)
          SparkleData.fromJson(s as List<dynamic>),
      ],
      marks = json['marks'] as bool;

  final double lift;
  final double lean;
  final double shadow;

  /// `L` and `R` arms.
  final Map<String, ArmPose> arms;
  final List<String> eyes;
  final Offset look;
  final String brows;
  final String mouth;
  final double tilt;
  final bool blush;
  final List<SparkleData> sparkles;
  final bool marks;
}

/// Parses `#RRGGBB`.
Color parseColor(String hex) =>
    Color(0xFF000000 | int.parse(hex.substring(1), radix: 16));

/// Parses an SVG path made of absolute `M`, `L` and `Z` commands only.
Path parseLinePath(String d) {
  final path = Path();
  final tokens = RegExp(r'[MLZ]|-?\d*\.?\d+').allMatches(d).map((m) => m[0]!);
  var command = 'M';
  final numbers = <double>[];
  void flush() {
    for (var i = 0; i + 1 < numbers.length; i += 2) {
      final x = numbers[i];
      final y = numbers[i + 1];
      if (command == 'M' && i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    numbers.clear();
  }

  for (final t in tokens) {
    if (t == 'M' || t == 'L' || t == 'Z') {
      flush();
      if (t == 'Z') {
        path.close();
      } else {
        command = t;
      }
    } else {
      numbers.add(double.parse(t));
    }
  }
  flush();
  return path;
}

double _d(Object? v) => (v as num).toDouble();

Offset _offset(Object? v) {
  final l = v as List;
  return Offset(_d(l[0]), _d(l[1]));
}

Size _size(Object? v) {
  final l = v as List;
  return Size(_d(l[0]), _d(l[1]));
}

Rect _rect(Object? v) {
  final l = v as List;
  return Rect.fromLTWH(_d(l[0]), _d(l[1]), _d(l[2]), _d(l[3]));
}

/// Degrees to radians.
double rad(double degrees) => degrees * math.pi / 180;
