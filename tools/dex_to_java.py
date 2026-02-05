#!/usr/bin/env python3
"""
DEX 反编译工具 - DEX -> JAR -> Java
"""

import os
import sys
import subprocess
import zipfile
import shutil
from pathlib import Path

def download_dex2jar():
    """下载 dex2jar 工具"""
    url = "https://github.com/ThexXTURBOXx/dex2jar/releases/download/v2.0/dex2jar-2.0.zip"
    output = "dex2jar-2.0.zip"
    
    if os.path.exists("dex2jar-2.0"):
        print("✅ dex2jar 已存在")
        return "dex2jar-2.0"
    
    print("📥 下载 dex2jar...")
    try:
        import urllib.request
        urllib.request.urlretrieve(url, output)
        
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall()
        
        os.remove(output)
        print("✅ dex2jar 已下载并解压")
        return "dex2jar-2.0"
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def decompile_with_cfr(jar_path, output_dir):
    """使用 CFR 反编译 JAR"""
    print("\n【步骤 3】使用 CFR 反编译 JAR 为 Java 源代码...")
    
    cfr_url = "https://www.benf.org/other/cfr/cfr.jar"
    cfr_jar = "cfr.jar"
    
    # 下载 CFR
    if not os.path.exists(cfr_jar):
        print(f"📥 下载 CFR...")
        try:
            import urllib.request
            urllib.request.urlretrieve(cfr_url, cfr_jar)
            print("✅ CFR 已下载")
        except Exception as e:
            print(f"⚠️  CFR 下载失败，尝试使用 javap: {e}")
            return False
    
    # 使用 CFR 反编译
    output_java = os.path.join(output_dir, "java_src")
    os.makedirs(output_java, exist_ok=True)
    
    try:
        cmd = [
            "java", "-jar", cfr_jar,
            jar_path,
            "--outputdir", output_java,
            "--codeformat", "structured"
        ]
        
        print(f"🔄 执行: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Java 源代码已反编译到: {output_java}")
            # 统计生成的 Java 文件
            java_files = list(Path(output_java).rglob("*.java"))
            print(f"📊 生成 {len(java_files)} 个 Java 文件")
            return True
        else:
            print(f"❌ CFR 反编译失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 反编译错误: {e}")
        return False

def convert_dex_to_jar(dex_path, output_jar, dex2jar_dir=None):
    """将 DEX 文件转换为 JAR"""
    print("\n【步骤 2】将 DEX 转换为 JAR...")
    
    if dex2jar_dir is None:
        dex2jar_dir = download_dex2jar()
    
    if dex2jar_dir is None:
        print("❌ dex2jar 工具不可用")
        return False
    
    # 查找 d2j-dex2jar 脚本
    if sys.platform == "win32":
        dex2jar_cmd = os.path.join(dex2jar_dir, "d2j-dex2jar.bat")
    else:
        dex2jar_cmd = os.path.join(dex2jar_dir, "d2j-dex2jar.sh")
    
    if not os.path.exists(dex2jar_cmd):
        print(f"❌ dex2jar 命令未找到: {dex2jar_cmd}")
        return False
    
    try:
        cmd = [dex2jar_cmd, "-f", "-o", output_jar, dex_path]
        print(f"🔄 执行: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_jar):
            file_size = os.path.getsize(output_jar) / 1024 / 1024
            print(f"✅ JAR 已生成: {output_jar} ({file_size:.2f} MB)")
            return True
        else:
            print(f"❌ DEX 转换失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return False

def analyze_dex_strings(dex_path):
    """分析 DEX 中的字符串"""
    print("\n【步骤 1】分析 DEX 文件...")
    
    # 使用已有的 dex_analysis.py 结果
    strings_file = "dex_strings.txt"
    
    if os.path.exists(strings_file):
        with open(strings_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        print(f"✅ DEX 字符串分析完成: {len(lines)} 个字符串")
        
        # 显示前 20 个字符串
        print("\n【示例字符串】")
        for line in lines[:20]:
            print(f"  - {line.strip()}")
        if len(lines) > 20:
            print(f"  ... 还有 {len(lines) - 20} 个字符串")
    else:
        print("⚠️  DEX 字符串文件不存在，请先运行 dex_analysis.py")

def main():
    print("=" * 80)
    print("【DEX 反编译工具 - DEX 转 Java】")
    print("=" * 80 + "\n")
    
    # 查找 DEX 文件
    dex_file = None
    if os.path.exists("decompiled/extracted/classes.dex"):
        dex_file = "decompiled/extracted/classes.dex"
    elif os.path.exists("base.apk"):
        # 从 APK 中提取 DEX
        print("【步骤 0】从 APK 中提取 DEX...")
        with zipfile.ZipFile("base.apk", 'r') as zip_ref:
            if 'classes.dex' in zip_ref.namelist():
                os.makedirs("decompiled/extracted", exist_ok=True)
                dex_file = zip_ref.extract('classes.dex', "decompiled/extracted")
                print(f"✅ DEX 已提取: {dex_file}")
    
    if not dex_file or not os.path.exists(dex_file):
        print("❌ 找不到 DEX 文件")
        sys.exit(1)
    
    # 分析 DEX
    analyze_dex_strings(dex_file)
    
    # 转换为 JAR
    output_dir = "decompiled"
    os.makedirs(output_dir, exist_ok=True)
    output_jar = os.path.join(output_dir, "classes.jar")
    
    if not convert_dex_to_jar(dex_file, output_jar):
        print("\n⚠️  dex2jar 工具不可用，尝试使用在线工具或手动反编译")
        print("推荐在线工具: http://www.javadecompilers.com/")
        return
    
    # 反编译为 Java
    if not os.path.exists(output_jar):
        print("❌ JAR 文件生成失败")
        return
    
    decompile_with_cfr(output_jar, output_dir)
    
    # 显示结果摘要
    print("\n" + "=" * 80)
    print("【反编译完成】")
    print("=" * 80)
    
    java_src_dir = os.path.join(output_dir, "java_src")
    if os.path.exists(java_src_dir):
        java_files = list(Path(java_src_dir).rglob("*.java"))
        print(f"\n✅ Java 源代码已生成到: {java_src_dir}")
        print(f"📊 共 {len(java_files)} 个 Java 文件")
        
        # 显示目录结构
        print("\n【源代码结构】")
        for root, dirs, files in os.walk(java_src_dir):
            level = root.replace(java_src_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # 只显示前 5 个文件
                print(f'{subindent}{file}')
            if len(files) > 5:
                print(f'{subindent}... 还有 {len(files) - 5} 个文件')
            if level > 2:  # 限制显示深度
                break
    else:
        print("⚠️  Java 源代码未生成，请检查 CFR 工具")
    
    print(f"\n【下一步】")
    print(f"1. 查看生成的 Java 文件: code {java_src_dir}")
    print(f"2. 搜索特定类: Get-ChildItem {java_src_dir} -Recurse -Filter '*Network*'")
    print(f"3. 分析关键代码: Select-String -Path '{java_src_dir}\\*.java' -Pattern 'API|key|secret'")

if __name__ == "__main__":
    main()
