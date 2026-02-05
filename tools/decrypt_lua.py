#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义 Lua 加密格式解密工具
支持 RY_QP_2016 格式的 Lua 文件解密
"""

import os
import sys
import struct
from pathlib import Path

def analyze_lua_format(data):
    """分析 Lua 文件格式"""
    print("[File Information]")
    print(f"  Size: {len(data)} bytes")
    print(f"  Header (hex): {' '.join(f'{b:02x}' for b in data[:32])}")
    print(f"  Header (ASCII): {repr(data[:32])}")
    
    # 检查已知的格式签名
    if data[:10] == b'RY_QP_2016':
        print("  Format: RY_QP_2016 (Custom encrypted)")
        return "RY_QP_2016"
    elif data[:4] == b'\x1bLuaQ':
        print("  Format: Lua 5.1 bytecode")
        return "lua51"
    elif data[:4] == b'\x1bLuaT':
        print("  Format: Lua 5.3 bytecode")
        return "lua53"
    else:
        print("  Format: Unknown")
        return "unknown"

def decrypt_ry_qp_2016(data):
    """
    Attempt to decrypt RY_QP_2016 format
    This format uses simple XOR and shift encryption
    """
    print("[Decrypting RY_QP_2016]")
    
    # Skip header 10 bytes (RY_QP_2016)
    header = data[:10]
    encrypted = data[10:]
    
    print(f"  Header: {header}")
    print(f"  Encrypted data size: {len(encrypted)} bytes")
    
    # Try multiple decryption methods
    
    # Method 1: Simple XOR
    print("  Trying method 1: Simple XOR...")
    for xor_key in range(256):
        decrypted = bytes(b ^ xor_key for b in encrypted)
        if decrypted[:4] == b'\x1bLuaQ' or decrypted[:4] == b'\x1bLuaT':
            print(f"  [OK] Success! XOR key: {xor_key:02x}")
            return header + decrypted
    
    # Method 2: Cyclic XOR
    print("  Trying method 2: Cyclic XOR...")
    for xor_key in range(256):
        decrypted = bytes((b ^ ((xor_key + i) % 256)) for i, b in enumerate(encrypted))
        if decrypted[:4] == b'\x1bLuaQ' or decrypted[:4] == b'\x1bLuaT':
            print(f"  [OK] Success! Cyclic XOR key: {xor_key:02x}")
            return header + decrypted
    
    # Method 3: Byte reversal + XOR
    print("  Trying method 3: Byte reversal...")
    reversed_data = bytes(255 - b for b in encrypted)
    if reversed_data[:4] == b'\x1bLuaQ' or reversed_data[:4] == b'\x1bLuaT':
        print("  [OK] Success! Byte reversal")
        return header + reversed_data
    
    # Method 4: Check encoding characteristics
    print("  Trying method 4: Checking encoding features...")
    if all(b < 128 for b in encrypted):
        print("  Hint: Encrypted data looks like ASCII printable characters")
        try:
            import base64
            decoded = base64.b64decode(bytes(encrypted))
            if decoded[:4] == b'\x1bLuaQ' or decoded[:4] == b'\x1bLuaT':
                print("  [OK] Success! Base64 decoding")
                return header + decoded
        except:
            pass
    
    # Method 5: Check if it's simple DEFLATE compression
    print("  Trying method 5: Checking DEFLATE compression...")
    try:
        import zlib
        decompressed = zlib.decompress(encrypted)
        if decompressed[:4] == b'\x1bLuaQ' or decompressed[:4] == b'\x1bLuaT':
            print("  [OK] Success! DEFLATE decompression")
            return header + decompressed
    except:
        pass
    
    print("  [FAIL] All methods failed")
    return None

def process_lua_file(input_path):
    """Process a single Lua file"""
    print(f"\n{'='*60}")
    print(f"File: {input_path}")
    print(f"{'='*60}")
    
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # Analyze format
    format_type = analyze_lua_format(data)
    
    if format_type == "RY_QP_2016":
        # Try to decrypt
        decrypted = decrypt_ry_qp_2016(data)
        if decrypted:
            print("[Output]")
            output_path = input_path.replace('.luac', '_decrypted.lua')
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            print(f"  Saved to: {output_path}")
            return True
    elif format_type == "lua51" or format_type == "lua53":
        print("[Result] Already Lua bytecode, can decompile directly")
        output_path = input_path.replace('.luac', '.lua_bytecode')
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f"  Copied to: {output_path}")
        return True
    
    return False

def main():
    """Main program"""
    print("\n" + "="*60)
    print("[Lua Custom Encryption Decryption Tool v1.0]")
    print("="*60)
    
    # Find all .luac files
    base_path = Path("decompiled/lua_extracted/assets/base/src")
    
    if not base_path.exists():
        print(f"\n[ERROR] Path does not exist: {base_path}")
        print("Please run this script in the project root directory")
        return
    
    lua_files = list(base_path.rglob("*.luac"))
    print(f"\nFound {len(lua_files)} Lua files")
    
    if not lua_files:
        print("[ERROR] No .luac files found")
        return
    
    # Analyze the first file
    print("\n[Step 1] Analyzing first file...")
    first_file = lua_files[0]
    process_lua_file(str(first_file))
    
    # Process remaining files in batch
    if len(lua_files) > 1:
        print(f"\n[Step 2] Processing remaining {len(lua_files)-1} files...")
        success_count = 0
        for i, lua_file in enumerate(lua_files[1:], 2):
            if process_lua_file(str(lua_file)):
                success_count += 1
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(lua_files)}")
        
        print("\n[Statistics]")
        print(f"  Total files: {len(lua_files)}")
        print(f"  Successfully processed: {success_count + 1}")
        print(f"  Failed: {len(lua_files) - success_count - 1}")

if __name__ == "__main__":
    main()
