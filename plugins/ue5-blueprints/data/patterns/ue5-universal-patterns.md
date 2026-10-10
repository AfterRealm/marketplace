# Universal UE5 Blueprint Anti-Patterns

These patterns apply to ANY UE5 Blueprint project. They represent common bugs that are easy to create and hard to spot visually in the Blueprint editor.

---

## P-001: BreakStruct Copy Bug
- **Severity:** CRITICAL
- **Detection:** Any BreakStruct output pin feeding into an array-mutating node's TargetArray pin (Array_Set, Array_Resize, Array_Clear, Array_Add, Array_Remove, Array_Insert, Array_Append) — even through Reroute chains.
- **Why:** BreakStruct returns disconnected copies. Any mutation writes to a throwaway copy. The original struct is never modified.
- **NOT a bug when:** BreakStruct output feeds a READ-ONLY operation. Safe targets: Array_Length, Get (a Copy), ForEachLoop source, Contains, Find, Last Index, Is Valid Index, Is Empty.
- **Fix:** MakeStruct reassembly + write-back to the original variable.

## P-002: Missing Write-Back After Struct Modification
- **Severity:** CRITICAL
- **Detection:** A struct field is modified but never reassembled via MakeStruct and written back to the original array/variable.
- **Why:** Struct fields in UE5 Blueprints are value types. Modifying a field in isolation doesn't propagate back unless you explicitly reconstruct and write back.
- **Fix:** After modifying any field, MakeStruct with all fields (modified + pass-through) then write back to original location.

## P-003: Uninitialized Variable Read
- **Severity:** HIGH
- **Detection:** A Get Variable node is read before any Set Variable in the execution flow path.
- **Why:** Uninitialized variables return CDO defaults (often 0, empty array, or None). Can cause index-out-of-bounds, null dereferences, or silent wrong behavior.
- **Fix:** Initialize in Class Defaults, or add a Set before the first Get, or add a Branch/IsValid guard.

## P-004: Missing IsValid Check
- **Severity:** HIGH
- **Detection:** A Cast node, GetComponentsByClass result, or array Get result is used without an IsValid/Branch check.
- **Why:** Accessing members on an invalid/null reference crashes the game or silently fails.
- **Fix:** Add IsValid check. Wire True exec to logic, False exec to early return or skip.

## P-005: Wrong Cast Type
- **Severity:** HIGH
- **Detection:** A Cast To node targets a class the source object can never actually be.
- **Why:** Cast always fails, intended logic never runs.
- **Fix:** Change cast target to the correct class. Trace source object's actual type.

## P-006: Disconnected Execution Wire (Dead Code)
- **Severity:** MEDIUM
- **Detection:** A node exists but never appears in any execution flow. Or an exec chain terminates at a node with unwired output exec pin.
- **Why:** The node's logic never runs. If it should, the function is silently incomplete.
- **Fix:** Wire the disconnected node into the correct execution chain.

## P-007: ForEachLoop Modifying Its Own Source Array
- **Severity:** HIGH
- **Detection:** A ForEachLoop iterates over an array, and within the LoopBody, the same array is modified.
- **Why:** Modifying an array while iterating causes undefined behavior — skipped elements, index-out-of-bounds, or infinite loops.
- **Fix:** Copy the array to a local variable before the loop. Iterate the copy, modify the original.

## P-008: Execution Through Wrong Branch
- **Severity:** MEDIUM
- **Detection:** Both True and False branches of a Branch node lead to the same downstream node, but one path skips required setup.
- **Why:** Downstream node may receive uninitialized or wrong data.
- **Fix:** Ensure each branch path sets up all required state.

## P-009: Integer Division Truncation
- **Severity:** LOW
- **Detection:** Integer Divide where result is used for something expecting fractional precision.
- **Why:** Integer division truncates. 7 / 10 = 0, not 0.7.
- **Fix:** Convert to float before dividing if fractional result is needed.

## P-010: Switch/Branch Default Not Wired
- **Severity:** HIGH
- **Detection:** A Switch node where the Default pin has no exec wire. Or a multi-branch chain where the final else is unwired.
- **Why:** Unhandled cases silently drop execution.
- **Fix:** Wire Default to appropriate fallthrough.

---

## Extended Patterns

## P-011: Pure Node Re-evaluation in Loops
- **Severity:** HIGH
- **Detection:** A pure function (no exec pins) used inside a ForEachLoop or ForLoop that gets called on every iteration but should only be called once.
- **Why:** Pure nodes re-execute every time their output is read. Inside loops, this means redundant work or inconsistent results if the function has side effects.
- **Fix:** Cache the result in a local variable before the loop.

## P-012: Delegate Leak
- **Severity:** HIGH
- **Detection:** A Bind Event node without a corresponding Unbind, especially in actors that can be spawned and destroyed.
- **Why:** Bound delegates prevent garbage collection. Memory grows with each spawn/destroy cycle.
- **Fix:** Unbind in EndPlay or BeginDestroy.

## P-013: Latent Node in ForEachLoop
- **Severity:** CRITICAL
- **Detection:** A Delay, AI MoveTo, or other latent node inside a ForEachLoop body.
- **Why:** Latent nodes break the loop — the loop doesn't wait, it continues immediately. Only the last iteration's latent action fires.
- **Fix:** Use an index variable + timer/event pattern instead of a loop.

## P-014: Delay on Tick
- **Severity:** HIGH
- **Detection:** A Delay node triggered from Event Tick.
- **Why:** Tick fires every frame. Each tick spawns a new Delay. After 1 second at 60fps, you have 60 pending delays all firing at once.
- **Fix:** Use a boolean gate, or Set Timer by Function Name instead.

## P-015: FlipFlop in Function
- **Severity:** HIGH
- **Detection:** A FlipFlop node inside a function (not an event).
- **Why:** FlipFlop state persists on the CDO, not per-instance. All instances share the same flip state.
- **Fix:** Use a boolean variable toggled manually, or move to an event.

## P-016: Hard Reference Cast
- **Severity:** MEDIUM
- **Detection:** A Cast To node referencing a large Blueprint class (especially levels, game modes, or asset-heavy actors) in a frequently-loaded Blueprint.
- **Why:** The cast creates a hard reference. Loading the casting Blueprint loads the entire cast target into memory. Can cause massive memory bloat.
- **Fix:** Use soft references, interfaces, or Blueprint Function Libraries.

## P-017: GetAllActorsOfClass on Tick
- **Severity:** HIGH
- **Detection:** GetAllActorsOfClass called from Event Tick or a high-frequency timer.
- **Why:** Iterates every actor in the level every frame. Severe performance hit.
- **Fix:** Cache the result, use overlap events, or find actors once in BeginPlay.

## P-018: Unguarded Array Get
- **Severity:** HIGH
- **Detection:** Array Get node where the index is not validated against Array Length first.
- **Why:** Out-of-bounds access crashes or returns garbage data.
- **Fix:** Add Array Length check before Get, or use "Get (a copy)" with IsValid.

## P-019: Timer String Mismatch
- **Severity:** HIGH
- **Detection:** Set Timer by Function Name where the string doesn't match any function name in the Blueprint.
- **Why:** Timer fires but function isn't found. Silent failure with no error in shipping builds.
- **Fix:** Verify function name matches exactly (case-sensitive).

## P-020: Sequence + Latent Node
- **Severity:** HIGH
- **Detection:** A Sequence node where one output leads to a latent node (Delay, MoveTo, etc.).
- **Why:** Sequence doesn't wait for latent nodes. All outputs fire immediately, only the execution AFTER the latent node is delayed.
- **Fix:** Chain latent nodes sequentially instead of using Sequence.

## P-021: Map Find Without IsValid
- **Severity:** MEDIUM
- **Detection:** Map.Find result used without checking the boolean output.
- **Why:** If key doesn't exist, the value output is default-initialized garbage.
- **Fix:** Always check the boolean output before using the value.

## P-022: Construction Script Side Effects
- **Severity:** MEDIUM
- **Detection:** Construction Script that spawns actors, modifies other actors, or has gameplay effects.
- **Why:** Construction Script runs in the editor AND at runtime, often multiple times. Side effects multiply.
- **Fix:** Move gameplay logic to BeginPlay.

## P-023: Multicast Without RepNotify
- **Severity:** HIGH
- **Detection:** A multicast RPC that modifies a replicated variable without using RepNotify.
- **Why:** Late-joining clients get the replicated value but never see the RPC, so the associated logic never fires for them.
- **Fix:** Use RepNotify on the variable instead of (or in addition to) the multicast.

## P-024: Non-exhaustive Enum Switch
- **Severity:** MEDIUM
- **Detection:** A Switch on Enum where not all enum values have wired outputs and Default is unwired.
- **Why:** Adding new enum values silently falls through to nothing.
- **Fix:** Wire all cases or wire Default to a fallback.

## P-025: Widget Leak
- **Severity:** HIGH
- **Detection:** Create Widget called repeatedly without checking if the widget already exists.
- **Why:** Each call creates a new widget. Old ones stay in memory unless explicitly removed.
- **Fix:** Check IsValid on the widget variable first, only create if null.

---

## Pattern Co-occurrence

When you find one pattern, check for its common partners:

| If you find... | Also check for... |
|----------------|-------------------|
| P-001 (BreakStruct Copy) | P-002 (Missing Write-Back) |
| P-004 (Missing IsValid) | P-005 (Wrong Cast Type) |
| P-006 (Dead Code) | P-010 (Unwired Default) |
| P-007 (ForEach modifying source) | P-001 (BreakStruct Copy) |
| P-013 (Latent in ForEach) | P-020 (Sequence + Latent) |
| P-014 (Delay on Tick) | P-017 (GetAllActors on Tick) |
| P-025 (Widget Leak) | P-004 (Missing IsValid) |
