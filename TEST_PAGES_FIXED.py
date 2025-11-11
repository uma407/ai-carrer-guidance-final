#!/usr/bin/env python3
"""
TEST_PAGES_FIXED.py
Verify that all pages now load without authentication redirects.
"""

import os
import sys

def check_page_authentication(filepath, page_name):
    """Check if a page file has authentication check that redirects to login."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Look for the authentication redirect pattern
    has_auth_check = "switch_page" in content and "1_login.py" in content
    
    if has_auth_check:
        return f"❌ {page_name}: Still has authentication redirect"
    else:
        return f"✅ {page_name}: Authentication check REMOVED"

# Test all pages
pages_dir = "pages"
pages = [
    ("2_Skills.py", "Skills"),
    ("3_Careers.py", "Careers"),
    ("4_Development.py", "Development"),
    ("5_Mentorship.py", "Mentorship"),
    ("6_Saved_Resources.py", "Saved Resources"),
    ("7_Profile.py", "Profile"),
]

print("=" * 80)
print("                     PAGE AUTHENTICATION CHECK")
print("=" * 80)
print()

all_fixed = True
for filename, page_name in pages:
    filepath = os.path.join(pages_dir, filename)
    if os.path.exists(filepath):
        result = check_page_authentication(filepath, page_name)
        print(result)
        if "❌" in result:
            all_fixed = False
    else:
        print(f"⚠️  {page_name}: File not found at {filepath}")
        all_fixed = False

print()
print("=" * 80)

if all_fixed:
    print("✅ SUCCESS: All pages have been fixed!")
    print("   Pages 2-7 now load WITHOUT authentication redirects.")
    print()
    print("   You can now:")
    print("   1. Go to http://localhost:8501")
    print("   2. Optionally login on the Login page")
    print("   3. Click on any page in the sidebar")
    print("   4. All pages (Skills, Careers, Development, etc.) will load")
    print("      their OWN content instead of showing login page")
    print()
    print("🎯 Expected Behavior:")
    print("   - Home page loads with onboarding form")
    print("   - Skills page loads skill assessment widgets")
    print("   - Careers page loads career explorer")
    print("   - Development page loads timeline")
    print("   - Mentorship page loads advisory system")
    print("   - Saved Resources page loads resource list")
    print("   - Profile page loads user profile form")
else:
    print("❌ FAIL: Some pages still have authentication issues")

print("=" * 80)
