#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEX to Java Decompiler
Converts DEX bytecode to readable Java source code
"""

import os
import sys
import subprocess
import zipfile
import shutil
from pathlib import Path
import urllib.request

def download_tool(url, filename):
    """Download a tool from URL"""
    if os.path.exists(filename):
        print(f"[OK] {filename} already exists")
        return True
    
    print(f"[Download] Fetching {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"[OK] Downloaded {filename}")
        return True
    except Exception as e:
        print(f"[Error] Download failed: {e}")
        return False

def extract_zip(zip_file, extract_to="."):
    """Extract ZIP file"""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"[OK] Extracted {zip_file}")
        return True
    except Exception as e:
        print(f"[Error] Extract failed: {e}")
        return False

def setup_dex2jar():
    """Setup dex2jar tool"""
    print("[Step 1] Setting up dex2jar...")
    
    dex2jar_dir = "tools/dex2jar"
    if os.path.exists(dex2jar_dir):
        print(f"[OK] dex2jar already installed at {dex2jar_dir}")
        return dex2jar_dir
    
    # Download dex2jar
    url = "https://github.com/ThexXTURBOXx/dex2jar/releases/download/v2.0/dex2jar-2.0.zip"
    zip_file = "dex2jar-2.0.zip"
    
    if not download_tool(url, zip_file):
        print("[Error] Could not download dex2jar, trying alternative...")
        # Try mirror
        url = "https://sourceforge.net/projects/dex2jar/files/dex2jar-2.0.zip"
        if not download_tool(url, zip_file):
            print("[Error] All downloads failed")
            return None
    
    # Extract
    if not extract_zip(zip_file, "tools"):
        return None
    
    # Rename
    if os.path.exists("tools/dex2jar-2.0"):
        shutil.move("tools/dex2jar-2.0", dex2jar_dir)
    
    # Clean up
    if os.path.exists(zip_file):
        os.remove(zip_file)
    
    return dex2jar_dir

def setup_cfr():
    """Setup CFR Java decompiler"""
    print("[Step 2] Setting up CFR...")
    
    cfr_path = "tools/cfr.jar"
    if os.path.exists(cfr_path):
        print(f"[OK] CFR already installed at {cfr_path}")
        return cfr_path
    
    # Download CFR
    url = "https://www.benf.org/other/cfr/cfr.jar"
    if not download_tool(url, cfr_path):
        print("[Error] Could not download CFR")
        return None
    
    return cfr_path

def convert_dex_to_jar(dex_file, output_jar, dex2jar_dir):
    """Convert DEX to JAR using dex2jar"""
    print(f"[Step 3] Converting DEX to JAR...")
    
    # Determine the platform-specific script
    if sys.platform == "win32":
        script = os.path.join(dex2jar_dir, "d2j-dex2jar.bat")
    else:
        script = os.path.join(dex2jar_dir, "d2j-dex2jar.sh")
    
    if not os.path.exists(script):
        print(f"[Error] Script not found: {script}")
        return False
    
    try:
        # Run dex2jar
        cmd = [script, "-o", output_jar, dex_file]
        print(f"[Command] {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[Error] dex2jar failed:")
            print(result.stderr)
            return False
        
        if os.path.exists(output_jar):
            print(f"[OK] JAR created: {output_jar}")
            return True
        else:
            # Check for alternative output name
            alt_jar = dex_file.replace(".dex", ".jar")
            if os.path.exists(alt_jar):
                shutil.move(alt_jar, output_jar)
                print(f"[OK] JAR created: {output_jar}")
                return True
        
        return False
    except Exception as e:
        print(f"[Error] Exception: {e}")
        return False

def decompile_jar_to_java(jar_file, output_dir, cfr_path):
    """Decompile JAR to Java using CFR"""
    print(f"[Step 4] Decompiling JAR to Java...")
    
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Run CFR
        cmd = ["java", "-jar", cfr_path, jar_file, "--outputdir", output_dir]
        print(f"[Command] {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[Warning] CFR returned code {result.returncode}")
            print(result.stderr)
        
        # Check if files were created
        java_files = list(Path(output_dir).rglob("*.java"))
        if java_files:
            print(f"[OK] Generated {len(java_files)} Java files")
            return True
        else:
            print(f"[Warning] No Java files generated")
            return False
    except Exception as e:
        print(f"[Error] Exception: {e}")
        return False

def analyze_java_structure(java_dir):
    """Analyze the decompiled Java structure"""
    print(f"[Step 5] Analyzing Java structure...")
    
    java_files = list(Path(java_dir).rglob("*.java"))
    
    if not java_files:
        print("[Warning] No Java files found")
        return
    
    print(f"[OK] Found {len(java_files)} Java files")
    
    # Group by package
    packages = {}
    for java_file in java_files:
        # Extract package name from path
        relative_path = java_file.relative_to(java_dir)
        package_path = str(relative_path.parent).replace("\\", "/")
        
        if package_path not in packages:
            packages[package_path] = []
        packages[package_path].append(java_file.name)
    
    print("\n[Package Structure]")
    for package, files in sorted(packages.items())[:20]:
        print(f"  {package}/")
        for file in files[:3]:
            print(f"    - {file}")
        if len(files) > 3:
            print(f"    ... +{len(files)-3} more")
    
    if len(packages) > 20:
        print(f"  ... +{len(packages)-20} more packages")

def main():
    """Main program"""
    print("="*80)
    print("[DEX to Java Decompiler v2.0]")
    print("="*80)
    
    # Find DEX file
    dex_file = "decompiled/extracted/classes.dex"
    
    if not os.path.exists(dex_file):
        print(f"[Error] DEX file not found: {dex_file}")
        return
    
    print(f"\n[Source] {dex_file}")
    print(f"[Size] {os.path.getsize(dex_file) / (1024*1024):.2f} MB")
    
    # Setup tools
    dex2jar_dir = setup_dex2jar()
    if not dex2jar_dir:
        print("[Error] Failed to setup dex2jar")
        return
    
    cfr_path = setup_cfr()
    if not cfr_path:
        print("[Error] Failed to setup CFR")
        return
    
    # Create output paths
    output_jar = "decompiled/extracted/classes.jar"
    output_dir = "decompiled/java_src"
    
    # Convert DEX to JAR
    if not convert_dex_to_jar(dex_file, output_jar, dex2jar_dir):
        print("[Error] DEX to JAR conversion failed")
        return
    
    # Decompile JAR to Java
    if not decompile_jar_to_java(output_jar, output_dir, cfr_path):
        print("[Error] JAR decompilation failed")
        return
    
    # Analyze result
    analyze_java_structure(output_dir)
    
    print("\n" + "="*80)
    print("[Success] Decompilation completed!")
    print(f"[Output] {output_dir}")
    print("="*80)

if __name__ == "__main__":
    main()
