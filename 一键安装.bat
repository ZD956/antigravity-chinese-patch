@echo off
title Antigravity IDE 汉化包 - 一键安装

echo ==========================================
echo        Antigravity IDE 汉化包安装程序
echo ==========================================
echo.
echo 正在检测 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 环境！
    echo 请先安装 Python，并确保添加到系统 PATH 环境变量中。
    echo.
    pause
    exit /b
)

echo [提示] 正在执行注入补丁...
python patch.py patch

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo [成功] 汉化补丁安装完毕！
    echo 请完全关闭并重新启动 Antigravity IDE 即可看到中文界面。
    echo ==========================================
) else (
    echo.
    echo [失败] 汉化补丁安装过程中出现错误，请查看上方报错信息。
)

echo.
pause
