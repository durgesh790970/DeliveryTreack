#!/usr/bin/env python
"""Check for mismatches between imageNameMap and actual image files"""

import os
import re

# Get actual image files
images_dir = 'frontend/static/images'
actual_files = set()
for f in os.listdir(images_dir):
    if f.endswith(('.jpg', '.jpeg')):
        actual_files.add(f)

# Read menu.html imageNameMap
with open('frontend/templates/menu.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract imageNameMap
start = content.find('const imageNameMap = {')
end = content.find('};', start) + 2
map_section = content[start:end]

# Parse imageNameMap
image_mappings = {}
pattern = r"'([^']+)':\s*'([^']+)'"
for match in re.finditer(pattern, map_section):
    item_name = match.group(1)
    image_file = match.group(2)
    image_mappings[item_name] = image_file

# Check for mismatches and missing entries
print("\n" + "=" * 80)
print("🔍 IMAGE MAPPING VALIDATION REPORT")
print("=" * 80)

# Find missing mappings
food_items = []
start = content.find('const foodItems = [')
end = content.find('];', start)
items_section = content[start:end]
item_pattern = r"{name: '([^']+)'"
for match in re.finditer(item_pattern, items_section):
    food_items.append(match.group(1))

missing_mappings = []
for item in food_items:
    if item not in image_mappings:
        missing_mappings.append(item)

print(f"\n❌ MISSING MAPPINGS ({len(missing_mappings)} items):")
for item in missing_mappings:
    print(f"  - {item}")

# Find file mismatches (mapped but file doesn't exist)
print(f"\n❌ MISSING IMAGE FILES ({len([m for m in image_mappings.values() if m not in actual_files])} items):")
for item, mapped_file in sorted(image_mappings.items()):
    if mapped_file not in actual_files:
        print(f"  - {item}: mapped to '{mapped_file}' (NOT FOUND)")
        # Try to find similar files
        similar = [f for f in actual_files if item.lower().replace(' - ', ' ').replace(' ', '').startswith(item.lower().replace(' - ', ' ').replace(' ', '')[:5])]
        if similar:
            print(f"    Similar files: {similar}")

# Pizza-specific check
print(f"\n🍕 PIZZA ITEMS CHECK:")
pizza_items = [f"'{item}': '{img}'" for item, img in sorted(image_mappings.items()) if 'pizza' in item.lower() or 'garlic' in item.lower()]
for item in pizza_items:
    print(f"  ✓ {item}")

print("\n" + "=" * 80)
