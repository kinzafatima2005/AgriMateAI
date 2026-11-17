import os
import sys
import subprocess
import zipfile
import shutil

SDK = r"C:\Users\SMART TECH\AppData\Local\Android\Sdk"
BUILD_TOOLS = os.path.join(SDK, "build-tools", "35.0.0")
PLATFORM_JAR = os.path.join(SDK, "platforms", "android-35", "android.jar")
AAPT2 = os.path.join(BUILD_TOOLS, "aapt2.exe")
D8 = os.path.join(BUILD_TOOLS, "d8.bat")
ZIPALIGN = os.path.join(BUILD_TOOLS, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS, "apksigner.bat")
ADB = os.path.join(SDK, "platform-tools", "adb.exe")

JBR_BIN = r"C:\Program Files\Android\Android Studio\jbr\bin"
JAVAC = os.path.join(JBR_BIN, "javac.exe")
KEYTOOL = os.path.join(JBR_BIN, "keytool.exe")

BASE_DIR = os.path.abspath("android_build")
SRC_DIR = os.path.join(BASE_DIR, "src")
RES_DIR = os.path.join(BASE_DIR, "res")
GEN_DIR = os.path.join(BASE_DIR, "gen")
CLASSES_DIR = os.path.join(BASE_DIR, "classes")
DEX_DIR = os.path.join(BASE_DIR, "dex")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MANIFEST = os.path.join(BASE_DIR, "AndroidManifest.xml")

COMPILED_RES = os.path.join(BASE_DIR, "compiled_res.zip")
UNALIGNED_APK = os.path.join(BASE_DIR, "unaligned.apk")
ALIGNED_APK = os.path.join(BASE_DIR, "aligned.apk")
FINAL_APK = os.path.abspath("AgriMate.apk")
KEYSTORE = os.path.join(BASE_DIR, "debug.keystore")

def run(cmd, desc):
    print(f"\n[STEP] {desc}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] {desc} failed:")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        sys.exit(1)
    print(f"[OK] {desc} succeeded.")
    return res

def main():
    print("=" * 60)
    print("BUILDING NATIVE STANDALONE ANDROID APK (AgriMate.apk)")
    print("=" * 60)

    for d in [GEN_DIR, CLASSES_DIR, DEX_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

    # 1. Compile Resources with aapt2
    cmd1 = f'"{AAPT2}" compile --dir "{RES_DIR}" -o "{COMPILED_RES}"'
    run(cmd1, "Compiling XML & Mipmap Resources with AAPT2")

    # 2. Link Resources with aapt2
    cmd2 = (
        f'"{AAPT2}" link -o "{UNALIGNED_APK}" -I "{PLATFORM_JAR}" '
        f'--manifest "{MANIFEST}" "{COMPILED_RES}" --java "{GEN_DIR}" --auto-add-overlay'
    )
    run(cmd2, "Linking Resources and Generating R.java")

    # 3. Compile Java Source Files
    java_files = [
        os.path.join(SRC_DIR, "pk", "agrimate", "ai", "MainActivity.java"),
        os.path.join(GEN_DIR, "pk", "agrimate", "ai", "R.java")
    ]
    java_files_str = " ".join([f'"{f}"' for f in java_files])
    cmd3 = f'"{JAVAC}" -source 8 -target 8 -cp "{PLATFORM_JAR}" -d "{CLASSES_DIR}" {java_files_str}'
    run(cmd3, "Compiling Java Sources with JDK 21 (Target 1.8 Bytecode)")

    # 4. Convert Class Bytecode to Dalvik Executable (classes.dex)
    class_files = [
        f'"{os.path.join(CLASSES_DIR, "pk", "agrimate", "ai", f)}"'
        for f in os.listdir(os.path.join(CLASSES_DIR, "pk", "agrimate", "ai"))
        if f.endswith(".class")
    ]
    cmd4 = f'"{D8}" --output "{DEX_DIR}" {" ".join(class_files)}'
    run(cmd4, "Compiling Classes to DEX with D8")

    # 5. Pack classes.dex and assets into unaligned.apk
    print("\n[STEP] Adding classes.dex and assets/ into unaligned APK...")
    dex_file = os.path.join(DEX_DIR, "classes.dex")
    with zipfile.ZipFile(UNALIGNED_APK, "a", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(dex_file, "classes.dex")
        for root, _, files in os.walk(ASSETS_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                z.write(full_path, rel_path.replace("\\", "/"))
    print("[OK] Packaged classes.dex and assets/ into APK.")

    # 6. Zipalign APK (4-byte boundary)
    if os.path.exists(ALIGNED_APK):
        os.remove(ALIGNED_APK)
    cmd6 = f'"{ZIPALIGN}" -v -p -f 4 "{UNALIGNED_APK}" "{ALIGNED_APK}"'
    run(cmd6, "Zipaligning APK on 4-byte boundaries")

    # 7. Generate Keystore if needed and Sign APK
    if not os.path.exists(KEYSTORE):
        cmd_ks = (
            f'"{KEYTOOL}" -genkey -v -keystore "{KEYSTORE}" -storepass android '
            f'-alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 '
            f'-dname "CN=AgriMate, OU=AgriTech, O=AgriMate AI, L=Multan, S=Punjab, C=PK"'
        )
        run(cmd_ks, "Generating AgriMate Android Debug Keystore")

    if os.path.exists(FINAL_APK):
        os.remove(FINAL_APK)
    shutil.copyfile(ALIGNED_APK, FINAL_APK)

    cmd7 = f'"{APKSIGNER}" sign --ks "{KEYSTORE}" --ks-pass pass:android --key-pass pass:android "{FINAL_APK}"'
    run(cmd7, "Signing AgriMate.apk with apksigner (v1, v2, v3 schemes)")

    # 8. Check ADB device connection and Install if available
    adb_check = subprocess.run(f'"{ADB}" devices', shell=True, capture_output=True, text=True)
    has_device = any(line.strip().endswith("device") for line in adb_check.stdout.splitlines() if line.strip())

    if has_device:
        cmd8 = f'"{ADB}" install -r "{FINAL_APK}"'
        run(cmd8, "Installing AgriMate.apk onto Connected Phone")

        # Also push to Download folder as convenient direct installer APK
        subprocess.run(f'"{ADB}" push "{FINAL_APK}" /sdcard/Download/AgriMate.apk', shell=True)

        # 9. Launch Native App
        cmd9 = f'"{ADB}" shell am start -n pk.agrimate.ai/.MainActivity'
        run(cmd9, "Launching AgriMate AI Native App on Phone Screen")
        print("\n" + "=" * 60)
        print("SUCCESS: AGRIMATE AI NATIVE APP IS INSTALLED & RUNNING ON YOUR PHONE!")
    else:
        print("\n" + "=" * 60)
        print("SUCCESS: AgriMate.apk COMPILED & SIGNED READY!")
        print("No USB device detected at the moment. Connect phone to install or open AgriMate.apk.")
    print(f"APK Location: {FINAL_APK}")
    print("Package: pk.agrimate.ai")
    print("=" * 60)

if __name__ == "__main__":
    main()

