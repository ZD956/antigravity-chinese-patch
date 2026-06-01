# -*- coding: utf-8 -*-
"""
Antigravity IDE 汉化补丁核心脚本 (Antigravity Chinese Patch)
用于读取翻译配置，修改 app.asar，并注入 preload.js 翻译引擎。
"""

import json
import os
import sys
import shutil
import platform
import argparse
from pathlib import Path
from asar import read_asar, collect_all_files, write_asar

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.resolve()

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def apply_translations(content: bytes, translations: dict) -> tuple[bytes, list]:
    text = content.decode('utf-8')
    log = []
    
    for eng, chn in translations.items():
        if eng in text:
            count = text.count(eng)
            text = text.replace(eng, chn)
            log.append((eng, chn, count))
            
    return text.encode('utf-8'), log

def get_asar_path():
    if platform.system() != 'Windows':
        print("Error: This patch currently only supports Windows.")
        return None
        
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if not local_app_data:
        return None
        
    path = os.path.join(local_app_data, 'Programs', 'antigravity', 'resources', 'app.asar')
    if os.path.exists(path):
        return path
    return None

def inject_translator(preload_content: bytes, translator_js_path: str, webui_translations: dict) -> bytes:
    try:
        with open(translator_js_path, 'r', encoding='utf-8') as f:
            translator_code = f.read()
    except Exception as e:
        print(f"Error loading translator script: {e}")
        return preload_content
        
    translations_json = json.dumps(webui_translations, ensure_ascii=False)
    injection = f"\n\n// --- Antigravity Chinese Patch Inject --- \nwindow.__AGY_WEBUI_TRANSLATIONS = {translations_json};\n{translator_code}\n"
    
    # If already injected, slice it off before appending new version
    marker = b"// --- Antigravity Chinese Patch Inject ---"
    if marker in preload_content:
        preload_content = preload_content[:preload_content.find(marker)]
        print("  ⚠️ Old translator found; updating to new version.")
        
    return preload_content + injection.encode('utf-8')

def check_process():
    import subprocess
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Antigravity.exe" /NH', shell=True).decode('gbk', errors='ignore')
        if "Antigravity.exe" in output:
            print("\n❌ 错误: 发现 Antigravity IDE 正在运行！")
            print("   在安装或卸载补丁前，请务必完全关闭 IDE（包括托盘图标右键->退出）。")
            return True
    except:
        pass
    return False

def patch(asar_path, ignore_process=False):
    print("=" * 60)
    print("  Antigravity IDE 汉化包 - 开始安装")
    print("=" * 60)
    
    if not ignore_process and check_process():
        return False
        
    if not os.path.exists(asar_path):
        print(f"\n❌ 错误: 找不到 app.asar。路径: {asar_path}")
        return False
        
    backup_path = asar_path + '.bak'
    if os.path.exists(backup_path):
        print(f"\n⚠️ 发现已存在备份文件: {backup_path}")
        print("   IDE 可能已经汉化过了。建议先运行 'python patch.py unpatch' 还原。")
        resp = input("   是否强制继续覆盖? (y/N): ").strip().lower()
        if resp != 'y':
            return False
            
    print(f"\n[1/4] 正在备份 app.asar...")
    shutil.copy2(asar_path, backup_path)
    print(f"  ✅ 备份已保存至: {backup_path}")
    
    print(f"\n[2/4] 正在解析 ASAR 归档...")
    header, data_offset, data = read_asar(asar_path)
    file_contents = collect_all_files(header, data)
    print(f"  ✅ 成功读取 {len(file_contents)} 个文件")
    
    print(f"\n[3/4] 正在注入汉化内容...")
    electron_dict = load_json(PROJECT_ROOT / 'locales' / 'zh-CN' / 'electron.json') or {}
    webui_dict = load_json(PROJECT_ROOT / 'locales' / 'zh-CN' / 'webui.json') or {}
    translator_path = PROJECT_ROOT / 'inject' / 'translator.js'
    
    total_replacements = 0
    for filepath, translations in electron_dict.items():
        if filepath in file_contents:
            content = file_contents[filepath]
            new_content, log = apply_translations(content, translations)
            if log:
                file_contents[filepath] = new_content
                for eng, chn, count in log:
                    print(f"  ✅ [{filepath}] \"{eng}\" → \"{chn}\" ({count}次)")
                    total_replacements += count
            else:
                print(f"  ⏭️ [{filepath}] 未找到匹配的字符串")
        else:
            print(f"  ⚠️ [{filepath}] 在 ASAR 中未找到")
            
    if 'dist/preload.js' in file_contents:
        print(f"  ✅ [dist/preload.js] 正在注入 Web UI 动态翻译引擎...")
        file_contents['dist/preload.js'] = inject_translator(file_contents['dist/preload.js'], str(translator_path), webui_dict)
        total_replacements += 1
    
    if total_replacements == 0:
        print(f"\n❌ 没有任何汉化生效。终止操作。")
        os.remove(backup_path)
        return False
        
    print(f"\n[4/4] 正在重新打包 ASAR...")
    import copy
    header_copy = copy.deepcopy(header)
    write_asar(asar_path, header_copy, file_contents)
    print(f"  ✅ 打包完成！")
    
    print(f"\n{'='*60}")
    print(f"  🎉 汉化安装成功！")
    print(f"  请重新启动 Antigravity IDE 查看效果。")
    print(f"  若要还原为英文，请运行: python patch.py unpatch")
    print(f"{'='*60}")
    return True

def unpatch(asar_path, ignore_process=False):
    print("=" * 60)
    print("  Antigravity IDE 汉化包 - 开始还原")
    print("=" * 60)
    
    if not ignore_process and check_process():
        return False
        
    backup_path = asar_path + '.bak'
    if not os.path.exists(backup_path):
        print(f"\n❌ 未找到备份文件: {backup_path}")
        print("   无需还原。")
        return False
        
    shutil.copy2(backup_path, asar_path)
    os.remove(backup_path)
    
    print(f"\n✅ 成功还原 app.asar 原始文件。")
    print(f"   请重新启动 Antigravity IDE。")
    return True

def status(asar_path):
    print("=" * 60)
    print("  Antigravity IDE 汉化包 - 状态检查")
    print("=" * 60)
    
    if not os.path.exists(asar_path):
        print(f"\n❌ 找不到 app.asar。路径: {asar_path}")
        return
        
    print(f"\n  ASAR 路径: {asar_path}")
    print(f"  文件大小:  {os.path.getsize(asar_path):,} bytes")
    
    backup_path = asar_path + '.bak'
    if os.path.exists(backup_path):
        print(f"  备份文件:  ✅ 已存在")
        print(f"  当前状态:  🟢 已汉化 (Patched)")
    else:
        print(f"  备份文件:  ❌ 未找到")
        print(f"  当前状态:  🔵 官方原版 (Original)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Antigravity IDE Chinese Patch Tool")
    parser.add_argument('command', choices=['patch', 'unpatch', 'status'], nargs='?', default='patch', help="Command to execute")
    parser.add_argument('--path', help="Custom path to app.asar")
    parser.add_argument('--ignore-process', action='store_true', help="Ignore if Antigravity is running (for testing)")
    
    args = parser.parse_args()
    
    target_path = args.path if args.path else get_asar_path()
    if not target_path:
        print("Error: Could not determine app.asar path. Please specify it using --path.")
        sys.exit(1)
        
    if args.command == 'patch':
        if not patch(target_path, ignore_process=args.ignore_process):
            sys.exit(1)
    elif args.command == 'unpatch':
        if not unpatch(target_path, ignore_process=args.ignore_process):
            sys.exit(1)
    elif args.command == 'status':
        status(target_path)
