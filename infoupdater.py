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

def update_descriptions():
    """Main function to update descriptions"""
    descriptions = load_descriptions()
    git_files = get_git_committed_files()
    
    if not git_files:
        print("No files found in git repository")
        return
    
    print(f"\nFound {len(git_files)} files in repository\n")
    
    for filename in git_files:
        if filename and filename != '.gitignore':  # Skip empty strings and .gitignore
            if filename in descriptions:
                print(f"✓ '{filename}' already has a description:")
                for line in descriptions[filename]:
                    print(f"  - {line}")
                choice = input("\nDo you want to update it? (y/n): ").strip().lower()
                if choice != 'y':
                    continue
            else:
                print(f"\n→ New file: '{filename}'")
            
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
            
            if lines:
                descriptions[filename] = lines
    
    # Save updated descriptions
    save_descriptions(descriptions)
    print("\n✓ Update complete!")

if __name__ == "__main__":
    update_descriptions()