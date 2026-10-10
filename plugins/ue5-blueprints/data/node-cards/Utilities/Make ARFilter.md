## Make ARFilter
**Category:** Utilities
**Search:** "Make ARFilter"
**Target:** Kismet System Library

**Inputs:**
- Package Names (name)
- Package Paths (name)
- Soft Object Paths (struct)
- Class Paths (struct)
- Recursive Class Paths Exclusion Set (struct)
- Class Names (name) — [DEPRECATED] - Class names are now represented by path names. If non-empty, this input will result in a runtime warning. Please use the ClassPaths input instead.
- Recursive Classes Exclusion Set (name) — [DEPRECATED] - Class names are now represented by path names. If non-empty, this input will result in a runtime warning. Please use the RecursiveClassPathsExclusionSet input instead.
- Recursive Paths (boolean)
- Recursive Classes (boolean)
- Include Only on Disk Assets (boolean)

**Outputs:**
- Return Value (struct)

**Description:** Builds an ARFilter struct. You should be using ClassPaths and RecursiveClassPathsExclusionSet, ClassNames and RecursiveClassesExclusionSet are deprecated.
---
