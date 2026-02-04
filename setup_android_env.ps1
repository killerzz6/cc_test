# Android 环境变量一键设置脚本
# 用法: .\setup_android_env.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Android 环境变量配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")

if (-not $isAdmin) {
    Write-Host "警告：建议以管理员身份运行此脚本" -ForegroundColor Yellow
    Write-Host ""
}

# 默认路径
$defaultSdkPath = "$env:USERPROFILE\AppData\Local\Android\Sdk"
$ndkPath = ""

# 检查 SDK 位置
if (Test-Path $defaultSdkPath) {
    Write-Host "✓ 检测到 Android SDK: $defaultSdkPath" -ForegroundColor Green
    
    # 查找 NDK
    $ndkFolder = Get-ChildItem "$defaultSdkPath\ndk" -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
    if ($ndkFolder) {
        $ndkPath = $ndkFolder.FullName
        Write-Host "✓ 检测到 Android NDK: $ndkPath" -ForegroundColor Green
    } else {
        Write-Host "⚠ 未找到 Android NDK，请先在 Android Studio 中下载" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ 未找到 Android SDK" -ForegroundColor Red
    Write-Host "请先安装 Android Studio: https://developer.android.com/studio" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "设置环境变量..." -ForegroundColor Cyan

# 设置 ANDROID_SDK_ROOT
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", $defaultSdkPath, "User")
Write-Host "✓ 已设置 ANDROID_SDK_ROOT = $defaultSdkPath" -ForegroundColor Green

# 设置 ANDROID_NDK_ROOT
if ($ndkPath) {
    [Environment]::SetEnvironmentVariable("ANDROID_NDK_ROOT", $ndkPath, "User")
    Write-Host "✓ 已设置 ANDROID_NDK_ROOT = $ndkPath" -ForegroundColor Green
}

# 添加 platform-tools 到 PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$platformToolsPath = "$defaultSdkPath\platform-tools"

if ($currentPath -notlike "*platform-tools*") {
    $newPath = "$currentPath;$platformToolsPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ 已添加 platform-tools 到 PATH" -ForegroundColor Green
} else {
    Write-Host "✓ platform-tools 已在 PATH 中" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "验证设置..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 刷新环境变量
$env:ANDROID_SDK_ROOT = [Environment]::GetEnvironmentVariable("ANDROID_SDK_ROOT", "User")
$env:ANDROID_NDK_ROOT = [Environment]::GetEnvironmentVariable("ANDROID_NDK_ROOT", "User")

# 验证
Write-Host "ANDROID_SDK_ROOT: $($env:ANDROID_SDK_ROOT)" -ForegroundColor Cyan
Write-Host "ANDROID_NDK_ROOT: $($env:ANDROID_NDK_ROOT)" -ForegroundColor Cyan

# 检查 adb
$adbPath = "$($env:ANDROID_SDK_ROOT)\platform-tools\adb.exe"
if (Test-Path $adbPath) {
    Write-Host "✓ adb 可用: $adbPath" -ForegroundColor Green
    & $adbPath version | Select-Object -First 1
} else {
    Write-Host "⚠ adb 不可用" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ 配置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步: 重启 PowerShell 并运行构建" -ForegroundColor Yellow
Write-Host "  cd c:\Users\J1\Desktop\cc_test" -ForegroundColor Cyan
Write-Host "  .\build.bat" -ForegroundColor Cyan
Write-Host ""
