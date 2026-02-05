#!/usr/bin/env python3
"""
APK 反编译工具 - 主程序
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path

def extract_apk(apk_path, output_dir):
    """解压 APK 文件"""
    print("=" * 80)
    print("【APK 反编译 - 步骤 1: 解压 APK 文件】")
    print("=" * 80 + "\n")
    
    if not os.path.exists(apk_path):
        print(f"❌ APK 文件未找到: {apk_path}")
        return False
    
    extract_path = os.path.join(output_dir, "extracted")
    
    if os.path.exists(extract_path):
        print(f"⚠️  输出目录已存在: {extract_path}")
        response = input("是否覆盖? (y/n): ").strip().lower()
        if response != 'y':
            print("✅ 使用现有的解压文件")
            return extract_path
        shutil.rmtree(extract_path)
    
    os.makedirs(extract_path, exist_ok=True)
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        file_count = len(list(Path(extract_path).rglob('*')))
        print(f"✅ APK 已解压: {extract_path}")
        print(f"📊 共 {file_count} 个文件\n")
        return extract_path
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False

def list_apk_contents(extract_path):
    """列出 APK 内容"""
    print("=" * 80)
    print("【步骤 2: APK 内容分析】")
    print("=" * 80 + "\n")
    
    # 关键文件分析
    print("【关键文件】\n")
    
    key_files = [
        ("AndroidManifest.xml", "应用清单 (二进制格式)"),
        ("classes.dex", "Java 字节码 (需反编译)"),
        ("resources.arsc", "应用资源"),
    ]
    
    for filename, desc in key_files:
        filepath = os.path.join(extract_path, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_mb = size / 1024 / 1024
            print(f"  ✅ {filename:30s} ({size_mb:6.2f} MB) - {desc}")
        else:
            print(f"  ❌ {filename:30s} - 未找到")
    
    print("\n【目录结构】\n")
    
    # 统计各目录
    dirs = {
        "assets": "应用资源 (Lua 脚本、配置等)",
        "lib": "本地库 (Native .so 文件)",
        "res": "UI 资源",
        "META-INF": "签名证书",
    }
    
    for dirname, desc in dirs.items():
        dirpath = os.path.join(extract_path, dirname)
        if os.path.exists(dirpath):
            file_count = len(list(Path(dirpath).rglob('*')))
            print(f"  ✅ {dirname:15s} ({file_count:4d} 个文件) - {desc}")
        else:
            print(f"  ❌ {dirname:15s} - 未找到")
    
    print("\n【Lua 文件统计】\n")
    lua_files = list(Path(extract_path).rglob("*.luac"))
    print(f"  📊 发现 {len(lua_files)} 个 Lua 编译文件 (.luac)")
    
    if lua_files:
        print("\n  示例:")
        for lua_file in lua_files[:5]:
            rel_path = lua_file.relative_to(extract_path)
            print(f"    - {rel_path}")
        if len(lua_files) > 5:
            print(f"    ... 还有 {len(lua_files) - 5} 个文件")
    
    print("\n【Native 库统计】\n")
    so_files = list(Path(extract_path).rglob("*.so"))
    print(f"  📊 发现 {len(so_files)} 个 Native 库 (.so)")
    
    if so_files:
        print("\n  示例:")
        for so_file in so_files[:5]:
            rel_path = so_file.relative_to(extract_path)
            size = so_file.stat().st_size / 1024
            print(f"    - {rel_path} ({size:.1f} KB)")

def create_navigation_guide(extract_path):
    """创建导航指南"""
    print("\n" + "=" * 80)
    print("【步骤 3: 创建导航指南】")
    print("=" * 80 + "\n")
    
    output_dir = os.path.dirname(extract_path)
    guide_file = os.path.join(output_dir, "DECOMPILATION_GUIDE.txt")
    
    guide_content = f"""
================================================================================
【APK 反编译导航指南】
生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

【快速导航】

📁 APK 解压目录:
   {extract_path}

【关键目录】

1. Lua 脚本代码:
   {os.path.join(extract_path, 'assets/base/src')}
   
   包含所有游戏逻辑代码 (.luac 编译文件)
   需要使用 unluac 工具反编译
   
   命令:
   $ python tools/decompile_lua.py

2. 游戏配置文件:
   {os.path.join(extract_path, 'assets/base/config.json')}
   
   包含应用配置、API 端点、参数等
   可以直接用文本编辑器查看

3. Java 字节码:
   {os.path.join(extract_path, 'classes.dex')}
   
   包含所有 Java 胶水代码
   需要 dex2jar + CFR 反编译
   
   命令:
   $ python tools/dex_to_java.py

4. Native 库:
   {os.path.join(extract_path, 'lib')}
   
   ARM64 库: lib/arm64-v8a/
   ARM32 库: lib/armeabi-v7a/
   
   需要 IDA Pro 或 Ghidra 逆向

5. UI 资源:
   {os.path.join(extract_path, 'res')}
   {os.path.join(extract_path, 'assets/base/res/client.zip')}
   
   包含游戏 UI 和美术资源

【文件列表】

DEX 字节码:
  {os.path.join(extract_path, 'classes.dex')}

资源文件:
  {os.path.join(extract_path, 'resources.arsc')}

应用清单:
  {os.path.join(extract_path, 'AndroidManifest.xml')}

签名证书:
  {os.path.join(extract_path, 'META-INF')}

【反编译步骤】

步骤 1: 反编译 Lua 脚本 (游戏逻辑)
  $ python tools/decompile_lua.py
  
  输出: decompiled/lua_decompiled/

步骤 2: 反编译 Java 代码 (应用框架)
  $ python tools/dex_to_java.py
  
  输出: decompiled/java_src/

步骤 3: 分析 Native 库 (可选)
  使用 IDA Pro 或 Ghidra 分析:
    {os.path.join(extract_path, 'lib/arm64-v8a/libcocos2dlua.so')}
    {os.path.join(extract_path, 'lib/arm64-v8a/libCrashSight.so')}

【关键信息】

配置文件 (config.json):
  包含 API 端点、服务器地址、参数配置
  路径: {os.path.join(extract_path, 'assets/base/config.json')}

Lua MVC 架构:
  models/  - 数据模型
  views/   - UI 视图
  controllers/ - 业务逻辑
  
  位置: {os.path.join(extract_path, 'assets/base/src')}

第三方 SDK:
  - WeChat SDK (社交/支付)
  - AMap (地理位置)
  - Tencent CrashSight (崩溃上报)
  - Retrofit2/OkHttp3 (网络)
  - Alibaba FastJSON (JSON)

【安全检查清单】

反编译后需要检查:

□ 硬编码的 API 密钥和密码
  搜索: "api_key", "secret", "token", "password"

□ 敏感 URL 和端点
  搜索: "http://", "https://", ".com", "/api/"

□ 不安全的网络通信
  搜索: "HttpClient", "exec", "Runtime.getRuntime"

□ 数据泄露风险
  搜索: "SharedPreferences", "database", "log", "send"

□ 权限滥用
  搜索: "getDeviceId", "getIMEI", "getLocation", "readSMS"

□ 代码注入漏洞
  搜索: "eval", "loadDex", "reflection", "getDeclaredMethod"

【输出文件说明】

DECOMPILATION_REPORT.txt
  - 详细的反编译报告
  - 文件列表统计
  - 发现的关键信息

DECOMPILATION_GUIDE.txt (本文件)
  - 导航和快速参考

lua_decompiled/
  - 反编译后的 Lua 源代码
  - 游戏逻辑代码

java_src/
  - 反编译后的 Java 源代码
  - 应用框架代码

【推荐查看顺序】

1️⃣ config.json (快速获取应用信息)
   $ type {os.path.join(extract_path, 'assets/base/config.json')}

2️⃣ Lua 脚本 (理解游戏逻辑)
   $ Get-ChildItem '{os.path.join(extract_path, 'assets/base/src')}' -Recurse

3️⃣ Java 代码 (理解应用框架)
   $ ls decompiled/java_src/

4️⃣ AndroidManifest.xml (权限和组件)
   $ file {os.path.join(extract_path, 'AndroidManifest.xml')}

【常用命令】

查找特定字符串:
  $ Get-ChildItem decompiled -Recurse | Select-String "api_key|password|secret"

统计代码行数:
  $ (Get-ChildItem decompiled/lua_decompiled -Recurse -Filter '*.lua' | 
     Measure-Object -Property Length -Sum).Sum

查找网络调用:
  $ Select-String -Path 'decompiled/java_src/*.java' -Pattern 'http|socket|request'

【需要的工具】

✅ 已有:
  - Java JDK (反编译工具需要)
  - Python 3 (脚本执行)
  - PowerShell (命令行)

📥 需要下载:
  - unluac (Lua 反编译): https://sourceforge.net/projects/unluac/
  - dex2jar (DEX 转 JAR): https://github.com/ThexXTURBOXx/dex2jar
  - CFR (JAR 反编译): https://www.benf.org/other/cfr/cfr.jar

【下一步】

1. 运行 Lua 反编译:
   $ python tools/decompile_lua.py

2. 运行 Java 反编译:
   $ python tools/dex_to_java.py

3. 分析关键信息:
   $ code decompiled/

4. 生成安全审计报告:
   $ python tools/final_security_report.py

================================================================================
"""
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ 导航指南已生成: {guide_file}")
    return guide_file

def main():
    apk_file = "base.apk"
    output_dir = "decompiled"
    
    # 步骤 1: 解压 APK
    extract_path = extract_apk(apk_file, output_dir)
    if not extract_path:
        print("❌ 反编译失败")
        return False
    
    # 步骤 2: 分析内容
    list_apk_contents(extract_path)
    
    # 步骤 3: 创建导航指南
    guide_file = create_navigation_guide(extract_path)
    
    # 显示后续步骤
    print("\n" + "=" * 80)
    print("【反编译完成】")
    print("=" * 80 + "\n")
    
    print("📋 后续步骤:\n")
    print("1️⃣  反编译 Lua 脚本 (游戏逻辑代码):")
    print("   python tools/decompile_lua.py\n")
    
    print("2️⃣  反编译 Java 代码 (应用框架):")
    print("   python tools/dex_to_java.py\n")
    
    print("3️⃣  查看配置文件:")
    print(f"   type '{os.path.join(extract_path, 'assets/base/config.json')}'\n")
    
    print("4️⃣  查看导航指南:")
    print(f"   type '{guide_file}'\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  用户中止")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
