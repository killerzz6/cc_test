#!/usr/bin/env python3
"""
AndroidManifest 权限与组件分析
"""
import re
import struct

def parse_android_manifest_binary(manifest_path):
    """
    解析二进制 AndroidManifest.xml
    由于是二进制格式，我们提取关键的 ASCII 字符串
    """
    with open(manifest_path, 'rb') as f:
        b = f.read()
    
    # 提取所有可见字符串（通常在二进制中以 null 分隔）
    parts = re.findall(b'([ -~]{3,300})', b)
    strings = [p.decode('utf-8', errors='ignore') for p in parts]
    
    return strings

def analyze_manifest_permissions(strings):
    """分析权限与组件"""
    result = {
        'package_name': None,
        'permissions': [],
        'exported_activities': [],
        'exported_services': [],
        'exported_receivers': [],
        'providers': [],
        'target_sdk': None,
        'min_sdk': None,
        'debuggable': False,
    }
    
    for s in strings:
        # 包名
        if 'package' in s and '=' not in s and len(s) > 3 and '.' in s:
            if re.match(r'^[a-z][a-z0-9\.]*$', s) and s.count('.') >= 2:
                result['package_name'] = s
        
        # 权限
        if s.startswith('android.permission.'):
            result['permissions'].append(s)
        
        # exported 组件
        if 'exported' in s.lower():
            result['exported_activities'].append(s)
        
        # 调试标志
        if s.lower() == 'debuggable' or 'debuggable' in s.lower():
            result['debuggable'] = True
        
        # SDK 版本
        if 'targetSdkVersion' in s or 'targetSdk' in s:
            result['target_sdk'] = s
        if 'minSdkVersion' in s or 'minSdk' in s:
            result['min_sdk'] = s
    
    return result

def categorize_permissions(permissions):
    """按风险等级分类权限"""
    dangerous = {
        'DANGEROUS': [
            'READ_CONTACTS', 'WRITE_CONTACTS', 'READ_CALL_LOG', 'WRITE_CALL_LOG',
            'READ_CALENDAR', 'WRITE_CALENDAR', 'CAMERA', 'READ_SMS', 'SEND_SMS',
            'RECEIVE_SMS', 'READ_PHONE_STATE', 'CALL_PHONE', 'ACCESS_FINE_LOCATION',
            'ACCESS_COARSE_LOCATION', 'RECORD_AUDIO', 'READ_EXTERNAL_STORAGE',
            'WRITE_EXTERNAL_STORAGE', 'READ_CELL_BROADCASTS',
        ],
        'SENSITIVE': [
            'INTERNET', 'ACCESS_NETWORK_STATE', 'ACCESS_WIFI_STATE',
            'CHANGE_NETWORK_STATE', 'MODIFY_PHONE_STATE', 'GET_ACCOUNTS',
            'USE_CREDENTIALS', 'GET_PACKAGE_SIZE', 'DELETE_CACHE_FILES',
        ]
    }
    
    result = {
        'dangerous': [],
        'sensitive': [],
        'other': []
    }
    
    for perm in permissions:
        found = False
        for perm_type, perm_list in dangerous.items():
            if any(p in perm for p in perm_list):
                result[perm_type.lower()].append(perm)
                found = True
                break
        if not found:
            result['other'].append(perm)
    
    return result

print("=" * 80)
print("AndroidManifest 安全分析")
print("=" * 80)

manifest_path = 'apk_unzip/AndroidManifest.xml'
print(f"\n[*] 解析 {manifest_path}...")
strings = parse_android_manifest_binary(manifest_path)

manifest_info = analyze_manifest_permissions(strings)

print("\n【基本信息】")
print(f"  包名: {manifest_info['package_name'] or 'N/A'}")
print(f"  最小 SDK: {manifest_info['min_sdk'] or 'N/A'}")
print(f"  目标 SDK: {manifest_info['target_sdk'] or 'N/A'}")
print(f"  调试模式: {manifest_info['debuggable']}")

print(f"\n【权限分析】 - 共 {len(manifest_info['permissions'])} 个权限")
perms = categorize_permissions(manifest_info['permissions'])

if perms['dangerous']:
    print(f"\n  ⚠️  【危险权限】{len(perms['dangerous'])} 个:")
    for p in perms['dangerous']:
        print(f"     - {p}")

if perms['sensitive']:
    print(f"\n  ⚠️  【敏感权限】{len(perms['sensitive'])} 个:")
    for p in perms['sensitive'][:15]:
        print(f"     - {p}")
    if len(perms['sensitive']) > 15:
        print(f"     ... 还有 {len(perms['sensitive']) - 15} 个")

print(f"\n  ℹ️  【其他权限】{len(perms['other'])} 个")

# 扫描风险权限组合
print("\n【权限风险评估】")
risk_combos = {
    'SMS & 通讯录': ['SEND_SMS', 'READ_CONTACTS'],
    '位置 & 相机': ['ACCESS_FINE_LOCATION', 'CAMERA'],
    '录音 & 网络': ['RECORD_AUDIO', 'INTERNET'],
    '日志 & 短信': ['READ_CALL_LOG', 'READ_SMS'],
}

for combo_name, combo_perms in risk_combos.items():
    all_perms_str = ' '.join(manifest_info['permissions'])
    if all(p in all_perms_str for p in combo_perms):
        print(f"  ⚠️  检测到风险组合: {combo_name}")
