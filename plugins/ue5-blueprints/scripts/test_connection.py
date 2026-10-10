"""
Test connection to UE5 Editor's Python Remote Execution.
Usage: python test_connection.py
"""
from upyrc.upyre import PythonRemoteConnection

print("Connecting to UE5 Editor...")
try:
    remote = PythonRemoteConnection()
    remote.open_connection()
    result = remote.execute_template_string("print('UE5 connection OK — engine version: ' + str(unreal.SystemLibrary.get_engine_version()))")
    for entry in result.output:
        print(f"[{entry['type']}] {entry['output']}")
    remote.close_connection()
    if result.success:
        print("\nConnected to UE5 Editor successfully!")
    else:
        print("\nConnection opened but test command failed.")
except Exception as e:
    print(f"\nFailed to connect: {e}")
    print("\nTroubleshooting:")
    print("  1. Is the UE5 Editor running?")
    print("  2. Is 'Python Editor Script Plugin' enabled? (Edit > Plugins)")
    print("  3. Is Remote Execution enabled? (Edit > Project Settings > Python)")
    print("  4. Firewall blocking UDP 6766 or TCP 53320?")
