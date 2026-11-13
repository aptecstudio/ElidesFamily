import 'dart:async';
import 'dart:math' as math;
import 'dart:ui';

import 'package:flutter/foundation.dart';

import 'character_frame.dart';
import 'character_rig.dart';

/// Short animated actions, played on top of the resting pose.
enum CharacterAction {
  /// Waves "hi" with the right hand.
  wave,

  /// "Hooray!": raised arms and two happy hops.
  cheer,

  /// Laughs and wiggles, as if tickled.
  giggle,

  /// A little jump of surprise.
  surprise,
}

/// Drives a character: smooth transitions between poses, the always-on
/// layers (breathing, blinking, tail, looking around) and short actions.
///
/// Time only advances through [tick], which [CharacterView] calls every
/// frame; tests can call it directly.
class CharacterController extends ChangeNotifier {
  CharacterController({String pose = 'idle', math.Random? random})
    : _pose = pose,
      _random = random ?? math.Random();

  final math.Random _random;
  CharacterRig? _rig;
  String _pose;

  CharacterFrame? _from;
  CharacterFrame? _to;
  double _blend = 1;
  double _blendSeconds = 0.35;

  double _time = 0;
  double _nextBlink = 1.5;
  double _blinkEnd = -1;
  Offset _gaze = Offset.zero;
  Offset _gazeTarget = Offset.zero;
  double _nextGaze = 2.5;

  final List<_Scheduled> _schedule = [];
  final List<_Effect> _effects = [];
  Completer<void>? _action;
  CharacterAction? _lastAction;
  CharacterFrame? _frame;

  /// The resting pose (the one the character goes back to after an action).
  String get pose => _pose;

  /// True while an action is playing.
  bool get isBusy => _action != null;

  /// The frame to draw; null until a rig is attached.
  CharacterFrame? get frame => _frame;

  /// Connects the loaded rig; the character starts in its resting pose.
  void attach(CharacterRig rig) {
    _rig = rig;
    _to = CharacterFrame.fromPose(rig.poses[_pose]!);
    _from = null;
    _blend = 1;
    tick(0);
  }

  /// Moves smoothly to [pose] and stays there.
  void setPose(String pose, {double seconds = 0.35}) {
    _pose = pose;
    _goTo(pose, seconds);
  }

  /// Plays a random reaction to a touch, never the same twice in a row.
  Future<void> react() {
    final choices = [
      CharacterAction.wave,
      CharacterAction.cheer,
      CharacterAction.giggle,
    ]..remove(_lastAction);
    return play(choices[_random.nextInt(choices.length)]);
  }

  /// Plays [action]; ignored if another action is still playing.
  Future<void> play(CharacterAction action) {
    if (_action != null || _rig == null) {
      return _action?.future ?? Future.value();
    }
    _lastAction = action;
    final done = _action = Completer<void>();
    final t0 = _time;
    final rest = _pose;
    void at(double seconds, VoidCallback run) =>
        _schedule.add(_Scheduled(t0 + seconds, run));
    void effect(double start, double seconds, _Apply apply) =>
        _effects.add(_Effect(t0 + start, seconds, apply));
    void finish(double seconds) => at(seconds, () {
      _action = null;
      done.complete();
    });

    switch (action) {
      case CharacterAction.wave:
        _goTo('wave', 0.3);
        effect(0.25, 1.6, (f, t) {
          final arm = f.arms['R'];
          if (arm == null) return f;
          final swing = 11 * math.sin(2 * math.pi * 2.2 * t * 1.6);
          final env = math.sin(math.pi * t);
          final p = arm.points;
          return f.copyWith(
            arms: {
              ...f.arms,
              'R': arm.copyWith(
                points: [
                  p[0],
                  p[1],
                  p[2] + Offset(swing * env * 0.5, 0),
                  p[3] + Offset(swing * env, -2 * env),
                ],
              ),
            },
          );
        });
        at(1.9, () => _goTo(rest, 0.4));
        finish(2.3);
      case CharacterAction.cheer:
        _goTo('cheer', 0.25);
        effect(0.2, 1.0, (f, t) {
          final phase = (t * 2) % 1;
          final h = math.sin(math.pi * phase);
          return f.copyWith(
            lift: f.lift - 26 * h,
            squash: f.squash + 0.035 * math.cos(2 * math.pi * phase),
          );
        });
        at(1.5, () => _goTo(rest, 0.45));
        finish(2.0);
      case CharacterAction.giggle:
        _goTo('giggle', 0.2);
        effect(0.1, 1.0, (f, t) {
          final env = math.sin(math.pi * t);
          final shake = math.sin(2 * math.pi * 5 * t);
          return f.copyWith(
            tilt: f.tilt + 5 * shake * env,
            lift: f.lift - 4 * shake.abs() * env,
            squash: f.squash + 0.02 * shake * env,
          );
        });
        at(1.15, () => _goTo(rest, 0.35));
        finish(1.5);
      case CharacterAction.surprise:
        _goTo('surprised', 0.15);
        effect(0, 0.4, (f, t) {
          return f.copyWith(lift: f.lift - 14 * math.sin(math.pi * t));
        });
        at(1.3, () => _goTo(rest, 0.4));
        finish(1.7);
    }
    return done.future;
  }

  /// Advances the animation by [dt] seconds.
  void tick(double dt) {
    final rig = _rig;
    if (rig == null) return;
    _time += dt;
    if (_blend < 1) {
      _blend = math.min(1, _blend + dt / _blendSeconds);
    }
    final due = _schedule.where((s) => s.time <= _time).toList();
    _schedule.removeWhere(due.contains);
    for (final s in due) {
      s.run();
    }

    var f = _base().copyWith(time: _time);
    f = _alive(f, dt);
    for (final e in _effects) {
      final t = (_time - e.start) / e.seconds;
      if (t >= 0 && t <= 1) f = e.apply(f, t);
    }
    _effects.removeWhere((e) => _time > e.start + e.seconds);
    _frame = f;
    notifyListeners();
  }

  void _goTo(String pose, double seconds) {
    final rig = _rig;
    if (rig == null) return;
    _from = _base();
    _to = CharacterFrame.fromPose(rig.poses[pose]!);
    _blend = 0;
    _blendSeconds = seconds;
  }

  CharacterFrame _base() {
    final from = _from;
    final to = _to!;
    if (from == null || _blend >= 1) return to;
    return CharacterFrame.lerp(from, to, _easeInOut(_blend));
  }

  /// The layers that make the character feel alive even when still.
  CharacterFrame _alive(CharacterFrame f, double dt) {
    const breathPeriod = 3.2;
    final breath = math.sin(2 * math.pi * _time / breathPeriod);

    // Blink every few seconds, sometimes twice.
    if (_time >= _nextBlink) {
      _blinkEnd = _time + 0.14;
      _nextBlink = _random.nextDouble() < 0.2
          ? _time + 0.35
          : _time + 2.2 + _random.nextDouble() * 3.2;
    }
    final open = _rig!.eyes.open;
    final eyes = _time < _blinkEnd
        ? [for (final e in f.eyes) open.contains(e) ? 'closed' : e]
        : f.eyes;

    // Look around now and then, only while resting.
    if (!isBusy && _pose == 'idle') {
      if (_time >= _nextGaze) {
        _gazeTarget = _random.nextDouble() < 0.4
            ? Offset.zero
            : Offset(
                (_random.nextDouble() * 2 - 1) * 7,
                _random.nextDouble() * 8 - 5,
              );
        _nextGaze = _time + 1.8 + _random.nextDouble() * 3;
      }
    } else {
      _gazeTarget = Offset.zero;
    }
    _gaze += (_gazeTarget - _gaze) * math.min(1, dt * 6);

    return f.copyWith(
      breathe: 0.012 * breath,
      headBob: 1.6 * math.sin(2 * math.pi * _time / breathPeriod + 0.6),
      tailAngle: 5 * math.sin(2 * math.pi * _time / 2.8),
      eyes: eyes,
      look: f.look + _gaze,
    );
  }

  static double _easeInOut(double t) =>
      t < 0.5 ? 4 * t * t * t : 1 - math.pow(-2 * t + 2, 3) / 2;
}

typedef _Apply = CharacterFrame Function(CharacterFrame frame, double t);

class _Scheduled {
  _Scheduled(this.time, this.run);

  final double time;
  final VoidCallback run;
}

class _Effect {
  _Effect(this.start, this.seconds, this.apply);

  final double start;
  final double seconds;
  final _Apply apply;
}
