# Java 环境变量自动配置脚本
# 用法: .\setup_java_env.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Java 环境变量自动配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 第一步：查找 Java 安装目录
Write-Host "第一步：查找 Java 安装目录..." -ForegroundColor Yellow
$javaPath = $null

if (Test-Path "C:\Program Files\Java") {
    $javaVersions = Get-ChildItem "C:\Program Files\Java" | Where-Object { $_.PSIsContainer -and $_.Name -like "jdk*" }
    
    if ($javaVersions) {
        # 选择最新的版本
        $latestJava = $javaVersions | Sort-Object Name -Descending | Select-Object -First 1
        $javaPath = $latestJava.FullName
        Write-Host "✓ 检测到 Java: $javaPath" -ForegroundColor Green
    }
}

if (-not $javaPath) {
    Write-Host "✗ 未找到 Java JDK" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Java JDK 11 或更高版本:" -ForegroundColor Yellow
    Write-Host "https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "安装后重新运行此脚本" -ForegroundColor Yellow
    exit
}

# 第二步：设置 JAVA_HOME
Write-Host ""
Write-Host "第二步：设置 JAVA_HOME 环境变量..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("JAVA_HOME", $javaPath, "User")
$env:JAVA_HOME = $javaPath
Write-Host "✓ 已设置 JAVA_HOME = $javaPath" -ForegroundColor Green

# 第三步：添加到 PATH
Write-Host ""
Write-Host "第三步：添加 JAVA_HOME\bin 到 PATH..." -ForegroundColor Yellow
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$javaBinPath = "$javaPath\bin"

if ($currentPath -notlike "*$javaBinPath*") {
    $newPath = "$currentPath;$javaBinPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ 已添加到 PATH" -ForegroundColor Green
} else {
    Write-Host "✓ 已在 PATH 中" -ForegroundColor Green
}

# 第四步：验证
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "验证配置..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "JAVA_HOME: $($env:JAVA_HOME)" -ForegroundColor Cyan

# 检查 java.exe
$javaExe = "$($env:JAVA_HOME)\bin\java.exe"
if (Test-Path $javaExe) {
    Write-Host "✓ java.exe 可用: $javaExe" -ForegroundColor Green
} else {
    Write-Host "✗ java.exe 不可用" -ForegroundColor Red
}

# 显示 Java 版本
Write-Host ""
Write-Host "Java 版本信息:" -ForegroundColor Cyan
& "$javaExe" -version

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Java 环境配置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "重要: 需要关闭当前 PowerShell 并重新打开，使环境变量生效" -ForegroundColor Yellow
Write-Host ""
Write-Host "然后运行:" -ForegroundColor Cyan
Write-Host "  cd c:\Users\J1\Desktop\cc_test`" -ForegroundColor White
Write-Host '  .\setup_android_env.ps1' -ForegroundColor White
Write-Host ""
