import os
import subprocess
import time
from datetime import datetime

def run_git_push():
    # 1. Validation Check
    if not os.path.exists(".git"):
        print("❌ ERROR: No .git folder found!")
        print("Please make sure this script is inside your GitHub project folder.")
        time.sleep(5)
        return

    try:
        # 2. Start the Process
        now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        print(f"--- Anu's Auto-Push Initialized ---")
        print(f"Time: {now}")
        print("\nPlease wait... almost there... ⏳")

        # 3. Execute Git Commands
        subprocess.run(["git", "add", "."], check=True)
        
        commit_msg = f"Auto-update: {now}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # We use 'git push' - it will push to your current branch
        subprocess.run(["git", "push"], check=True)

        # 4. Success Message
        print("\n" + "="*35)
        print(f"✅ SUCCESS! Your code is on GitHub.")
        print(f"Timestamp: {now}")
        print("="*35)

    except subprocess.CalledProcessError:
        print("\n❌ Oops! Git had an issue (maybe nothing to commit or no internet?)")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

    # 5. The Pause
    print("\nClosing window in 5 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    run_git_push()
