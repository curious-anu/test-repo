import os
import subprocess
import time
from datetime import datetime
import winsound 
import webbrowser

def play_success_sound():
    """Plays a happy beep on successful sync."""
    winsound.Beep(1000, 300)

def ensure_gitignore():
    """Checks for .gitignore and creates a basic one if missing."""
    if not os.path.exists(".gitignore"):
        print("\n\033[93m📝 GitGlide Suggestion: No .gitignore found. I can create one for you...\033[0m")
        choice = input("Keep your repo clean? (y/n): ").lower()
        if choice == 'y':
            content = "__pycache__/\n*.py[cod]\n*$py.class\n.env\nvenv/\nenv/\n.vscode/\n.DS_Store\n"
            with open(".gitignore", "w") as f:
                f.write(content)
            print("✅ .gitignore created! (Temporary files will now be ignored)")

def handle_undo():
    """Emergency cleanup for stuck states and optional commit rollback."""
    print("\n\033[91m⚠️ Cleaning up ghost states...\033[0m")
    # Force abort any stuck rebases or merges
    subprocess.run(["git", "rebase", "--abort"], capture_output=True)
    subprocess.run(["git", "merge", "--abort"], capture_output=True)
    
    choice = input("⏪ Would you like to UNDO your last local commit? (y/n): ").lower()
    if choice == 'y':
        result = subprocess.run(["git", "reset", "--soft", "HEAD~1"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Commit undone. Files are safe but 'uncommitted'.")
        else:
            print("💡 No commit to undo, but your workspace is now clean!")

def get_current_branch():
    """Detects the current active branch name."""
    try:
        result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        branch = result.stdout.strip()
        return branch if branch else "main"
    except:
        return "main"

def smart_push_logic():
    print("\n\033[94m🚀 GitGlide: Preparing to Sync...\033[0m")

    active_branch = get_current_branch()
    print(f"📂 Detected active Branch: \033[92m{active_branch}\033[0m")

    branch_input = input(f"Push to '{active_branch}'? (Enter for Yes / Type branch name): ").strip().lower()
    target_branch = active_branch if branch_input in ["", "yes", "y"] else branch_input
    
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    custom_msg = input(f"💬 Enter commit message (Enter for '{now}'): ").strip()
    final_msg = custom_msg if custom_msg else f"Auto-update: {now}"

    try:
        # STEP 1: Stage and Commit
        subprocess.run(["git", "add", "."], check=True)
        commit_check = subprocess.run(["git", "commit", "-m", final_msg], capture_output=True, text=True)
        
        if "nothing to commit" in commit_check.stdout:
            print("💡 Nothing new to commit locally, checking GitHub...")

        # STEP 2: Push with Auto-Healer
        print(f"📡 Pushing to {target_branch}...")
        result = subprocess.run(["git", "push", "origin", target_branch], capture_output=True, text=True)

        if result.returncode != 0:
            if "rejected" in result.stderr.lower() or "conflict" in result.stderr.lower():
                print(f"\n\033[93m⚠️ CONFLICT! GitHub has updates that clash with your local changes.\033[0m")
                print("How should I fix this for you?")
                print("1. \033[92mKeep MY version\033[0m (Overwrite GitHub's line)")
                print("2. \033[94mKeep GITHUB version\033[0m (Overwrite my local line)")
                print("3. I'll fix it manually in VS Code")
                
                choice = input("\nSelect (1/2/3): ").strip()

                if choice == '1':
                    print("🔄 Applying 'Ours' strategy...")
                    subprocess.run(["git", "pull", "--rebase", "-Xours", "origin", target_branch])
                    subprocess.run(["git", "push", "origin", target_branch])
                    msg = "Your version is now live!"
                elif choice == '2':
                    print("🔄 Applying 'Theirs' strategy...")
                    subprocess.run(["git", "pull", "--rebase", "-Xtheirs", "origin", target_branch])
                    subprocess.run(["git", "push", "origin", target_branch])
                    msg = "GitHub's version was kept."
                else:
                    print("🆗 Please fix the arrows in VS Code and run GitGlide again.")
                    return

                play_success_sound()
                print(f"\033[92m✨ SUCCESS! {msg}\033[0m")
            else:
                print(f"\033[91m❌ Push failed: {result.stderr}\033[0m")
                handle_undo()
        else:
            play_success_sound()
            print(f"\n\033[92m✅ SUCCESS! {target_branch} updated at {now}\033[0m")

            if input("🌍 Open GitHub page? (y/n): ").lower() == 'y':
                url_res = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True)
                web_url = url_res.stdout.strip().replace(".git", "")
                webbrowser.open(web_url)

    except Exception as e:
        print(f"❌ Error: {e}")
        handle_undo()

def setup_new_repo():
    print("\n\033[94m🌟 SETUP MODE: Creating a new GitHub bridge...\033[0m")
    repo_url = input("Paste your GitHub Repo URL: ").strip()
    if not repo_url:
        print("❌ URL cannot be empty!")
        return

    ensure_gitignore()

    if input("Create a README.md? (y/n): ").lower() == 'y':
        desc = input("Project description: ")
        with open("README.md", "w") as f:
            f.write(f"# Project\n\n{desc}\n\nSynced with GitGlide.")

    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial setup via GitGlide"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        play_success_sound()
        print("\n\033[92m✨ SUCCESS! Repository linked and pushed.\033[0m")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

if __name__ == "__main__":
    os.system('color') 
    print("--- ✨ GitGlide v1.4: Professional Git Automation ---")
    
    if not os.path.exists(".git"):
        setup_new_repo()
    else:
        ensure_gitignore()
        smart_push_logic()

    print("\nClosing in 10 seconds...")
    time.sleep(10)