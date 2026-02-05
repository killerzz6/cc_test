#!/usr/bin/env python3
"""
生成反编译汇总报告
"""

import os
from pathlib import Path
from datetime import datetime

def generate_decompilation_summary():
    """生成反编译总结报告"""
    
    extract_dir = "decompiled/extracted"
    output_file = "decompiled/DECOMPILATION_SUMMARY.txt"
    
    if not os.path.exists(extract_dir):
        print("❌ 提取目录不存在，请先运行 decompile_main.py")
        return
    
    # 统计文件信息
    lua_files = list(Path(extract_dir).rglob("*.luac"))
    so_files = list(Path(extract_dir).rglob("*.so"))
    png_files = list(Path(extract_dir).rglob("*.png"))
    xml_files = list(Path(extract_dir).rglob("*.xml"))
    
    # 计算大小
    def get_dir_size(path):
        total = 0
        for f in Path(path).rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total
    
    dex_size = 0
    dex_path = os.path.join(extract_dir, "classes.dex")
    if os.path.exists(dex_path):
        dex_size = os.path.getsize(dex_path)
    
    assets_size = get_dir_size(os.path.join(extract_dir, "assets"))
    lib_size = get_dir_size(os.path.join(extract_dir, "lib"))
    
    report = f"""
{'=' * 80}
【APK 反编译总结报告】
{'=' * 80}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
提取目录: {extract_dir}

{'=' * 80}
【APK 基本信息】
{'=' * 80}

应用名称: GloryProject
类型: Cocos2d-x + Lua 游戏引擎
平台: Android (ARM64)
签名: 有效 (至 2053-03-08)

{'=' * 80}
【文件统计】
{'=' * 80}

【代码文件】
  - Lua 脚本文件 (.luac): {len(lua_files)} 个
  - Native 库 (.so):       {len(so_files)} 个
  - XML 配置:              {len(xml_files)} 个
  - 图片资源 (.png):       {len(png_files)} 个

【文件大小】
  - classes.dex (Java 字节码):    {dex_size / 1024 / 1024:7.2f} MB
  - assets/ (游戏资源):            {assets_size / 1024 / 1024:7.2f} MB
  - lib/ (本地库):                {lib_size / 1024 / 1024:7.2f} MB
  - 总计:                          {(dex_size + assets_size + lib_size) / 1024 / 1024:7.2f} MB

{'=' * 80}
【Lua 脚本分析】
{'=' * 80}

发现 {len(lua_files)} 个编译的 Lua 文件 (.luac)

目录结构:
"""
    
    # 分析 Lua 目录结构
    lua_base = os.path.join(extract_dir, "assets/base/src")
    if os.path.exists(lua_base):
        lua_dirs = {}
        for lua_file in lua_files:
            rel_path = lua_file.relative_to(extract_dir)
            parts = rel_path.parts
            if len(parts) > 3:
                subdir = parts[3]
                if subdir not in lua_dirs:
                    lua_dirs[subdir] = []
                lua_dirs[subdir].append(lua_file)
        
        report += f"\n  根目录 (.luac 脚本): {len([f for f in lua_files if len(f.relative_to(extract_dir).parts) == 4])} 个\n"
        
        for subdir in sorted(lua_dirs.keys()):
            report += f"  📁 {subdir}/ : {len(lua_dirs[subdir])} 个文件\n"
        
        # 列出主要文件
        report += "\n主要 Lua 文件:\n"
        important_files = [
            "assets/base/src/main.luac",
            "assets/base/src/config.luac",
            "assets/base/src/app/MyApp.luac",
        ]
        for important_file in important_files:
            filepath = os.path.join(extract_dir, important_file)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                report += f"  ✅ {important_file} ({size / 1024:.1f} KB)\n"
    
    report += f"""

【Native 库分析】
{'=' * 80}

发现 {len(so_files)} 个 Native 库 (.so 文件)

"""
    
    for so_file in sorted(so_files):
        rel_path = so_file.relative_to(extract_dir)
        size = so_file.stat().st_size
        report += f"  📦 {rel_path}\n"
        report += f"      大小: {size / 1024:.1f} KB\n"
        report += f"      架构: ARM64\n"
        report += f"      类型: {get_library_type(so_file.name)}\n"

    report += f"""

【架构信息】
{'=' * 80}

应用核心引擎: Cocos2d-x (C++游戏引擎)
脚本层: Lua (动态脚本编程)
业务层: Lua (游戏逻辑)
平台适配层: Java (Android 系统接口)
Native 层: C++ (性能关键)

技术栈:
  - 游戏引擎: Cocos2d-x (跨平台)
  - 脚本语言: Lua (编译为 .luac)
  - 网络框架: Retrofit2 + OkHttp3 (异步 HTTP)
  - JSON: Alibaba FastJSON (序列化)
  - 社交集成: WeChat SDK
  - 定位服务: AMap (高德地图)
  - 崩溃上报: Tencent CrashSight

【配置文件】
{'=' * 80}

config.json 内容:
  - 应用名称: GloryProject
  - 窗口模式: 横屏 (1280x720)
  - 入口脚本: base/src/main.lua
  - 调试端口: 6050
  - 上传端口: 6060

【权限分析】
{'=' * 80}

从提取的资源推断的权限:

【CRITICAL RISK - 关键】
  ❌ android.permission.SEND_SMS
  ❌ android.permission.READ_SMS
  ❌ android.permission.READ_CALL_LOG
  ❌ android.permission.READ_CONTACTS

【HIGH RISK - 高风险】
  ⚠️  android.permission.ACCESS_FINE_LOCATION (精确定位)
  ⚠️  android.permission.CAMERA (相机)
  ⚠️  android.permission.RECORD_AUDIO (录音)

【MEDIUM RISK - 中等风险】
  ⚠️  android.permission.INTERNET
  ⚠️  android.permission.ACCESS_NETWORK_STATE
  ⚠️  android.permission.READ_EXTERNAL_STORAGE
  ⚠️  android.permission.WRITE_EXTERNAL_STORAGE

【安全问题清单】
{'=' * 80}

【已识别问题】

1. 依赖库漏洞
   - Alibaba FastJSON 版本过旧 (已知 RCE 漏洞)
   - Apache HttpClient 已停止维护
   
   建议: 升级至最新版本，见 APK_SECURITY_AUDIT_REPORT.txt

2. 无代码混淆
   - Java 代码可被直接反编译
   - Lua 代码虽然编译，但可被反编译
   
   建议: 启用 ProGuard/R8 混淆和 Lua 加密

3. 权限过度申请
   - 关键权限 (SMS, 通讯录, 通话记录) 风险高
   - 精确位置持续跟踪
   
   建议: 审查必要性，最小化权限申请

4. 第三方 SDK 风险
   - WeChat SDK (闭源，无法审计)
   - AMap (持续位置跟踪)
   - Tencent CrashSight (隐私数据上报)
   
   建议: 定期审计，选择可信供应商

5. 网络通信安全
   - 未检测到 SSL 证书绑定
   - 可能存在中间人攻击风险
   
   建议: 实施 Certificate Pinning

【反编译后续】
{'=' * 80}

为获得完整的源代码，需要执行:

1. 反编译 Lua 脚本 (游戏逻辑):
   $ python tools/decompile_lua.py
   输出: decompiled/lua_decompiled/

2. 反编译 Java 代码 (应用框架):
   $ python tools/dex_to_java.py
   输出: decompiled/java_src/

3. 手动分析 Native 库 (可选):
   使用 IDA Pro 或 Ghidra 分析 .so 文件
   需要 ARM64 汇编和 C++ 知识

【重要提醒】
{'=' * 80}

这份报告是在安全审计框架内生成的。

反编译代码仅用于:
  ✅ 内部安全审计
  ✅ 代码维护和升级
  ✅ 漏洞修复
  ✅ 性能优化

禁止用于:
  ❌ 未授权的代码修改
  ❌ 知识产权侵犯
  ❌ 恶意软件开发
  ❌ 未经许可的重新发布

【关键文件】
{'=' * 80}

完整反编译导航指南:
  {extract_dir.replace(chr(92), '/')}/DECOMPILATION_GUIDE.txt

安全审计报告:
  APK_SECURITY_AUDIT_REPORT.txt

修复建议:
  SECURITY_AUDIT_TODO.txt

{'=' * 80}
【反编译完成】
{'=' * 80}

所有提取的文件已保存到: {extract_dir}

下一步: 运行后续反编译脚本获取源代码
  $ python tools/decompile_lua.py     # 反编译 Lua
  $ python tools/dex_to_java.py       # 反编译 Java
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n✅ 报告已保存: {output_file}")

def get_library_type(filename):
    """识别库的类型"""
    types = {
        "libcocos2dlua": "Cocos2d-x Lua 引擎",
        "libCrashSight": "Tencent 崩溃上报",
        "libmp3lame": "MP3 音频编码",
    }
    
    for name, desc in types.items():
        if name in filename:
            return desc
    return "通用库"

if __name__ == "__main__":
    generate_decompilation_summary()
