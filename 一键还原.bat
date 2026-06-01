@echo off
title Antigravity IDE 汉化包 - 一键还原

echo ==========================================
echo        Antigravity IDE 汉化包还原程序
echo ==========================================
echo.
echo 正在检测 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 环境！
    pause
    exit /b
)

echo [提示] 正在执行还原操作...
python patch.py restore

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo [成功] 汉化补丁已成功移除，已恢复为原版英文。
    echo 请完全关闭并重新启动 Antigravity IDE。
    echo ==========================================
) else (
    echo.
    echo [失败] 还原过程中出现错误，请查看上方报错信息。
)

echo.
pause
