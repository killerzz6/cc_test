#!/usr/bin/env python3
"""
Lua 脚本安全分析（.luac 文件）
"""
import os
import re

def scan_lua_files(base_path):
    """扫描并分析 Lua 文件"""
    lua_files = []
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if f.endswith('.luac') or f.endswith('.lua'):
                lua_files.append(os.path.join(root, f))
    return lua_files

def analyze_lua_file(lua_path):
    """分析单个 Lua 文件（查找可见的危险字符串）"""
    try:
        with open(lua_path, 'rb') as f:
            b = f.read()
    except:
        return None
    
    # 从二进制中提取可见字符串
    parts = re.findall(b'([ -~]{4,200})', b)
    strings = [p.decode('utf-8', errors='ignore') for p in parts]
    
    risks = {
        'network_calls': [],
        'file_operations': [],
        'dangerous_functions': [],
        'hardcoded_values': [],
        'debug_code': [],
    }
    
    for s in strings:
        # 网络调用
        if re.search(r'(http|socket|curl|request|download|upload)', s, re.I):
            risks['network_calls'].append(s)
        
        # 文件操作
        if re.search(r'(file|read|write|path|open|io\.)', s, re.I):
            risks['file_operations'].append(s)
        
        # 危险函数
        if re.search(r'(os\.execute|system|shell|exec|load|require)', s, re.I):
            risks['dangerous_functions'].append(s)
        
        # 硬编码值（密钥、token 等）
        if re.search(r'(key|token|secret|password|appid|uid|sid|sessionid)\s*=\s*["\'][\w\-]{8,}["\']', s, re.I):
            risks['hardcoded_values'].append(s)
        
        # 调试代码
        if 'print' in s.lower() or 'debug' in s.lower() or 'log' in s.lower():
            risks['debug_code'].append(s)
    
    return risks

print("=" * 80)
print("Lua 脚本安全分析")
print("=" * 80)

lua_base = 'apk_unzip/assets/base/src'
print(f"\n[*] 扫描 {lua_base}...")
lua_files = scan_lua_files(lua_base)
print(f"[+] 发现 {len(lua_files)} 个 Lua 文件")

all_risks = {
    'network_calls': [],
    'file_operations': [],
    'dangerous_functions': [],
    'hardcoded_values': [],
    'debug_code': [],
}

for lua_file in lua_files:
    risks = analyze_lua_file(lua_file)
    if risks:
        for cat, items in risks.items():
            all_risks[cat].extend(items)

print("\n【Lua 脚本风险】")
for category, items in all_risks.items():
    if items:
        unique_items = list(set(items))
        print(f"\n  {category}: {len(unique_items)} 个问题")
        for item in unique_items[:8]:
            print(f"    - {item[:80]}")
        if len(unique_items) > 8:
            print(f"    ... 还有 {len(unique_items) - 8} 个")

print(f"\n[*] Lua 文件列表（前30个）:")
for lua_file in lua_files[:30]:
    rel_path = lua_file.replace('apk_unzip/assets/base/src/', '')
    print(f"  - {rel_path}")
if len(lua_files) > 30:
    print(f"  ... 还有 {len(lua_files) - 30} 个文件")
