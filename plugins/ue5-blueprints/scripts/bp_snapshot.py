"""
Universal Blueprint Graph Snapshot
Dumps graph structure to JSON for any UE5 Blueprint — actors, widgets, anything.

This script runs INSIDE the UE5 Editor via remote execution.
Configure targets by writing a JSON file before running.

Config file: <output_dir>/snapshot_targets.json
Format:
[
  {
    "path": "/Game/MyProject/BP_Player",
    "output": "BP_Player_snapshot.json",
    "graphs": ["EventGraph", "MyFunction"]
  }
]

Set "graphs" to null or omit it to snapshot ALL graphs in the Blueprint.
"""
import unreal
import json
import re
import os
from datetime import datetime

OUTPUT_DIR = os.environ.get("UE5BP_OUTPUT_DIR", "C:/ue5bp_export")
TARGETS_FILE = os.environ.get("UE5BP_SNAPSHOT_FILE", os.path.join(OUTPUT_DIR, "snapshot_targets.json"))

# Friendly names for common engine functions
FUNC_FRIENDLY = {
    "FTrunc": "Truncate",
    "Conv_IntToDouble": "Int to Float",
    "Conv_DoubleToString": "Float to String",
    "Conv_IntToString": "Int to String",
    "Conv_StringToText": "String to Text",
    "Conv_TextToString": "Text to String",
    "Array_Length": "Array Length",
    "Array_Set": "Set Array Elem",
    "Array_Add": "Array Add",
    "Array_Clear": "Array Clear",
    "Array_Get": "Array Get",
    "Array_Resize": "Array Resize",
    "Array_Num": "Array Length",
    "Array_Remove": "Array Remove",
    "Array_Insert": "Array Insert",
    "Array_Contains": "Array Contains",
    "Array_Find": "Array Find",
    "Array_IsEmpty": "Array IsEmpty",
    "Array_LastIndex": "Array LastIndex",
    "Array_IsValidIndex": "Array IsValidIndex",
    "Array_Append": "Array Append",
    "Percent_IntInt": "% (Modulo)",
    "Add_IntInt": "Int + Int",
    "Subtract_IntInt": "Int - Int",
    "Multiply_IntInt": "Int * Int",
    "Divide_IntInt": "Int / Int",
    "Add_DoubleDouble": "Float + Float",
    "Subtract_DoubleDouble": "Float - Float",
    "Multiply_DoubleDouble": "Float * Float",
    "Divide_DoubleDouble": "Float / Float",
    "Less_IntInt": "Int < Int",
    "Greater_IntInt": "Int > Int",
    "LessEqual_IntInt": "Int <= Int",
    "GreaterEqual_IntInt": "Int >= Int",
    "EqualEqual_IntInt": "Int == Int",
    "NotEqual_IntInt": "Int != Int",
    "BooleanAND": "AND",
    "BooleanOR": "OR",
    "Not_PreBool": "NOT",
    "GetDataTableRowNames": "Get Data Table Row Names",
    "GetDataTableRowFromName": "Get Data Table Row",
    "K2_SetText": "Set Text",
    "SetStaticMesh": "Set Static Mesh",
    "SetMaterial": "Set Material",
    "GetComponentsByClass": "GetComponentsByClass",
    "DestroyComponent": "DestroyComponent",
    "AddChildToScrollBox": "Add Child (ScrollBox)",
    "AddChildToHorizontalBox": "Add Child (HBox)",
    "AddChildToVerticalBox": "Add Child (VBox)",
    "ClearChildren": "Clear Children",
    "RemoveFromParent": "Remove From Parent",
    "CreateWidget": "Create Widget",
    "AddToViewport": "Add to Viewport",
    "IsValid": "IsValid",
    "PrintString": "Print String",
    "Delay": "Delay",
    "SetTimer": "Set Timer by Function Name",
    "GetAllActorsOfClass": "Get All Actors of Class",
    "SpawnActor": "Spawn Actor",
    "DestroyActor": "Destroy Actor",
    "GetActorLocation": "Get Actor Location",
    "SetActorLocation": "Set Actor Location",
    "GetActorRotation": "Get Actor Rotation",
    "SetActorRotation": "Set Actor Rotation",
}


def get_member_name(ref):
    try:
        txt = ref.export_text()
        m = re.search(r'MemberName="([^"]+)"', txt)
        return m.group(1) if m else None
    except Exception:
        return None


def get_macro_name(ref):
    try:
        txt = ref.export_text()
        m = re.search(r"StandardMacros:(\w+)'", txt)
        return m.group(1) if m else None
    except Exception:
        return None


def get_real_class(node):
    try:
        node.wc_get_property_value("Pins")
        return node.get_class().get_name()
    except Exception as e:
        match = re.search(r"on '(\w+)'", str(e))
        if match:
            return match.group(1)
        return node.get_class().get_name()


def safe_prop(node, prop_name):
    try:
        return node.wc_get_property_value(prop_name)
    except Exception:
        return None


def extract_node(node):
    info = {}
    info["class"] = get_real_class(node)
    x = safe_prop(node, "NodePosX")
    y = safe_prop(node, "NodePosY")
    info["pos"] = [x if x is not None else 0, y if y is not None else 0]
    comment = safe_prop(node, "NodeComment")
    info["comment"] = comment if comment else None

    cls = info["class"]

    if "VariableGet" in cls or "VariableSet" in cls:
        ref = safe_prop(node, "VariableReference")
        if ref:
            name = get_member_name(ref)
            if name:
                info["variable"] = name
                info["access"] = "GET" if "Get" in cls else "SET"

    if "CallFunction" in cls or "CallArrayFunction" in cls:
        ref = safe_prop(node, "FunctionReference")
        if ref:
            name = get_member_name(ref)
            if name:
                info["function"] = name
                friendly = FUNC_FRIENDLY.get(name)
                if friendly:
                    info["friendly_name"] = friendly

    if "MacroInstance" in cls:
        ref = safe_prop(node, "MacroGraphReference")
        if ref:
            name = get_macro_name(ref)
            if name:
                info["macro"] = name

    if "IfThenElse" in cls:
        info["friendly_name"] = "Branch"
    if "FunctionEntry" in cls:
        info["friendly_name"] = "Entry"
    if "FunctionResult" in cls:
        info["friendly_name"] = "Return"
    if "Knot" in cls:
        info["friendly_name"] = "Reroute"
    if "MakeStruct" in cls:
        info["friendly_name"] = "Make Struct"
    if "BreakStruct" in cls:
        info["friendly_name"] = "Break Struct"
    if "GetArrayItem" in cls:
        info["friendly_name"] = "Get (a copy)"
    if "PromotableOperator" in cls:
        op = safe_prop(node, "OperationName")
        if op:
            info["operation"] = str(op)
    if "DynamicCast" in cls or "ClassDynamicCast" in cls:
        target = safe_prop(node, "TargetType")
        if target:
            info["cast_target"] = str(target.get_name()) if hasattr(target, "get_name") else str(target)[:100]
    if "CreateWidget" in cls:
        wclass = safe_prop(node, "WidgetType")
        if wclass:
            info["widget_class"] = str(wclass.get_name()) if hasattr(wclass, "get_name") else str(wclass)[:100]
    if "CustomEvent" in cls or "Event" in cls:
        name = safe_prop(node, "CustomFunctionName")
        if name:
            info["event_name"] = str(name)
    if "Switch" in cls:
        ref = safe_prop(node, "FunctionReference")
        if ref:
            name = get_member_name(ref)
            if name:
                info["function"] = name

    return info


def scan_graphs(bp, graph_names):
    bel = unreal.BlueprintEditorLibrary
    results = {}
    for graph_name in graph_names:
        print("  Scanning: {}".format(graph_name))
        try:
            graph = bel.find_graph(bp, graph_name)
        except Exception as e:
            results[graph_name] = {"error": str(e)}
            continue
        if graph is None:
            results[graph_name] = {"error": "Graph not found"}
            continue
        try:
            nodes_raw = graph.wc_get_property_value("Nodes")
        except Exception as e:
            results[graph_name] = {"error": str(e)}
            continue
        if not nodes_raw:
            results[graph_name] = {"node_count": 0, "nodes": []}
            continue
        node_list = []
        for idx, node in enumerate(nodes_raw):
            try:
                node_list.append(extract_node(node))
            except Exception as e:
                node_list.append({"class": "ERROR", "error": str(e)[:200], "pos": [0, 0], "comment": None})
        results[graph_name] = {"node_count": len(node_list), "nodes": node_list}
        classes = [n["class"] for n in node_list]
        class_counts = {}
        for c in classes:
            class_counts[c] = class_counts.get(c, 0) + 1
        summary = ["{} x{}".format(c, n) for c, n in sorted(class_counts.items(), key=lambda x: -x[1])]
        print("    {} nodes: {}".format(len(node_list), ", ".join(summary)))
    return results


# === MAIN ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

if os.path.exists(TARGETS_FILE):
    with open(TARGETS_FILE, 'r') as f:
        TARGETS = json.load(f)
    print("Loaded {} targets from {}".format(len(TARGETS), TARGETS_FILE))
else:
    print("No targets file at {}".format(TARGETS_FILE))
    print("Create snapshot_targets.json with target definitions.")
    TARGETS = []

for target in TARGETS:
    bp_path = target["path"]
    out_file = os.path.join(OUTPUT_DIR, target.get("output", bp_path.split("/")[-1] + "_snapshot.json"))

    print("\nLoading: {}".format(bp_path))
    bp = unreal.load_asset(bp_path)
    if bp is None:
        print("  ERROR: Could not load. Skipping.")
        continue

    print("  Loaded successfully.")
    graph_names = target.get("graphs")

    # If no graphs specified, discover all graphs
    if not graph_names:
        try:
            all_graphs = unreal.BlueprintEditorLibrary.get_all_graphs(bp)
            graph_names = [g.get_name() for g in all_graphs] if all_graphs else ["EventGraph"]
        except Exception:
            graph_names = ["EventGraph"]

    graph_results = scan_graphs(bp, graph_names)

    output = {
        "timestamp": datetime.now().isoformat(),
        "blueprint": bp_path,
        "graphs": graph_results,
    }

    out_path = os.path.join(OUTPUT_DIR, target.get("output", bp_path.split("/")[-1] + "_snapshot.json"))
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        print("  Wrote: {}".format(out_path))
    except Exception as e:
        print("  ERROR writing: {}".format(e))

print("\n=== SNAPSHOT COMPLETE ===")
