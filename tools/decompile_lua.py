#!/usr/bin/env python3
"""
Lua 反编译工具 - .luac 转 .lua
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

def download_unluac():
    """下载 unluac 反编译工具"""
    url = "https://sourceforge.net/projects/unluac/files/latest/download"
    output = "unluac.jar"
    
    if os.path.exists(output):
        print("✅ unluac.jar 已存在")
        return output
    
    print("📥 下载 unluac...")
    try:
        import urllib.request
        urllib.request.urlretrieve(url, output)
        print("✅ unluac 已下载")
        return output
    except Exception as e:
        print(f"⚠️  直接下载失败: {e}")
        print("📝 请从这里手动下载: https://sourceforge.net/projects/unluac/")
        return None

def decompile_lua_file(luac_path, output_path, unluac_jar):
    """反编译单个 Lua 文件"""
    try:
        cmd = ["java", "-jar", unluac_jar, "-o", output_path, luac_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return True
        else:
            print(f"⚠️  反编译失败 {luac_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return False

def extract_luac_from_apk():
    """从 APK 中提取 Lua 文件"""
    print("【步骤 1】从 APK 中提取 Lua 文件...")
    
    apk_path = "base.apk"
    lua_dir = "decompiled/lua_extracted"
    
    if not os.path.exists(apk_path):
        print(f"❌ APK 文件不存在: {apk_path}")
        return None
    
    os.makedirs(lua_dir, exist_ok=True)
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as zip_ref:
            # 查找所有 .luac 文件
            luac_files = [f for f in zip_ref.namelist() if f.endswith('.luac')]
            
            if not luac_files:
                print("❌ APK 中未找到 .luac 文件")
                return None
            
            print(f"✅ 发现 {len(luac_files)} 个 Lua 文件")
            
            # 提取所有 .luac 文件
            for luac_file in luac_files:
                try:
                    zip_ref.extract(luac_file, lua_dir)
                except Exception as e:
                    print(f"⚠️  提取失败: {luac_file}")
            
            print(f"✅ 已提取到: {lua_dir}")
            return lua_dir
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        return None

def decompile_lua_files(lua_source_dir):
    """反编译所有 Lua 文件"""
    print("\n【步骤 2】反编译 Lua 文件...")
    
    # 尝试下载 unluac
    unluac_jar = download_unluac()
    
    if not unluac_jar:
        print("\n⚠️  unluac 工具不可用，尝试备用方案...")
        print("【备用方案】")
        print("1. 使用在线反编译器:")
        print("   https://decompiler.slobodyan.com/")
        print("")
        print("2. 手动安装 unluac:")
        print("   $ java -jar unluac.jar script.luac > script.lua")
        print("")
        return False
    
    if not os.path.exists(lua_source_dir):
        print(f"❌ 源目录不存在: {lua_source_dir}")
        return False
    
    # 查找所有 .luac 文件
    luac_files = list(Path(lua_source_dir).rglob("*.luac"))
    
    if not luac_files:
        print(f"❌ 未找到 .luac 文件在: {lua_source_dir}")
        return False
    
    print(f"✅ 发现 {len(luac_files)} 个需要反编译的 Lua 文件")
    
    output_dir = "decompiled/lua_decompiled"
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    failed_count = 0
    
    for idx, luac_file in enumerate(luac_files, 1):
        # 生成输出文件路径
        rel_path = luac_file.relative_to(lua_source_dir)
        output_file = Path(output_dir) / rel_path.with_suffix('.lua')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[{idx}/{len(luac_files)}] 反编译: {rel_path}")
        
        if decompile_lua_file(str(luac_file), str(output_file), unluac_jar):
            success_count += 1
            print(f"        ✅ -> {output_file.name}")
        else:
            failed_count += 1
            print(f"        ❌ 失败")
    
    print(f"\n【反编译结果】")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {failed_count}")
    
    return output_dir if success_count > 0 else None

def analyze_decompiled_lua(lua_dir):
    """分析反编译的 Lua 代码"""
    print("\n【步骤 3】分析 Lua 代码......")
    
    if not os.path.exists(lua_dir):
        print(f"❌ 目录不存在: {lua_dir}")
        return
    
    lua_files = list(Path(lua_dir).rglob("*.lua"))
    
    if not lua_files:
        print("❌ 未找到 .lua 文件")
        return
    
    print(f"✅ 发现 {len(lua_files)} 个反编译的 Lua 文件\n")
    
    # 分析关键代码
    analysis_report = "decompiled/LUA_ANALYSIS_REPORT.txt"
    
    with open(analysis_report, 'w', encoding='utf-8') as report:
        report.write("=" * 80 + "\n")
        report.write("【Lua 代码分析报告】\n")
        report.write("=" * 80 + "\n\n")
        
        for lua_file in lua_files:
            rel_path = lua_file.relative_to(lua_dir)
            
            try:
                with open(lua_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 搜索关键代码
                findings = []
                
                # 网络请求
                if 'http' in content.lower() or 'socket' in content.lower():
                    findings.append("网络通信代码")
                
                # 关键字
                if 'require' in content:
                    findings.append("模块导入")
                
                if 'function' in content:
                    count = content.count('function')
                    findings.append(f"函数定义 ({count} 个)")
                
                # 敏感操作
                if 'os.' in content or 'io.' in content:
                    findings.append("操作系统/文件操作")
                
                if findings:
                    report.write(f"\n【{rel_path}】\n")
                    report.write(f"大小: {len(content)} 字节\n")
                    for finding in findings:
                        report.write(f"  - {finding}\n")
            except Exception as e:
                report.write(f"\n【{rel_path}】❌ 读取失败: {e}\n")
        
        report.write("\n" + "=" * 80 + "\n")
        report.write(f"【文件列表】\n")
        report.write("=" * 80 + "\n\n")
        
        for lua_file in lua_files:
            rel_path = lua_file.relative_to(lua_dir)
            size = lua_file.stat().st_size
            report.write(f"{rel_path} ({size} 字节)\n")
    
    print(f"✅ 分析报告已生成: {analysis_report}")

def main():
    print("=" * 80)
    print("【Lua 反编译工具 - .luac 转 .lua】")
    print("=" * 80 + "\n")
    
    # 步骤 1: 从 APK 提取 Lua 文件
    lua_source = extract_luac_from_apk()
    
    if not lua_source:
        print("\n❌ 无法提取 Lua 文件")
        sys.exit(1)
    
    # 步骤 2: 反编译 Lua 文件
    lua_decompiled = decompile_lua_files(lua_source)
    
    if lua_decompiled:
        # 步骤 3: 分析代码
        analyze_decompiled_lua(lua_decompiled)
        
        print("\n" + "=" * 80)
        print("【反编译完成】")
        print("=" * 80)
        print(f"\n✅ 反编译的 Lua 代码位置:")
        print(f"   {lua_decompiled}")
        print(f"\n【快速查看】")
        print(f"  Get-ChildItem '{lua_decompiled}' -Recurse -Filter '*.lua' | Select-Object -First 10")
        print(f"\n【代码分析】")
        print(f"  Select-String -Path '{lua_decompiled}\\*.lua' -Pattern 'http|require|function'")
    else:
        print("\n⚠️  反编译失败，请检查 unluac 工具")

if __name__ == "__main__":
    main()
