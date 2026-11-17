# Builder script to assemble complete, clean frontend/mobile_web/index.html
# with dedicated Farmer, Buyer, and Expert dashboards.

import os
import shutil

OUTPUT_FILE = r"frontend/mobile_web/index.html"
ANDROID_FILE = r"android_build/assets/www/index.html"

# We will construct the complete HTML with all screens, modals, styles, and scripts.
print("Building full frontend with role-specific dashboards...")

