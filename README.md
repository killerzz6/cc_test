# Android 悬浮窗倒计时应用

## 项目说明
一个简单的 Android 悬浮窗应用，显示 60 秒倒计时。使用 Kivy 框架开发。

## 前置要求

### Windows 开发环境
- Python 3.8+
- Java JDK 11+（用于 Android 编译）
- Android SDK（API Level 30+）
- Android NDK（r23c 或 r25）

## 本地构建 APK

### 步骤 1：安装构建工具
```powershell
pip install buildozer cython kivy
```

### 步骤 2：配置 Android SDK 和 NDK
设置环境变量：
```powershell
$env:ANDROID_SDK_ROOT = "C:\Android\sdk"
$env:ANDROID_NDK_ROOT = "C:\Android\ndk\r25"
```

### 步骤 3：运行 buildozer 构建
```powershell
buildozer android debug
```

生成的 APK 文件位于：`bin/countdown-1.0-debug.apk`

### 步骤 4：安装到设备
```powershell
adb install bin/countdown-1.0-debug.apk
```

## 自定义配置

### 修改倒计时时间
编辑 `main.py` 第 9 行：
```python
self.countdown_time = 60  # 改成你想要的秒数
```

### 修改应用名称和包名
编辑 `buildozer.spec`：
```ini
title = 你的应用名称
package.name = countdown
package.domain = org.countdown
```

### 修改颜色
编辑 `main.py`：
- 背景色：`Color(0.2, 0.2, 0.2, 0.9)` - RGB + Alpha
- 文字色：`color=(1, 1, 1, 1)` - 白色

## 云端构建（推荐 - 网络受限）

本地构建需要完整的 Android 开发环境。如果遇到网络问题，可以使用在线构建服务。

**推荐选项**：
1. **使用 Python 在线 IDE**：
   - Replit、PythonAnywhere 等提供 Python 环境
   - 手动上传文件或使用 Git

2. **Buildozer 云服务**：
   - 网址：https://buildozer.app/
   - 上传 main.py 和 buildozer.spec
   - 等待构建完成并下载 APK

## 常见问题

**Q: 找不到 Android SDK？**
A: 安装 Android Studio，配置 `ANDROID_SDK_ROOT` 环境变量

**Q: APK 文件很大（50-100MB）？**
A: 正常现象，Kivy 包含 Python 运行环境

**Q: 应用在旧 Android 版本上不能运行？**
A: 修改 `buildozer.spec` 中的 `android.api` 和 `android.minapi`

## 快速命令参考

```powershell
# 清理构建缓存
buildozer android clean

# 查看帮助
buildozer android help

# 生成发布版本（签名）
buildozer android release
```

## 参考资源

- Kivy 官方文档: https://kivy.org/doc/
- Buildozer 文档: https://buildozer.readthedocs.io/
- Android 开发文档: https://developer.android.com/
