"""
Universal Blueprint T3D Exporter
Exports any UE5 Blueprint as T3D text — contains ALL node data including
pin connections (LinkedTo lines).

This script runs INSIDE the UE5 Editor via remote execution.
Configure targets by writing a JSON file before running.

Config file: <output_dir>/export_targets.json
Format:
[
  {"path": "/Game/MyProject/BP_Player", "output": "BP_Player.t3d"},
  {"path": "/Game/MyProject/BP_Enemy",  "output": "BP_Enemy.t3d"}
]

Environment: Set UE5BP_OUTPUT_DIR and UE5BP_TARGETS_FILE before execution,
or edit the defaults below.
"""
import unreal
import os
import json

# Defaults — overridden by env vars if set
OUTPUT_DIR = os.environ.get("UE5BP_OUTPUT_DIR", "C:/ue5bp_export")
TARGETS_FILE = os.environ.get("UE5BP_TARGETS_FILE", os.path.join(OUTPUT_DIR, "export_targets.json"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load targets
if os.path.exists(TARGETS_FILE):
    with open(TARGETS_FILE, 'r') as f:
        TARGETS = json.load(f)
    print("Loaded {} targets from {}".format(len(TARGETS), TARGETS_FILE))
else:
    print("No targets file at {}".format(TARGETS_FILE))
    print("Create export_targets.json with: [{\"path\": \"/Game/...\", \"output\": \"name.t3d\"}]")
    TARGETS = []

for target in TARGETS:
    bp_path = target["path"]
    out_file = os.path.join(OUTPUT_DIR, target["output"])

    bp = unreal.load_asset(bp_path)
    if not bp:
        print("ERROR: Could not load {}".format(bp_path))
        continue

    task = unreal.AssetExportTask()
    task.set_editor_property('object', bp)
    task.set_editor_property('filename', out_file)
    task.set_editor_property('automated', True)
    task.set_editor_property('prompt', False)

    result = unreal.Exporter.run_asset_export_task(task)
    if result:
        size = os.path.getsize(out_file)
        print("OK: {} — {} bytes".format(target["output"], size))
    else:
        print("ERROR: Export failed for {}".format(bp_path))

if TARGETS:
    print("\nDone. {} files exported to {}".format(len(TARGETS), OUTPUT_DIR))
