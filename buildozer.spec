[app]
# 应用标题和包名
title = 倒计时悬浮窗
package.name = countdown
package.domain = org.countdown

# 源码位置
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本信息
version = 1.0
requirements = python3,kivy,android

# 权限配置
android.permissions = SYSTEM_ALERT_WINDOW,INTERNET,ACCESS_NETWORK_STATE

# 特性配置
android.features = android.hardware.touchscreen

# 架构
android.archs = arm64-v8a,armeabi-v7a

# 启动方向
orientation = portrait

# 构建配置
fullscreen = 0

# 以下根据你的实际路径修改（Windows 用户通常自动安装在这个位置）
# android.sdk_root = /path/to/android-sdk
# android.ndk_root = /path/to/android-ndk

[buildozer]
# 日志级别
log_level = 2
warn_on_root = 1
