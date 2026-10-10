## Suggest Projectile Velocity Moving Target
**Category:** Game
**Search:** "Suggest Projectile Velocity Moving Target"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Projectile Start Location (vector) — Location the projectile is launched from
- Target Actor (object) — Actor that the projectile should hit in TimeToTarget seconds
- Target Location Offset (vector) — Offset to apply to the location the projectile is aiming for
- Gravity ZOverride (real) — Optional override of WorldGravityZ
- Time to Target (real) — Time (in seconds) between the projectile being launched and the projectile hitting the TargetActor - clamped to be at least 0.1
- Draw Debug Type (enum)
- Draw Debug Time (real)
- Draw Debug Color (linearcolor)

**Outputs:**
- Out (exec)
- Out Launch Velocity (vector) — The launch velocity returned from this calculation
- Return Value (boolean)

**Description:** Returns a launch velocity need for a projectile to hit the TargetActor in TimeToTarget seconds based on the TargetActor's current velocity. This assumes the projectile is only accelerated by gravity (i.e. no outside forces), and that the TargetActor is moving at a constant velocity.
---
