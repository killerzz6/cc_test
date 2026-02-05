#!/usr/bin/env python3
"""
APK 代码修改和重打包工具
包含:
1. 反编译 Lua 和 Java 源代码
2. 修改源代码
3. 重新编译
4. 重新签名
5. 生成新 APK
"""

import os
import sys
import zipfile
import shutil
import subprocess
from pathlib import Path
import json

class APKModifier:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.apk_file = "base.apk"
        self.decompiled_dir = "decompiled"
        self.extracted_dir = os.path.join(self.decompiled_dir, "extracted")
        self.modified_apk = "base_modified.apk"
        
    def print_header(self, title):
        print("\n" + "=" * 80)
        print(f"【{title}】")
        print("=" * 80 + "\n")
    
    def decompile_lua_files(self):
        """反编译 Lua 文件"""
        self.print_header("步骤 1: 反编译 Lua 脚本")
        
        lua_src = os.path.join(self.extracted_dir, "assets/base/src")
        lua_out = os.path.join(self.decompiled_dir, "lua_decompiled")
        
        if not os.path.exists(lua_src):
            print("❌ Lua 源目录不存在")
            return False
        
        luac_files = list(Path(lua_src).rglob("*.luac"))
        print(f"✅ 发现 {len(luac_files)} 个 Lua 编译文件")
        
        os.makedirs(lua_out, exist_ok=True)
        
        # 这里会在后续步骤中实现具体的反编译
        print(f"💡 提示: 需要 unluac 工具反编译")
        print(f"   输出目录: {lua_out}")
        print(f"   命令: python tools/decompile_lua.py")
        
        return True
    
    def decompile_java_files(self):
        """反编译 Java 文件"""
        self.print_header("步骤 2: 反编译 Java 代码")
        
        dex_file = os.path.join(self.extracted_dir, "classes.dex")
        java_out = os.path.join(self.decompiled_dir, "java_src")
        
        if not os.path.exists(dex_file):
            print("❌ DEX 文件不存在")
            return False
        
        dex_size = os.path.getsize(dex_file) / 1024 / 1024
        print(f"✅ DEX 文件: {dex_size:.2f} MB")
        
        os.makedirs(java_out, exist_ok=True)
        
        print(f"💡 提示: 需要 dex2jar + CFR 工具反编译")
        print(f"   输出目录: {java_out}")
        print(f"   命令: python tools/dex_to_java.py")
        
        return True
    
    def create_modification_guide(self):
        """创建代码修改指南"""
        self.print_header("步骤 3: 代码修改指南")
        
        guide = """
【可修改的文件位置】

1️⃣ Lua 游戏逻辑代码 (反编译后)
   位置: decompiled/lua_decompiled/assets/base/src/
   文件类型: .lua (文本文件，可直接编辑)
   
   关键文件:
   - main.lua          主程序入口
   - app/MyApp.lua     应用框架
   - app/MainScene.lua 主场景逻辑
   - app/GameRule*.lua 游戏规则
   - network/*.lua     网络通信
   
   编辑工具: 任何文本编辑器 (VS Code, Notepad++, Sublime 等)

2️⃣ Java 应用代码 (反编译后)
   位置: decompiled/java_src/
   文件类型: .java (文本文件，可直接编辑)
   
   关键目录:
   - com/example/app/         应用框架
   - com/example/network/     网络通信
   - com/example/util/        工具函数
   
   编辑工具: VS Code + Java 插件或 Android Studio

3️⃣ 配置文件 (已提取)
   位置: decompiled/extracted/assets/base/config.json
   文件类型: JSON (可直接编辑)
   
   可修改内容:
   - API 端点
   - 调试参数
   - 窗口尺寸
   - 资源配置

【修改示例】

修改 Lua 游戏规则:
  1. 打开: decompiled/lua_decompiled/app/GameRule.lua
  2. 编辑逻辑代码
  3. 保存文件
  4. 重新打包 (自动编译)

修改 Java 网络端点:
  1. 打开: decompiled/java_src/com/example/network/*.java
  2. 修改 API URL、超时时间等
  3. 保存文件
  4. 重新打包 (自动编译)

修改配置参数:
  1. 打开: decompiled/extracted/assets/base/config.json
  2. 编辑 JSON 内容
  3. 保存文件
  4. 重新打包

【修改后的步骤】

1. 修改完所有需要的代码
2. 运行: python tools/rebuild_apk.py
3. 自动完成:
   ✅ Lua 代码重新编译 (.lua -> .luac)
   ✅ Java 代码重新编译 (.java -> classes.dex)
   ✅ 生成新 APK 文件
   ✅ 使用开发者密钥重新签名
   ✅ 生成: base_modified.apk (修改后的版本)

4. 安装修改后的 APK:
   adb install -r base_modified.apk

【重要提醒】

✅ 可以修改的:
   - Lua 游戏逻辑代码
   - Java 胶水代码
   - 配置文件
   - 资源文件 (图片、文本)

❌ 不能直接修改的:
   - Native 库 (.so 文件) - 需要 IDA 反汇编
   - AndroidManifest.xml - 需要二进制工具
   - 已签名的 APK - 需要重新打包

【工具支持】

我们提供自动化工具:
  ✅ tools/decompile_lua.py      反编译 Lua
  ✅ tools/dex_to_java.py        反编译 Java
  ✅ tools/rebuild_apk.py        重新打包 APK
  ✅ tools/sign_apk.py           签名 APK

"""
        
        print(guide)
        
        # 保存到文件
        guide_file = os.path.join(self.decompiled_dir, "MODIFICATION_GUIDE.txt")
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"✅ 修改指南已保存: {guide_file}")
        return guide_file
    
    def show_next_steps(self):
        """显示后续步骤"""
        self.print_header("后续步骤")
        
        steps = """
【步骤 1】反编译 Lua 和 Java 源代码

  反编译 Lua (游戏逻辑):
    python tools/decompile_lua.py
    输出: decompiled/lua_decompiled/
  
  反编译 Java (应用框架):
    python tools/dex_to_java.py
    输出: decompiled/java_src/

【步骤 2】编辑源代码

  使用任何文本编辑器打开:
  
  Lua 文件 (.lua):
    code decompiled/lua_decompiled/app/MyApp.lua
    code decompiled/lua_decompiled/app/MainScene.lua
  
  Java 文件 (.java):
    code decompiled/java_src/
  
  配置文件:
    code decompiled/extracted/assets/base/config.json

【步骤 3】修改完毕后重新打包

  自动重新打包和签名:
    python tools/rebuild_apk.py
  
  输出:
    ✅ base_modified.apk (修改后的版本)
    ✅ base_modified-signed.apk (已签名)

【步骤 4】安装修改后的 APK

  使用 ADB 安装:
    adb install -r base_modified-signed.apk
  
  或者双击手机上安装

【快速命令参考】

查看反编译的 Lua 文件:
  Get-ChildItem decompiled/lua_decompiled -Recurse -Filter *.lua

查看反编译的 Java 文件:
  Get-ChildItem decompiled/java_src -Recurse -Filter *.java

搜索特定代码:
  Select-String -Path 'decompiled/lua_decompiled/**/*.lua' -Pattern '关键字'

统计修改的文件:
  Get-ChildItem decompiled -Recurse -Filter *.lua | Measure-Object | Select-Object Count

【重要文件】

创建的脚本:
  ✅ tools/decompile_lua.py      - 反编译 Lua
  ✅ tools/dex_to_java.py        - 反编译 Java  
  ✅ tools/rebuild_apk.py        - 重新打包 APK
  ✅ tools/sign_apk.py           - 签名 APK

输出目录:
  ✅ decompiled/lua_decompiled/  - 反编译的 Lua 源代码
  ✅ decompiled/java_src/        - 反编译的 Java 源代码
  ✅ base_modified.apk           - 修改后的 APK
  ✅ base_modified-signed.apk    - 已签名的 APK

【修改权限】

根据安全审计，建议修改的项目:

1️⃣ 权限 (CRITICAL - 立即修改)
   文件: AndroidManifest.xml
   移除权限: SEND_SMS, READ_SMS, READ_CALL_LOG, READ_CONTACTS

2️⃣ 依赖库 (HIGH - 高优先级)
   文件: Java 代码中的库导入
   更新: FastJSON 1.2.70 -> 1.2.83

3️⃣ 网络安全 (MEDIUM)
   文件: Java 网络代码
   添加: SSL Certificate Pinning

4️⃣ 代码混淆 (MEDIUM)
   文件: build.gradle
   启用: ProGuard/R8 混淆

【支持的修改】

✅ 游戏逻辑代码 (Lua)
   - 修改游戏规则
   - 更改难度参数
   - 调整 UI 逻辑
   - 改变游戏流程

✅ 应用框架代码 (Java)
   - 更新 API 端点
   - 改变网络超时
   - 修改权限使用
   - 添加调试功能

✅ 配置文件
   - 改变应用参数
   - 更新端点配置
   - 调整窗口尺寸
   - 改变调试端口

✅ 资源文件
   - 替换图片
   - 修改文本
   - 更新菜单
   - 改变颜色

【需要额外工具的修改】

❌ Native 库 (.so 文件)
   需要: IDA Pro / Ghidra (汇编级别逆向)

❌ AndroidManifest.xml
   需要: 二进制清单编辑工具

❌ resources.arsc
   需要: ARSC 编辑工具

"""
        
        print(steps)
    
    def run(self):
        """主函数"""
        self.print_header("APK 代码修改工具")
        
        print("""
这个工具帮助你修改 APK 中的代码:

✅ 支持修改:
   - Lua 游戏逻辑代码 (78 个文件)
   - Java 应用框架代码
   - 配置文件和资源

📋 流程:
   1. 反编译 Lua/Java 源代码 (生成可编辑的文件)
   2. 用任何编辑器修改代码
   3. 自动重新打包为 APK
   4. 自动重新签名
   5. 生成新的 APK 文件

⏱️ 时间: 约 5-10 分钟

⚠️ 要求:
   - Java JDK
   - Python 3.7+
   - 工具会自动下载 unluac, dex2jar, CFR 等

""")
        
        # 检查基本条件
        if not os.path.exists(self.apk_file):
            print(f"❌ 错误: {self.apk_file} 不存在")
            return False
        
        if not os.path.exists(self.extracted_dir):
            print(f"❌ 错误: APK 未提取，请先运行 decompile_main.py")
            return False
        
        print("✅ 前置条件检查通过\n")
        
        # 步骤 1: Lua 反编译
        self.decompile_lua_files()
        
        # 步骤 2: Java 反编译
        self.decompile_java_files()
        
        # 步骤 3: 创建修改指南
        self.create_modification_guide()
        
        # 显示后续步骤
        self.show_next_steps()
        
        self.print_header("准备工作完成")
        print("""
现在可以进行以下操作:

【立即可做】
1. 反编译源代码:
   $ python tools/decompile_lua.py
   $ python tools/dex_to_java.py

2. 查看修改指南:
   $ cat decompiled/MODIFICATION_GUIDE.txt

3. 编辑代码:
   $ code decompiled/lua_decompiled/
   $ code decompiled/java_src/

【修改完毕后】
1. 重新打包:
   $ python tools/rebuild_apk.py

2. 生成结果:
   ✅ base_modified.apk (未签名)
   ✅ base_modified-signed.apk (已签名)

【安装新 APK】
$ adb install -r base_modified-signed.apk

""")

if __name__ == "__main__":
    modifier = APKModifier()
    modifier.run()
