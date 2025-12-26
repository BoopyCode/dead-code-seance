#!/usr/bin/env python3
"""Dead Code Séance - Summon the ghosts of code past to decide their fate."""

import re
import sys
from pathlib import Path
from collections import defaultdict

# Ghosts of code past whisper their regrets through these patterns
COMMENT_PATTERNS = [
    r'#.*TODO.*',          # The ghost of good intentions
    r'#.*FIXME.*',         # The ghost of technical debt
    r'#.*HACK.*',          # The ghost of desperation
    r'#.*XXX.*',           # The ghost of "this will bite us"
    r'#.*\b(?:remove|delete)\b.*',  # The ghost of procrastination
]

# The great beyond where all commented code goes to rest
COMMENTED_BLOCK_PATTERN = r'(?s)(?:^|\n)\s*#.*?(?=\n\s*[^#\s]|\Z)'

def summon_ghosts(filepath):
    """Summon the spectral remains of commented code."""
    try:
        content = Path(filepath).read_text()
    except Exception as e:
        print(f"Failed to summon from {filepath}: {e}")
        return {}
    
    ghosts = defaultdict(list)
    
    # Find haunted comment blocks (more than 2 lines)
    for match in re.finditer(COMMENTED_BLOCK_PATTERN, content):
        block = match.group()
        lines = block.count('\n') + 1
        if lines > 2:  # Single-line ghosts are less dangerous
            ghosts['long_blocks'].append((match.start(), lines, block[:100]))
    
    # Find cursed annotations
    for i, line in enumerate(content.split('\n'), 1):
        for pattern in COMMENT_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                ghosts['cursed'].append((i, line.strip()))
                break
    
    return ghosts

def conduct_seance(filepath):
    """Conduct a séance to determine if code can rest in peace."""
    ghosts = summon_ghosts(filepath)
    
    if not ghosts:
        print(f"\n🔮 {filepath} is spiritually clean!")
        print("   These comments may pass to the great git log in the sky.")
        return True
    
    print(f"\n👻 {filepath} is HAUNTED!")
    
    if ghosts.get('cursed'):
        print("\nCURSED ANNOTATIONS (handle with care):")
        for line_num, line in ghosts['cursed'][:5]:  # Show first 5
            print(f"  Line {line_num}: {line}")
    
    if ghosts.get('long_blocks'):
        print(f"\nLONG DEAD BLOCKS ({len(ghosts['long_blocks'])} found):")
        print("  These ghosts might contain forgotten business logic.")
        print("  Consider: 1) Reviving it 2) Proper burial (delete) 3) Exorcism (git blame)")
    
    return False

def main():
    """Main ritual - call forth the spirits from command line."""
    if len(sys.argv) < 2:
        print("Usage: python dead_code_seance.py <file1> [file2 ...]")
        print("Example: python dead_code_seance.py *.py")
        sys.exit(1)
    
    print("🔮 Beginning Dead Code Séance...")
    print("   The spirits will decide their fate.")
    
    all_clean = True
    for filepath in sys.argv[1:]:
        if not conduct_seance(filepath):
            all_clean = False
    
    if all_clean:
        print("\n🎉 All files are ready for the great deletion!")
    else:
        print("\n⚠️  Some files contain restless spirits. Proceed with caution.")

if __name__ == "__main__":
    main()
