import os
import subprocess
import time
from datetime import datetime
import winsound 
import webbrowser

def play_success_sound():
    winsound.Beep(1000, 300)

def ensure_gitignore():
    """Checks for .gitignore and creates a basic one for Python/Web if missing."""
    if not os.path.exists(".gitignore"):
        print("\n\033[93m📝 GitGlide Suggestion: No .gitignore found. I can create a standard one for you..(.env,cache etc.)\033[0m")
        choice = input("Would you like to create a .gitignore and keep your repo clean and secure? (y/n): ").lower()

        if choice == 'y':
            content = "__pycache__/\n*.py[cod]\n*$py.class\n.env\nvenv/\nenv/\n.vscode/\n.DS_Store\n"
            with open(".gitignore", "w") as f:
                f.write(content)
            print("✅ .gitignore created! (Temporary files will now be ignored thus keeping your project clean)")
        else:
            print("No problem! I will upload ever single thing.")

def handle_undo():
    """Option to undo the last local commit if something went wrong."""
    choice = input("\n\033[91m⏪ Would you like to UNDO the last commit? (y/n): \033[0m").lower()
    if choice == 'y':
        subprocess.run(["git", "reset", "--soft", "HEAD~1"])
        print("✅ Last commit undone. Your files are safe but 'uncommitted'.")

def get_current_branch():
    """detects the current active branch name."""
    try:
        result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        branch = result.stdout.strip()
        return branch if branch else "main"
    except:
        return "main"

def smart_push_logic():
    print("\n\033[94m🚀 GitGlide: Preparing to Sync...\033[0m")

    active_branch = get_current_branch()
    print(f"📂Detected active Branch: \033[92m{active_branch}\033[0m")

    branch_input = input(f"Push to '{active_branch}'? (Yes/Type branch name): ").strip()
    target_branch = branch_input if branch_input else active_branch
    
    # Feature: Personalized Commit Message
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    custom_msg = input(f"💬 Enter commit message (Enter for '{now}'): ").strip()
    final_msg = custom_msg if custom_msg else f"Auto-update: {now}"

    try:
        # Step 1: Add and Commit
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", final_msg], check=True)
        
        # Step 2: Try to Push
        print(f"📡 Pushing to GitHub on branch '{target_branch}'...")
        result = subprocess.run(["git", "push", "origin", target_branch], capture_output=True, text=True)

        # Feature: The Auto-Healer (Conflict Resolution)
        if result.returncode != 0:
            if "rejected" in result.stderr.lower():
                print(f"\n\033[93m⚠️ Conflict Detected! GitHub has updates on '{target_branch}' that you don't have.\033[0m")
                print(f"🔄 Auto-Healer: Syncing (Rebasing) {target_branch} safely...")
                
                sync = subprocess.run(["git", "pull", "--rebase", "origin", target_branch], capture_output=True, text=True)
                
                if sync.returncode == 0:
                    print("✅ Sync Successful! Retrying push...")
                    subprocess.run(["git", "push", "origin", target_branch])
                    play_success_sound()
                    print(f"\033[92m✨ SUCCESS! Your work and GitHub's work are now merged and live!.\033[0m")
                else:
                    print("\033[91m❌ Manual Help Needed: There is a 'Merge Conflict' in your files.\033[0m")
                    handle_undo()
            else:
                print(f"\033[91m❌ Push failed: {result.stderr}\033[0m")
                handle_undo()
        else:
            play_success_sound()
            print(f"\n\033[92m✅ SUCCESS!{target_branch} updated at {now}\033[0m")

            open_web = input("Would you like to open the GitHub page? (y/n): ").lower()
            if open_web == 'y':
                url_res = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True)
                web_url = url_res.stdout.strip().replace(".git", "")
                webbrowser.open(web_url)


    except Exception as e:
        print(f"❌ An error occurred: {e}")
        handle_undo()

def setup_new_repo():
    print("\n\033[94m🌟 SETUP MODE: Creating a new GitHub bridge...\033[0m")
    repo_url = input("Paste your GitHub Repo URL: ").strip()
    if not repo_url:
        print("❌ URL cannot be empty!")
        return

    ensure_gitignore() # Check gitignore even in setup!

    make_readme = input("Do you want to create a README.md? (y/n): ").lower()
    if make_readme == 'y':
        project_name = input("Enter a short project description: ")
        with open("README.md", "w") as f:
            f.write(f"# {project_name}\n\nAutomated by GitGlide.")

    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial setup via GitGlide"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        play_success_sound()
        print("\n\033[92m✨ ALL DONE! Your repo is now linked and pushed.\033[0m")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

if __name__ == "__main__":
    os.system('color') 
    print("--- ✨ GitGlide: Professional Git Automation ---")
    
    if not os.path.exists(".git"):
        setup_new_repo()
    else:
        ensure_gitignore()
        smart_push_logic()

    print("\nClosing in 10 seconds...")
    time.sleep(10)