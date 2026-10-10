"""
Runner — executes a Python script inside a running UE5 Editor via remote execution.
Usage: python run_in_editor.py <script.py> [--timeout SECONDS]

Requires: pip install upyrc
Requires: UE5 Editor running with Python Remote Execution enabled.
"""
import sys
import argparse
from pathlib import Path
from upyrc.upyre import PythonRemoteConnection

parser = argparse.ArgumentParser(description="Run a Python script inside UE5 Editor")
parser.add_argument("script", help="Path to the .py script to execute")
parser.add_argument("--timeout", type=float, default=120.0, help="Execution timeout in seconds (default: 120)")
args = parser.parse_args()

script_path = Path(args.script)

# Search relative to this file's directory if not found directly
if not script_path.exists():
    candidate = Path(__file__).parent / script_path.name
    if candidate.exists():
        script_path = candidate

if not script_path.exists():
    print(f"Script not found: {args.script}")
    sys.exit(1)

print(f"Running: {script_path}")
try:
    remote = PythonRemoteConnection()
    remote.open_connection()
    result = remote.execute_template_file(script_path, timeout=args.timeout)
    for entry in result.output:
        print(f"[{entry['type']}] {entry['output']}")
    if not result.success:
        print("\n*** SCRIPT FAILED ***")
        remote.close_connection()
        sys.exit(1)
    remote.close_connection()
except Exception as e:
    print(f"Connection failed: {e}")
    print("Is the UE5 Editor running with Remote Execution enabled?")
    sys.exit(1)
