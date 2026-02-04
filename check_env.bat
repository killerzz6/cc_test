@echo off
REM Android 开发环境检查脚本

echo ============================================
echo Android 开发环境检查
echo ============================================

echo.
echo 1. 检查 Python...
python --version
if errorlevel 1 (
    echo ERROR: 未找到 Python，请先安装
    exit /b 1
)

echo.
echo 2. 检查 Java JDK...
java -version
if errorlevel 1 (
    echo ERROR: 未找到 Java，请先安装 JDK 11+
    exit /b 1
)

echo.
echo 3. 检查 Android SDK...
if defined ANDROID_SDK_ROOT (
    echo   ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
) else (
    echo ERROR: 未设置 ANDROID_SDK_ROOT 环境变量
    echo   请设置: setx ANDROID_SDK_ROOT "C:\Android\sdk"
    exit /b 1
)

echo.
echo 4. 检查 Android NDK...
if defined ANDROID_NDK_ROOT (
    echo   ANDROID_NDK_ROOT: %ANDROID_NDK_ROOT%
) else (
    echo ERROR: 未设置 ANDROID_NDK_ROOT 环境变量
    echo   请设置: setx ANDROID_NDK_ROOT "C:\Android\ndk\r25"
    exit /b 1
)

echo.
echo 5. 检查 adb...
adb version
if errorlevel 1 (
    echo WARNING: adb 不在 PATH 中
)

echo.
echo ============================================
echo 环境检查完成！
echo ============================================
echo.
echo 下一步：运行 buildozer android debug
