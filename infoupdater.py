import json
import subprocess
import os

def get_git_committed_files():
    """Get list of files that have been committed to git"""
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git not found")
        return []

def get_changed_files():
    """Get list of changed files from git"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        changed = result.stdout.strip().split('\n')
        return [f for f in changed if f]
    except subprocess.CalledProcessError:
        print("Error: Could not get changed files")
        return []

def load_descriptions(filename='descriptions.json'):
    """Load existing descriptions from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_descriptions(descriptions, filename='descriptions.json'):
    """Save descriptions to JSON file with proper formatting"""
    with open(filename, 'w') as f:
        json.dump(descriptions, f, indent=2)
    print(f"✓ Descriptions saved to {filename}")

def get_description(filename):
    """Get description for a file from user input"""
    print(f"Enter description(s) for '{filename}' (press Enter twice when done):")
    lines = []
    while True:
        line = input("  > ").strip()
        if not line:
            if lines:
                break
            print("  Please enter at least one line of description")
            continue
        lines.append(line)
    return lines

def update_descriptions():
    """Main function to update descriptions"""
    descriptions = load_descriptions()
    git_files = get_git_committed_files()
    changed_files = get_changed_files()
    
    if not git_files:
        print("No files found in git repository")
        return
    
    print(f"\nFound {len(git_files)} files in repository")
    print(f"Found {len(changed_files)} changed files\n")
    
    updated_files = []
    
    # Step 1: Ask for descriptions of changed files
    if changed_files:
        print("=" * 50)
        print("STEP 1: Update descriptions for changed files")
        print("=" * 50 + "\n")
        
        for filename in changed_files:
            if filename and filename != '.gitignore':
                print(f"\n→ Changed file: '{filename}'")
                lines = get_description(filename)
                
                if lines:
                    descriptions[filename] = lines
                    updated_files.append(filename)
    else:
        print("No changed files found.\n")
    
 # Step 2: Ask if user wants to update descriptions for unchanged files
    print("\n" + "=" * 50)
    unchanged_files = [f for f in git_files if f and f != '.gitignore' and f not in changed_files]
    
    if unchanged_files and descriptions:
        print("STEP 2: Update descriptions for unchanged files")
        print("=" * 50)
        choice = input("\nDo you want to update descriptions of any previously updated files? (y/n): ").strip().lower()
        
        if choice == 'y':
            print(f"\nFound {len(unchanged_files)} unchanged files\n")
            
            for filename in unchanged_files:
                if filename in descriptions:
                    print(f"\n✓ '{filename}' already has a description:")
                    for line in descriptions[filename]:
                        print(f"  - {line}")
                    update_choice = input("\nDo you want to update it? (y/n): ").strip().lower()
                    if update_choice == 'y':
                        lines = get_description(filename)
                        if lines:
                            descriptions[filename] = lines
                            updated_files.append(filename)
    
    # Save updated descriptions
    if updated_files:
        save_descriptions(descriptions)
        print(f"\n✓ Update complete! Updated {len(updated_files)} file(s)")
    else:
        print("\n✓ No files were updated")

if __name__ == "__main__":
    update_descriptions()