import json
from pathlib import Path

backup_path = "/home/santhosh/Documents/Strivers_local/dsa-tracker/data/dsa-progress-backup-2026-04-16.json"
out_dir = Path("/home/santhosh/Documents/Strivers_local/dsa-tracker/data/data_files")

with open(backup_path) as f:
    backup_data = json.load(f)

progress = {}
streaks = {}

for item in backup_data.get("progress", []):
    q_id = item.get("question_id")
    if not q_id: continue
    
    is_completed = item.get("completed", False)
    is_revision = item.get("marked_for_revision", False)
    
    status = "done" if is_completed else "todo"
    
    date_str = item.get("completed_date")
    if not date_str:
        date_str = item.get("updated_date", "")[:10]
    
    if status != "todo" or is_revision or item.get("notes"):
        progress[q_id] = {
            "status": status,
            "revision": is_revision,
            "last_updated": date_str,
            "note": item.get("notes", "")
        }
        
    if status == "done" and date_str:
        streaks[date_str] = streaks.get(date_str, 0) + 1

with open(out_dir / "progress.json", "w") as f:
    json.dump(progress, f, indent=2)

with open(out_dir / "streaks.json", "w") as f:
    json.dump(streaks, f, indent=2)

print("Progress JSON updated with independent revision flags!")
