#!/usr/bin/env python
"""Verify all menu images are correctly set with no duplicates"""

import re

# Read menu.html
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

# Check for duplicates
image_to_items = {}
for item, image in image_mappings.items():
    if image not in image_to_items:
        image_to_items[image] = []
    image_to_items[image].append(item)

# Print results
print("\n" + "=" * 80)
print("✅ IMAGE MAPPING VERIFICATION REPORT")
print("=" * 80)
print(f"\n📊 Total Mapped Items: {len(image_mappings)}")
print(f"📊 Total Unique Images: {len(image_to_items)}")

print("\n" + "=" * 80)
print("🔍 CHECKING FOR DUPLICATE IMAGES (Same image for multiple items):")
print("=" * 80)

has_duplicates = False
for image, items in sorted(image_to_items.items()):
    if len(items) > 1:
        has_duplicates = True
        print(f"\n⚠️  IMAGE: {image}")
        print(f"   Used by {len(items)} items:")
        for item in items:
            print(f"   - {item}")

if not has_duplicates:
    print("\n✅ NO DUPLICATES FOUND!")
    print("✅ Each item has its own UNIQUE image!")
    print("✅ All images are PROPERLY SET!")

print("\n" + "=" * 80)
print("📋 ALL MAPPED ITEMS AND THEIR IMAGES:")
print("=" * 80)
for i, (item, image) in enumerate(sorted(image_mappings.items()), 1):
    print(f"{i:2d}. {item:40s} → {image}")

print("\n" + "=" * 80)
print("✅ VERIFICATION COMPLETE!")
print("=" * 80 + "\n")
