## Break ARFilter
**Category:** Utilities
**Search:** "Break ARFilter"
**Target:** Kismet System Library

**Inputs:**
- In ARFilter (struct)

**Outputs:**
- Package Names (name)
- Package Paths (name)
- Soft Object Paths (struct)
- Class Paths (struct)
- Recursive Class Paths Exclusion Set (struct)
- Class Names (name) — [DEPRECATED] - Class names are now represented by path names. Please use the ClassPaths output instead.
- Recursive Classes Exclusion Set (name) — [DEPRECATED] - Class names are now represented by path names. Please use the RecursiveClassPathsExclusionSet output instead.
- Recursive Paths (boolean)
- Recursive Classes (boolean)
- Include Only on Disk Assets (boolean)

**Description:** Breaks an ARFilter struct into its component pieces. You should be using ClassPaths and RecursiveClassPathsExclusionSet from this node, ClassNames and RecursiveClassesExclusionSet are deprecated.
---
