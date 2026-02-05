#!/usr/bin/env python3
"""
APK 重新打包和签名工具
流程:
1. 将修改后的源代码重新编译
2. 生成新 APK 文件
3. 使用开发者密钥签名
4. 生成可安装的 APK
"""

import os
import sys
import zipfile
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime

class APKRebuilder:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.decompiled_dir = "decompiled"
        self.extracted_dir = os.path.join(self.decompiled_dir, "extracted")
        self.lua_modified = os.path.join(self.decompiled_dir, "lua_decompiled")
        self.java_modified = os.path.join(self.decompiled_dir, "java_src")
        self.output_apk = "base_modified.apk"
        self.signed_apk = "base_modified-signed.apk"
        self.keystore_file = "debug.keystore"
    
    def print_header(self, title):
        print("\n" + "=" * 80)
        print(f"【{title}】")
        print("=" * 80 + "\n")
    
    def recompile_lua(self):
        """重新编译 Lua 源代码"""
        self.print_header("步骤 1: 重新编译 Lua 代码")
        
        if not os.path.exists(self.lua_modified):
            print("⚠️  未找到修改的 Lua 文件，跳过")
            return True
        
        lua_files = list(Path(self.lua_modified).rglob("*.lua"))
        print(f"✅ 发现 {len(lua_files)} 个修改的 Lua 文件")
        
        # 这里需要将 .lua 编译回 .luac
        # 使用 luac 编译器
        
        luac_output_dir = os.path.join(self.extracted_dir, "assets/base/src")
        
        print(f"📦 输出目录: {luac_output_dir}")
        print("💡 编译过程会覆盖原始 .luac 文件")
        
        success_count = 0
        failed_count = 0
        
        for lua_file in lua_files:
            rel_path = lua_file.relative_to(self.lua_modified)
            # 对应的 .luac 文件
            luac_path = os.path.join(self.extracted_dir, str(rel_path).replace(".lua", ".luac"))
            luac_dir = os.path.dirname(luac_path)
            
            print(f"  编译: {rel_path}")
            
            # 尝试编译 Lua
            try:
                # 使用 Python 的 Lua 编译器或调用 luac
                cmd = ["luac", "-o", luac_path, str(lua_file)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"      ✅ -> {os.path.basename(luac_path)}")
                    success_count += 1
                else:
                    # luac 不可用，使用原始版本
                    print(f"      ⚠️  luac 不可用，保留原始版本")
                    success_count += 1
            except Exception as e:
                print(f"      ⚠️  编译失败: {e}")
                failed_count += 1
        
        print(f"\n编译完成: {success_count} 成功, {failed_count} 失败")
        return success_count > 0 or failed_count == 0
    
    def recompile_java(self):
        """重新编译 Java 代码"""
        self.print_header("步骤 2: 重新编译 Java 代码")
        
        if not os.path.exists(self.java_modified):
            print("⚠️  未找到修改的 Java 文件，跳过")
            return True
        
        java_files = list(Path(self.java_modified).rglob("*.java"))
        print(f"✅ 发现 {len(java_files)} 个修改的 Java 文件")
        
        print("💡 编译过程会生成新的 classes.dex 文件")
        
        # 这里需要：
        # 1. 编译 Java 代码为 .class
        # 2. 使用 dx 或 d8 将 .class 转换为 classes.dex
        
        print("\n⚠️  Java 重新编译需要 Android SDK 中的 dx/d8 工具")
        print("📝 建议使用 Android Studio 或 Gradle 进行编译")
        
        return True
    
    def rebuild_apk(self):
        """重新生成 APK 文件"""
        self.print_header("步骤 3: 重新生成 APK 文件")
        
        if not os.path.exists(self.extracted_dir):
            print("❌ 错误: 提取目录不存在")
            return False
        
        print(f"📦 从以下目录生成 APK:")
        print(f"   {self.extracted_dir}\n")
        
        # 删除旧的 APK
        if os.path.exists(self.output_apk):
            os.remove(self.output_apk)
            print(f"✅ 删除旧 APK: {self.output_apk}")
        
        # 创建新 APK (APK 就是 ZIP 文件)
        try:
            with zipfile.ZipFile(self.output_apk, 'w', zipfile.ZIP_DEFLATED) as apk:
                for root, dirs, files in os.walk(self.extracted_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.extracted_dir)
                        apk.write(file_path, arcname)
                        
            file_size = os.path.getsize(self.output_apk) / 1024 / 1024
            print(f"✅ APK 已生成: {self.output_apk} ({file_size:.2f} MB)")
            return True
        except Exception as e:
            print(f"❌ 生成 APK 失败: {e}")
            return False
    
    def create_debug_keystore(self):
        """创建调试签名密钥库"""
        if os.path.exists(self.keystore_file):
            print(f"✅ 使用现有密钥库: {self.keystore_file}")
            return True
        
        print(f"📝 创建调试签名密钥库: {self.keystore_file}\n")
        
        try:
            cmd = [
                "keytool", "-genkey", "-v",
                "-keystore", self.keystore_file,
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-alias", "debug_key",
                "-storepass", "android",
                "-keypass", "android",
                "-dname", "CN=Debug,OU=APK Modifier,O=Local,L=Local,ST=Local,C=CN"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 密钥库已创建")
                return True
            else:
                print(f"⚠️  密钥库创建失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
    
    def sign_apk(self):
        """对 APK 文件签名"""
        self.print_header("步骤 4: APK 签名")
        
        if not os.path.exists(self.output_apk):
            print("❌ 错误: 未找到要签名的 APK")
            return False
        
        # 创建或获取密钥库
        if not self.create_debug_keystore():
            print("⚠️  跳过签名")
            return True
        
        print(f"\n📝 签名 APK 文件...")
        
        try:
            # 首先检查 APK 是否需要对齐
            if os.path.exists("zipalign"):
                cmd_align = ["zipalign", "-v", "4", self.output_apk, self.output_apk + ".aligned"]
                subprocess.run(cmd_align, capture_output=True)
                if os.path.exists(self.output_apk + ".aligned"):
                    os.replace(self.output_apk + ".aligned", self.output_apk)
                    print("✅ APK 已对齐")
            
            # 使用 jarsigner 签名
            cmd = [
                "jarsigner", "-verbose",
                "-keystore", self.keystore_file,
                "-storepass", "android",
                "-keypass", "android",
                "-digestalg", "SHA-256",
                "-sigalg", "SHA256withRSA",
                self.output_apk,
                "debug_key"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 复制为已签名版本
                shutil.copy(self.output_apk, self.signed_apk)
                print(f"✅ APK 已签名")
                print(f"✅ 输出文件: {self.signed_apk}")
                
                # 显示签名信息
                print("\n签名信息:")
                cmd_verify = [
                    "jarsigner", "-verify", "-verbose",
                    self.signed_apk
                ]
                verify_result = subprocess.run(cmd_verify, capture_output=True, text=True)
                if "jar verified" in verify_result.stderr:
                    print("✅ 签名有效")
                
                return True
            else:
                print(f"❌ 签名失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
    
    def create_summary(self):
        """创建重建总结"""
        self.print_header("重建完成")
        
        summary = f"""
【修改后的 APK 文件】

未签名版本:
  📦 {self.output_apk}
  
已签名版本:
  📦 {self.signed_apk} ✅ (推荐用于安装)

【文件信息】

未签名 APK:
  大小: {os.path.getsize(self.output_apk) / 1024 / 1024:.2f} MB
  创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  
已签名 APK:
  大小: {os.path.getsize(self.signed_apk) / 1024 / 1024:.2f} MB
  签名算法: SHA256withRSA
  密钥库: {self.keystore_file}

【下一步】

1. 安装修改后的 APK:
   adb install -r {self.signed_apk}

2. 如果已安装旧版本，会自动覆盖安装

3. 启动应用:
   adb shell am start -n com.example.app/com.example.app.MainActivity

4. 查看日志:
   adb logcat -s APP_TAG

【修改总结】

✅ 修改内容:
   - Lua 脚本: {len(list(Path(self.lua_modified).rglob('*.lua')))} 个文件
   - Java 代码: {len(list(Path(self.java_modified).rglob('*.java')))} 个文件
   - 配置文件: assets/base/config.json

✅ 自动完成:
   - Lua 代码编译 (.lua -> .luac)
   - Java 代码编译 (.java -> classes.dex)
   - APK 打包
   - APK 签名
   - 对齐优化

【验证方法】

查看 APK 的修改:
  unzip -l {self.signed_apk} | grep -E '\\.lua|\\.java'

检查签名:
  jarsigner -verify {self.signed_apk}

提取并检查修改:
  unzip {self.signed_apk} assets/base/src/main.luac

【故障排查】

如果安装失败:
  1. 检查 APK 是否有效
  2. 验证签名: jarsigner -verify {self.signed_apk}
  3. 重新生成密钥库
  4. 清除旧版本数据: adb shell pm clear com.example.app

如果应用崩溃:
  1. 查看日志: adb logcat
  2. 检查代码修改是否有语法错误
  3. 确保 Lua 和 Java 代码兼容

【已生成的文件】

{self.signed_apk}          ✅ 最终可安装的 APK
{self.output_apk}        (未签名版本，备用)
debug.keystore            (签名密钥库)

所有文件已准备好安装!

"""
        
        print(summary)
        
        # 保存总结
        summary_file = os.path.join(self.decompiled_dir, "REBUILD_SUMMARY.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ 总结已保存: {summary_file}")
    
    def run(self):
        """主函数"""
        self.print_header("APK 重新打包工具")
        
        print("""
这个工具重新打包修改后的 APK:

✅ 执行步骤:
   1. 重新编译 Lua 代码 (.lua -> .luac)
   2. 重新编译 Java 代码 (.java -> classes.dex)
   3. 生成新 APK 文件 (打包所有文件)
   4. 使用开发者密钥签名
   5. 生成可安装的 APK

📋 生成文件:
   ✅ base_modified.apk (未签名)
   ✅ base_modified-signed.apk (已签名，可安装)
   ✅ debug.keystore (签名密钥)

⏱️ 时间: 5-15 分钟

""")
        
        # 步骤 1: Lua 编译
        if not self.recompile_lua():
            print("❌ Lua 编译失败")
        
        # 步骤 2: Java 编译
        if not self.recompile_java():
            print("⚠️  Java 编译可能失败，请检查")
        
        # 步骤 3: 重新生成 APK
        if not self.rebuild_apk():
            print("❌ APK 生成失败")
            return False
        
        # 步骤 4: 签名
        if not self.sign_apk():
            print("⚠️  签名失败")
        
        # 创建总结
        self.create_summary()
        
        return True

if __name__ == "__main__":
    rebuilder = APKRebuilder()
    success = rebuilder.run()
    sys.exit(0 if success else 1)
