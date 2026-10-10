## Make Hit Result
**Category:** Collision
**Search:** "Make Hit Result"
**Target:** Gameplay Statics

**Inputs:**
- Blocking Hit (boolean) — True if there was a blocking hit, false otherwise.
- Initial Overlap (boolean) — True if the hit started in an initial overlap. In this case some other values should be interpreted differently. Time will be 0, ImpactPoint will equal Location, and normals will be equal and indicate a depenetration vector.
- Time (real) — 'Time' of impact along trace direction ranging from [0.0 to 1.0) if there is a hit, indicating time between start and end. Equals 1.0 if there is no hit.
- Distance (real) — The distance from the TraceStart to the Location in world space. This value is 0 if there was an initial overlap (trace started inside another colliding object).
- Location (vector) — Location of the hit in world space. If this was a swept shape test, this is the location where we can place the shape in the world where it will not penetrate.
- Impact Point (vector) — Location of the actual contact point of the trace shape with the surface of the hit object. Equal to Location in the case of an initial overlap.
- Normal (vector) — Normal of the hit in world space, for the object that was swept (e.g. for a sphere trace this points towards the sphere's center). Equal to ImpactNormal for line tests.
- Impact Normal (vector) — Normal of the hit in world space, for the object that was hit by the sweep.
- Phys Mat (object) — Physical material that was hit. Must set bReturnPhysicalMaterial to true in the query params for this to be returned.
- Hit Actor (object) — Actor hit by the trace.
- Hit Component (object) — PrimitiveComponent hit by the trace.
- Hit Bone Name (name) — Name of the bone hit (valid only if we hit a skeletal mesh).
- Bone Name (name) — Name of the trace bone hit (valid only if we hit a skeletal mesh).
- Hit Item (integer) — Primitive-specific data recording which item in the primitive was hit
- Element Index (integer) — If colliding with a primitive with multiple parts, index of the part that was hit.
- Face Index (integer) — If colliding with trimesh or landscape, index of face that was hit.
- Trace Start (vector)
- Trace End (vector)

**Outputs:**
- Return Value (struct)

**Description:** Create a HitResult struct
---
