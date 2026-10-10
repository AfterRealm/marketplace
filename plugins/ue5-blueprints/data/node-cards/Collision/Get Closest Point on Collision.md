## Get Closest Point on Collision
**Category:** Collision
**Search:** "Get Closest Point on Collision"
**Target:** Primitive Component

**Inputs:**
- Target (object)
- Point (vector) — World 3D vector
- Bone Name (name) — If a SkeletalMeshComponent, name of body to set center of mass of. 'None' indicates root body.

**Outputs:**
- Out Point on Body (vector) — Point on the surface of collision closest to Point
- Return Value (real) — Success if returns > 0.f, if returns 0.f, it is either not convex or inside of the point If returns < 0.f, this primitive does not have collsion

**Description:** Returns the distance and closest point to the collision surface. Component must have simple collision to be queried for closest point.
---
