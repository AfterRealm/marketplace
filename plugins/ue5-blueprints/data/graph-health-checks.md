# Blueprint Graph Health Checks

Universal heuristic checks that catch problems no specific anti-pattern covers. These are based on general Blueprint graph properties and apply to any UE5 project.

Run these on every function you analyze.

---

## Execution Flow Health

### Dead-end exec path
An execution wire chain that stops without reaching Return, another function call, or a terminal node. Every exec branch should go somewhere meaningful.
- **Severity:** MEDIUM-HIGH (depends on what's dead)
- **Detection:** Trace every exec output pin. If any chain terminates at a node whose output exec pins are all unwired, flag it.

### Orphaned nodes
Nodes that exist in the graph but have NO exec wires in or out AND no data wires feeding into connected nodes. These are dead weight.
- **Severity:** LOW (usually leftover from editing)
- **Detection:** Any node not referenced in Execution Flow or Data Wiring sections.

### Unreachable exec branches
A Branch True/False pin or Switch case pin that's wired but can never fire based on the data flow feeding the condition.
- **Severity:** MEDIUM
- **Detection:** If a Branch's condition is a literal True/False constant, one branch is dead.

---

## Variable Health

### Write-only variable
A variable is Set but never Get anywhere in this function (or any other function if you can check).
- **Severity:** LOW (potential dead code)
- **Detection:** Variable appears in Set nodes but not Get nodes.

### Read-before-write
A variable is Get before any Set in the execution flow.
- **Severity:** MEDIUM (may read stale/default values)
- **Detection:** Trace exec flow — if Get appears before Set on any path from Entry.

### Multiple unguarded writes
Two or more Set nodes write to the same variable on parallel exec paths (both branches of a Branch) with no merge.
- **Severity:** MEDIUM (last-write-wins can be unpredictable)
- **Detection:** Same variable Set on both True and False branches.

---

## Node Health

### Cast with unwired failure
A Cast node where the "Cast Failed" exec pin has nothing wired. If the cast fails, execution silently stops.
- **Severity:** HIGH (silent failure)
- **Detection:** Cast node with Cast Failed exec pin having no LinkedTo.

### ForEachLoop with unwired Completed
The Completed exec pin is disconnected — nothing happens after the loop finishes.
- **Severity:** MEDIUM (may be intentional if function just loops and returns)
- **Detection:** ForEachLoop Completed pin with no LinkedTo.

### Array Get without bounds check
Array Get using an index that isn't validated against Array Length first.
- **Severity:** HIGH (crash risk)
- **Detection:** ArrayGet node where the Index input doesn't trace back to a Length check.

### Select/Switch with missing cases
A Select or Switch node where not all enum values or expected cases are wired.
- **Severity:** MEDIUM
- **Detection:** Switch node with unwired case pins and no Default wired.

---

## Array Safety

### Empty array guard
A ForEachLoop or Array Get where the source array could be empty and there's no Array Length or IsEmpty guard.
- **Severity:** HIGH (silent visual bugs or crash)
- **Detection:** ForEachLoop/ArrayGet with no Length > 0 Branch guard before it in the exec flow.

### Modulo with zero divisor
Percent_IntInt (modulo) where the divisor comes from Array Length that could be 0.
- **Severity:** HIGH (divide by zero crash)
- **Detection:** Modulo node where divisor traces back to Array Length without a > 0 guard.

---

## Data Flow Health

### Dangling required input
A node's required input pin is disconnected and has no default value. Node may behave unexpectedly.
- **Severity:** MEDIUM
- **Detection:** Input pin with no LinkedTo and no DefaultValue (excluding self pins and optional pins).

### Excessive reroute chain
Chain of 3+ Reroute (Knot) nodes in sequence.
- **Severity:** LOW (readability, not a bug)
- **Detection:** Reroute → Reroute → Reroute chains.

---

## Cross-Function Checks

### Save/Restore field mismatch
If both SaveState and RestoreState functions exist, check that they pack and unpack data in the same order with the same indices.
- **Severity:** CRITICAL
- **Detection:** Compare array indices and field order between paired save/restore functions.

### Missing parent call
An overridden function that doesn't call Parent at any point in its execution flow.
- **Severity:** HIGH (base class logic never runs)
- **Detection:** Override function with no CallParentFunction node in exec flow.

### Parameter propagation gap
A function that passes an object reference to sub-functions, but one sub-function in the chain doesn't receive it.
- **Severity:** HIGH (downstream operations silently fail on null)
- **Detection:** Trace object references through call chains.

---

## Reporting Format

```
HEURISTIC FINDINGS:
  [H1] Dead-end exec: Branch_0.True -> nothing (exec chain stops)
  [H2] Cast unwired failure: CastToActor_0 has no Cast Failed wiring
  [H3] ForEachLoop_1.Completed is disconnected
  [OK] No write-only variables detected
  [OK] No orphaned nodes detected
```

Tag findings as `[H#]` separate from pattern bugs `[Bug#]`. Not every heuristic finding is a bug — some are intentional. Use judgment.
