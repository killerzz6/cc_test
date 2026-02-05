#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEX to Java Decompiler (Simplified)
Uses local dex2jar and finds available decompiler
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def find_dex2jar():
    """Find dex2jar installation"""
    possible_paths = [
        "tools/dex2jar",
        "tools/dex2jar-2.0",
        "dex2jar",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"[OK] Found dex2jar at: {path}")
            return path
    
    print("[Error] dex2jar not found")
    return None

def run_dex2jar(dex_file, dex2jar_dir):
    """Run dex2jar conversion"""
    print(f"[Converting] DEX to JAR...")
    
    # Try to find the script
    if sys.platform == "win32":
        script = os.path.join(dex2jar_dir, "d2j-dex2jar.bat")
    else:
        script = os.path.join(dex2jar_dir, "d2j-dex2jar.sh")
    
    if not os.path.exists(script):
        # Try with .cmd extension
        script_cmd = os.path.join(dex2jar_dir, "d2j-dex2jar.cmd")
        if os.path.exists(script_cmd):
            script = script_cmd
        else:
            print(f"[Error] Script not found: {script}")
            print(f"[Debug] Available files in {dex2jar_dir}:")
            for file in os.listdir(dex2jar_dir)[:10]:
                print(f"  - {file}")
            return None
    
    try:
        # Prepare output path
        output_jar = dex_file.replace(".dex", ".jar")
        
        # Run dex2jar
        cmd = [script, "-o", output_jar, dex_file]
        print(f"[Command] {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=dex2jar_dir)
        
        if result.returncode != 0 and result.returncode != 1:  # dex2jar returns 1 on success
            print(f"[Warning] Return code: {result.returncode}")
        
        print(f"[Output] {result.stdout[:500]}")
        
        # Check if JAR was created
        if os.path.exists(output_jar):
            size_mb = os.path.getsize(output_jar) / (1024*1024)
            print(f"[OK] JAR created: {output_jar} ({size_mb:.2f} MB)")
            return output_jar
        else:
            print(f"[Error] JAR not created")
            return None
    except Exception as e:
        print(f"[Error] Exception: {e}")
        return False

def create_summary_report():
    """Create a summary report"""
    print("\n" + "="*80)
    print("[DEX Analysis Summary]")
    print("="*80 + "\n")
    
    dex_file = "decompiled/extracted/classes.dex"
    
    if not os.path.exists(dex_file):
        print("[Error] DEX file not found")
        return
    
    size_mb = os.path.getsize(dex_file) / (1024*1024)
    print(f"[DEX File]")
    print(f"  Location: {dex_file}")
    print(f"  Size: {size_mb:.2f} MB")
    
    print(f"\n[Status]")
    print(f"  Conversion: Attempted using dex2jar")
    print(f"  Next step: Manual Java decompilation required")
    
    print(f"\n[Options to Continue]")
    print(f"\n1. Online Decompiler (QuickBytez):")
    print(f"   - Visit: https://www.quickbytez.com/showcase/android/apk-decompiler")
    print(f"   - Upload: {dex_file}")
    print(f"   - Get: Readable Java source code")
    
    print(f"\n2. Local Decompiler (Recommend):")
    print(f"   - Download: CFR from https://github.com/leibnitz27/cfr/releases")
    print(f"   - Command: java -jar cfr.jar {dex_file} --outputdir decompiled/java_src")
    
    print(f"\n3. Alternative Decompilers:")
    print(f"   - Procyon: https://github.com/mstrobel/procyon")
    print(f"   - Fernflower: https://github.com/facebookarchive/fernflower")
    print(f"   - Decompiler (JADX): https://github.com/skylot/jadx")
    
    print(f"\n[Recommended Tool]")
    print(f"  JADX GUI - Most user-friendly")
    print(f"  Download: https://github.com/skylot/jadx/releases")
    print(f"  Usage: Just drag-and-drop APK or DEX file")
    
    print(f"\n" + "="*80)

def main():
    """Main program"""
    print("="*80)
    print("[DEX to Java Decompiler - Simplified Edition]")
    print("="*80 + "\n")
    
    dex_file = "decompiled/extracted/classes.dex"
    
    if not os.path.exists(dex_file):
        print(f"[Error] DEX file not found: {dex_file}")
        return
    
    print(f"[Source] {dex_file}")
    print(f"[Size] {os.path.getsize(dex_file) / (1024*1024):.2f} MB\n")
    
    # Find dex2jar
    dex2jar_dir = find_dex2jar()
    if not dex2jar_dir:
        print("\n[Action Required]")
        print("  The dex2jar tool was not found properly.")
        print("  Please try running the decompilation with JADX instead.")
        create_summary_report()
        return
    
    # Run dex2jar
    output_jar = run_dex2jar(dex_file, dex2jar_dir)
    
    if not output_jar:
        print("\n[Note]")
        print("  dex2jar conversion needs CFR or another decompiler to complete.")
        create_summary_report()
        return
    
    print("\n[Next Steps]")
    print(f"  1. Download CFR: https://github.com/leibnitz27/cfr/releases")
    print(f"  2. Run: java -jar cfr.jar {output_jar} --outputdir decompiled/java_src")
    print(f"  3. Java source will be in: decompiled/java_src/")
    
    create_summary_report()

if __name__ == "__main__":
    main()
