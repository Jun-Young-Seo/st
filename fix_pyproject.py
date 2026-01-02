#!/usr/bin/env python3
"""Remove AWS CodeArtifact sources from pyproject.toml files"""

import re
from pathlib import Path

def fix_pyproject(file_path):
    """Remove AWS source sections from pyproject.toml"""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove AWS source sections
    # Pattern: [[tool.poetry.source]] followed by name/url/priority for epc-power or third-party
    pattern = r'\[\[tool\.poetry\.source\]\]\s*\n\s*name\s*=\s*["\'](?:epc-power|third-party)["\'][\s\S]*?(?=\n\[|\Z)'
    content = re.sub(pattern, '', content)
    
    # Ensure PyPI is set as primary if no sources remain
    if '[[tool.poetry.source]]' not in content:
        # Add PyPI as primary source before [tool.poetry.dependencies]
        content = re.sub(
            r'(\[tool\.poetry\.dependencies\])',
            r'[[tool.poetry.source]]\nname = "PyPI"\npriority = "primary"\n\n\1',
            content
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

# Fix main project
fix_pyproject('pyproject.toml')

# Fix submodule
submodule_pyproject = Path('sub/epyqlib/pyproject.toml')
if submodule_pyproject.exists():
    fix_pyproject(submodule_pyproject)
else:
    print(f"Submodule pyproject.toml not found at {submodule_pyproject}")

print("All pyproject.toml files fixed!")

