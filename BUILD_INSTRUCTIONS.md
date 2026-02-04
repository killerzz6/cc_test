# 如何创建 Android 安装包

## 概述

此项目使用 Buildozer 工具将 Python/Kivy 应用编译为 Android APK 文件。

## 前置条件

### 1. 安装 Java JDK 11 或更高版本

**下载**：https://www.oracle.com/java/technologies/downloads/

**验证安装**：
```powershell
java -version
```

### 2. 安装 Android Studio（自动安装 SDK）

**下载**：https://developer.android.com/studio

**安装后自动会安装**：
- Android SDK
- Android SDK Platform-tools（包括 adb）
- Android Emulator

### 3. 设置环境变量

在 Windows PowerShell 中运行：

```powershell
# 设置 Android SDK 路径（通常自动安装在这个位置）
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", "C:\Users\YourUsername\AppData\Local\Android\Sdk", "User")

# 设置 Android NDK 路径（需要在 Android Studio 中下载）
[Environment]::SetEnvironmentVariable("ANDROID_NDK_ROOT", "C:\Android\ndk\r25", "User")

# 刷新环境变量
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### 4. 下载 Android NDK

在 Android Studio 中：
1. Tools → SDK Manager
2. SDK Tools 标签页
3. 勾选 "NDK (Side by side)"
4. 点击 Apply 下载

通常安装在：`C:\Android\ndk\r25` 或 `C:\Users\YourUsername\AppData\Local\Android\Sdk\ndk\25.x.x`

## 构建步骤

### 方法 A：使用自动化脚本（推荐）

```powershell
cd c:\Users\J1\Desktop\cc_test

# 1. 检查环境（可选）
.\check_env.bat

# 2. 运行构建脚本
.\build.bat
```

脚本会自动：
- 创建虚拟环境
- 安装依赖
- 运行 buildozer
- 生成 APK

### 方法 B：手动构建

```powershell
cd c:\Users\J1\Desktop\cc_test

# 1. 创建虚拟环境
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 安装依赖
pip install buildozer cython kivy

# 3. 构建
buildozer android debug

# 生成的 APK: bin/countdown-1.0-debug.apk
```

## 安装到设备

### 连接 Android 手机

1. 用 USB 线连接手机到电脑
2. 在手机上启用"开发者模式"（连续点击"版本号"7 次）
3. 启用"USB 调试"

### 安装 APK

```powershell
# 查看连接的设备
adb devices

# 安装应用
adb install bin/countdown-1.0-debug.apk

# 启动应用
adb shell am start -n org.countdown.countdown/.CountdownFloatingWindowActivity
```

## 构建常见问题

### 问题 1：找不到 Android SDK/NDK

**错误信息**：
```
Could not find Android SDK
```

**解决**：
1. 确认已安装 Android Studio
2. 打开 Android Studio，检查 SDK 安装位置
3. 设置正确的环境变量
4. 重启 PowerShell 使环境变量生效

### 问题 2：构建超级慢或中途停止

**原因**：
- 首次构建下载文件很大（2-5GB）
- 网络连接不稳定

**解决**：
- 确保网络稳定
- 不要中断构建过程
- 可以在后台运行：`buildozer android debug > build.log 2>&1`

### 问题 3：APK 文件很大（50-100MB）

**原因**：
正常现象。包含了完整的 Python 运行环境。

**优化**：
- 使用发布版本：`buildozer android release`
- 启用代码混淆（Proguard）

### 问题 4：SSL 证书错误

**错误**：
```
SSLError: EOF occurred in violation of protocol
```

**解决**：
```powershell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

然后重新运行构建。

## 生成发布版本（署名）

用于 Google Play Store 发布：

```powershell
# 生成密钥（仅第一次）
keytool -genkey -v -keystore my-release-key.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias

# 构建发布版本
buildozer android release
```

## 清理构建缓存

```powershell
# 清理所有构建文件
buildozer android clean

# 仅清理最后一次构建
buildozer android clean_deps
```

## 调试提示

### 查看应用日志

```powershell
adb logcat | findstr countdown
```

### 查看所有日志

```powershell
adb logcat
```

### 卸载应用

```powershell
adb uninstall org.countdown.countdown
```

### 进入应用数据目录

```powershell
adb shell
cd /data/data/org.countdown.countdown/
ls -la
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | Python 应用源代码 |
| `buildozer.spec` | Buildozer 配置文件 |
| `check_env.bat` | 环境检查脚本 |
| `build.bat` | 自动构建脚本 |
| `bin/countdown-1.0-debug.apk` | 最终生成的 APK 文件 |

## 参考资源

- Buildozer 官方文档: https://buildozer.readthedocs.io/
- Kivy 官方文档: https://kivy.org/doc/
- Android 开发者文档: https://developer.android.com/
- Python-for-Android: https://python-for-android.readthedocs.io/
