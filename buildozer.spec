[app]
# 应用标题和包名
title = Countdown
package.name = countdown
package.domain = org.countdown

# 源码位置
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本信息
version = 1.0
requirements = python3,kivy

# 权限配置
android.permissions = INTERNET

# 架构 (只用 arm64-v8a 加快构建速度)
android.archs = arm64-v8a

# 启动方向
orientation = portrait

# 构建配置
fullscreen = 0

# Android API 版本
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# P4A 配置
p4a.branch = master

[buildozer]
# 日志级别
log_level = 2
warn_on_root = 0
