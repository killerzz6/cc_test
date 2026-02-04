@echo off
REM 快速构建 APK 脚本

setlocal enabledelayedexpansion

echo ============================================
echo Android APK 构建脚本
echo ============================================

REM 检查环境
if not defined ANDROID_SDK_ROOT (
    echo ERROR: 未设置 ANDROID_SDK_ROOT
    echo 请先运行: setx ANDROID_SDK_ROOT "C:\Android\sdk"
    pause
    exit /b 1
)

if not defined ANDROID_NDK_ROOT (
    echo ERROR: 未设置 ANDROID_NDK_ROOT
    echo 请先运行: setx ANDROID_NDK_ROOT "C:\Android\ndk\r25"
    pause
    exit /b 1
)

echo.
echo 检测到:
echo   ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
echo   ANDROID_NDK_ROOT: %ANDROID_NDK_ROOT%
echo.

REM 激活虚拟环境
if exist .venv\Scripts\activate.bat (
    echo 激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo 创建虚拟环境...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM 安装依赖
echo.
echo 安装依赖...
pip install -U pip setuptools
pip install buildozer cython

REM 运行 buildozer
echo.
echo 开始构建... (这可能需要 30+ 分钟)
buildozer android debug

if errorlevel 1 (
    echo.
    echo ERROR: 构建失败
    pause
    exit /b 1
)

echo.
echo ============================================
echo 构建成功！
echo APK 文件位置: bin/countdown-1.0-debug.apk
echo ============================================
echo.
echo 安装到设备: adb install bin/countdown-1.0-debug.apk
echo.
pause
