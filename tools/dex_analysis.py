#!/usr/bin/env python3
"""
APK DEX 反编译与安全分析脚本
"""
import re
import os
from collections import Counter

def extract_strings_from_dex(dex_path, max_strings=5000):
    """从 dex 文件提取字符串，寻找敏感信息"""
    with open(dex_path, 'rb') as f:
        b = f.read()
    
    # 提取 ULEB128 编码的字符串与二进制格式字符串
    strings = []
    
    # 寻找可见的 ASCII 字符串（4-300 字符）
    parts = re.findall(b'([ -~]{4,300})', b)
    strings = [p.decode('utf-8', errors='ignore') for p in parts]
    
    return strings[:max_strings]

def analyze_security_issues(strings):
    """分析安全问题"""
    issues = {
        'hardcoded_credentials': [],
        'api_keys': [],
        'suspicious_urls': [],
        'hardcoded_ips': [],
        'debugging_enabled': [],
        'crypto_weaknesses': [],
        'permissions_risky': [],
        'external_commands': [],
    }
    
    for s in strings:
        s_lower = s.lower()
        
        # 检查硬编码凭证
        if re.search(r'(password|passwd|pwd|secret|token|key)\s*=\s*["\'][\w\-]{4,}["\']', s, re.I):
            issues['hardcoded_credentials'].append(s)
        
        # 检查 API Key
        if re.search(r'(api[_-]?key|apikey|appkey|app[_-]?secret|access[_-]?key)\s*=\s*', s, re.I):
            issues['api_keys'].append(s)
        
        # 可疑 URL（可能是 C&C、数据收集、广告服务器）
        if re.search(r'https?://[a-zA-Z0-9\.\-]+\.(tk|ml|ga|cf|xyz|top|club|win|bid)', s, re.I):
            issues['suspicious_urls'].append(s)
        
        # 硬编码 IP
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', s):
            issues['hardcoded_ips'].append(s)
        
        # 调试模式标志
        if 'DEBUG' in s or 'debug' in s_lower or 'build.debug' in s_lower:
            issues['debugging_enabled'].append(s)
        
        # 弱加密或不安全的加密
        if re.search(r'(md5|sha1|des|rc4|ecb)', s, re.I):
            issues['crypto_weaknesses'].append(s)
        
        # 危险权限相关
        if re.search(r'(SEND_SMS|RECEIVE_SMS|READ_CONTACTS|READ_CALL_LOG|ACCESS_FINE_LOCATION|RECORD_AUDIO)', s):
            issues['permissions_risky'].append(s)
        
        # 外部命令执行
        if re.search(r'(exec|Runtime.getRuntime|ProcessBuilder|sh -c|/bin/)', s):
            issues['external_commands'].append(s)
    
    return issues

def extract_classes_and_methods(strings):
    """提取类名与方法名"""
    classes = set()
    for s in strings:
        if re.match(r'^[a-z][a-z0-9\.]*\.[A-Z][a-zA-Z0-9$]*$', s):
            classes.add(s)
    return sorted(list(classes))

print("=" * 80)
print("APK 安全审计 - DEX 分析")
print("=" * 80)

dex_path = 'apk_unzip/classes.dex'
print(f"\n[*] 从 {dex_path} 提取字符串...")
strings = extract_strings_from_dex(dex_path)
print(f"[+] 成功提取 {len(strings)} 个字符串")

print("\n[*] 分析安全问题...")
issues = analyze_security_issues(strings)

print("\n" + "=" * 80)
print("安全问题汇总")
print("=" * 80)

for category, items in issues.items():
    if items:
        print(f"\n【{category}】 - 发现 {len(items)} 个问题:")
        for i, item in enumerate(items[:10]):  # 显示前10个
            print(f"  {i+1}. {item[:100]}")
        if len(items) > 10:
            print(f"  ... 还有 {len(items) - 10} 个")

print("\n[*] 提取主要类名...")
classes = extract_classes_and_methods(strings)
print(f"[+] 发现 {len(classes)} 个主要类/包")
print("\n主要应用类（前50个）:")
for c in classes[:50]:
    if 'com.' in c or 'org.' in c or 'android.' in c:
        print(f"  - {c}")
