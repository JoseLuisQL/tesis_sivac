import subprocess
import csv

# Query WMI for WINWORD processes with /Automation
cmd = 'wmic process where "name=\'WINWORD.EXE\'" get ProcessId,CommandLine /format:csv'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("Processes found:")
for line in res.stdout.splitlines():
    if "WINWORD.EXE" in line and "/Automation" in line:
        parts = line.strip().split(",")
        pid = parts[-1].strip()
        print(f"Killing hung automation Word PID {pid}...")
        subprocess.run(f"taskkill /F /PID {pid}", shell=True)
print("Done killing hung automation processes.")
