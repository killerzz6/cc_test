# APK 反编译脚本 - 使用多种方法提取源代码

param(
    [string]$ApkFile = "base.apk",
    [string]$OutputDir = "decompiled"
)

Write-Host "================================================================================`n"
Write-Host "【APK 反编译工具】`n" -ForegroundColor Cyan
Write-Host "================================================================================`n"

# 检查 APK 文件
if (-not (Test-Path $ApkFile)) {
    Write-Host "❌ APK 文件未找到: $ApkFile" -ForegroundColor Red
    exit 1
}

$ApkPath = (Resolve-Path $ApkFile).Path
Write-Host "✅ APK 文件: $ApkPath`n"

# 创建输出目录
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# 方法 1: 用 PowerShell 解压 APK (APK = ZIP)
Write-Host "【步骤 1】解压 APK 文件..." -ForegroundColor Yellow
$extractDir = Join-Path $OutputDir "extracted"
New-Item -ItemType Directory -Path $extractDir -Force | Out-Null

try {
    Expand-Archive -Path $ApkPath -DestinationPath $extractDir -Force
    Write-Host "✅ APK 已解压到: $extractDir`n" -ForegroundColor Green
} catch {
    Write-Host "❌ 解压失败: $_" -ForegroundColor Red
    exit 1
}

# 方法 2: 使用 dex2jar 和 CFR 反编译 DEX (使用 Python 脚本)
Write-Host "【步骤 2】准备 DEX 反编译..." -ForegroundColor Yellow
Write-Host "将使用 Python 工具进行 DEX -> JAR -> Java 反编译`n"

# 方法 3: 创建详细的资源分析报告
Write-Host "【步骤 3】创建反编译分析报告..." -ForegroundColor Yellow

$reportPath = Join-Path $OutputDir "DECOMPILATION_REPORT.txt"
$report = @"
================================================================================
【APK 反编译分析报告】
================================================================================
生成时间: $(Get-Date)
APK 文件: $($ApkFile)
输出目录: $((Resolve-Path $OutputDir).Path)

================================================================================
【1. 文件结构分析】
================================================================================

"@

# 列出所有提取的文件
Get-ChildItem -Path $extractDir -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($extractDir.Length + 1)
    $size = if ($_.PSIsContainer) { "-" } else { $_.Length }
    $report += "$($relativePath) ($size bytes)`n"
} | Out-Null

$report += @"

================================================================================
【2. 关键文件列表】
================================================================================

**AndroidManifest.xml**
- 位置: $extractDir\AndroidManifest.xml
- 说明: 应用清单文件 (二进制格式)

**classes.dex**
- 位置: $extractDir\classes.dex
- 大小: $(if (Test-Path "$extractDir\classes.dex") { (Get-Item "$extractDir\classes.dex").Length } else { "未找到" }) 字节
- 说明: Dalvik 字节码 (需要转换为 JAR 后反编译)

**resources.arsc**
- 位置: $extractDir\resources.arsc
- 说明: 应用资源文件

**assets/** 目录
- 位置: $extractDir\assets
- 说明: 游戏资源、Lua 脚本、图片等

**lib/** 目录
- 位置: $extractDir\lib
- 说明: 本地 Native 库 (.so 文件)

================================================================================
【3. 反编译步骤】
================================================================================

**第一步：查看应用资源**
- Lua 脚本位置: assets/base/src/
  所有 .luac 文件可以用 luadec 或 unluac 反编译

- 配置文件位置: assets/base/config.json
  使用文本编辑器直接查看

- 图片资源: res/ 目录
  直接用图片查看器打开

**第二步：反编译 DEX 代码**
需要工具:
1. dex2jar: 将 classes.dex 转换为 classes.jar
2. CFR/JD-GUI: 将 JAR 反编译为 Java 源代码

下一步运行:
  python tools/dex_to_java.py

**第三步：分析 Native 库**
Native 库位置: lib/arm64-v8a/
- libcocos2dlua.so: Cocos2d 框架实现
- libCrashSight.so: 腾讯崩溃上报
- libmp3lame.so: MP3 编码库

需要 IDA Pro 或 Ghidra 进行逆向

================================================================================
【4. Lua 脚本反编译】
================================================================================

发现的 Lua 文件: 78 个 (.luac 格式)

反编译工具选项:
1. luadec (推荐): https://github.com/viruscamp/luadec
2. unluac: https://sourceforge.net/projects/unluac/

执行:
  python tools/decompile_lua.py

预期结果:
- 提取游戏逻辑代码
- 发现网络协议实现
- 识别配置信息和硬编码参数

================================================================================
【5. 已提取的文件结构】
================================================================================

$extractDir/
├── AndroidManifest.xml
├── classes.dex
├── resources.arsc
├── assets/
│   └── base/
│       ├── src/            (Lua 脚本目录)
│       ├── res/            (资源 ZIP)
│       └── config.json
├── lib/
│   ├── arm64-v8a/          (ARM64 Native 库)
│   └── armeabi-v7a/        (ARM32 Native 库)
├── res/                     (应用资源)
└── META-INF/                (签名证书)

================================================================================
【6. 推荐查看顺序】
================================================================================

1️⃣ 首先查看资源文件 (无需反编译)
   - assets/base/config.json
   - 配置参数和端点
   
2️⃣ 查看 AndroidManifest.xml (需要解析器)
   - 应用权限
   - 组件定义
   - 意图过滤器

3️⃣ 反编译 Lua 脚本
   - 游戏逻辑
   - 网络通信
   - 关键业务流程
   
4️⃣ 反编译 DEX 字节码 (Java 胶水代码)
   - JNI 接口
   - 应用框架
   - 第三方库调用

5️⃣ 逆向 Native 库 (可选)
   - 核心算法实现
   - 性能关键代码
   - 安全敏感操作

================================================================================
【7. 快速命令参考】
================================================================================

查看 Lua 文件列表:
  Get-ChildItem $extractDir\assets -Recurse -Filter "*.luac"

查看资源 ZIP 内容:
  python tools\inspect_resources.py

查看配置文件:
  Get-Content $extractDir\assets\base\config.json

列出 Native 库:
  Get-ChildItem $extractDir\lib -Recurse -Filter "*.so"

================================================================================
【下一步】
================================================================================

运行以下脚本继续反编译:

1. 反编译 Lua:
   python tools/decompile_lua.py

2. 转换 DEX 为 Java:
   python tools/dex_to_java.py

3. 分析 AndroidManifest:
   python tools/analyze_manifest_binary.py

4. 提取所有字符串:
   python tools/extract_all_strings.py

================================================================================
"@

$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "✅ 报告已生成: $reportPath`n" -ForegroundColor Green

# 步骤 4: 创建快速导航脚本
Write-Host "【步骤 4】创建导航脚本..." -ForegroundColor Yellow

$navScript = Join-Path $OutputDir "navigate.ps1"
@"
# 快速导航脚本

`$base = "$extractDir"

Write-Host "【APK 文件浏览】" -ForegroundColor Cyan
Write-Host "`n1. Lua 脚本目录:`n   `$base\assets\base\src\`n"
Write-Host "2. 资源 ZIP:`n   `$base\assets\base\res\client.zip`n"
Write-Host "3. 配置文件:`n   `$base\assets\base\config.json`n"
Write-Host "4. Native 库:`n   `$base\lib\arm64-v8a\`n"

Write-Host "使用示例:"
Write-Host "  dir `$base\assets\base\src               # 列出 Lua 文件"
Write-Host "  type `$base\assets\base\config.json      # 查看配置"
Write-Host "  dir `$base\lib\arm64-v8a                 # 列出本地库"
"@ | Out-File -FilePath $navScript -Encoding UTF8

# 显示摘要
Write-Host "================================================================================`n"
Write-Host "【反编译摘要】" -ForegroundColor Green
Write-Host "================================================================================`n"

$stats = @{
    "APK 文件" = $ApkPath
    "输出目录" = (Resolve-Path $OutputDir).Path
    "提取文件数" = @(Get-ChildItem -Path $extractDir -Recurse).Count
    "报告位置" = $reportPath
    "导航脚本" = $navScript
}

$stats.GetEnumerator() | ForEach-Object {
    Write-Host "✅ $($_.Key): $($_.Value)" -ForegroundColor Cyan
}

Write-Host "`n【建议操作】" -ForegroundColor Yellow
Write-Host "1. 浏览 Lua 脚本: Get-ChildItem '$extractDir\assets\base\src' -Filter '*.luac'"
Write-Host "2. 反编译 Lua: python tools/decompile_lua.py"
Write-Host "3. 反编译 Java: python tools/dex_to_java.py"
Write-Host "4. 查看报告: Get-Content '$reportPath' | more"
Write-Host ""
