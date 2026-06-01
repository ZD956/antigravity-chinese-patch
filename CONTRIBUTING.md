# 贡献指南

感谢你考虑为 Antigravity IDE 中文汉化包做出贡献！

## 添加或修改翻译

翻译内容分为两部分：

### 1. Electron 壳层翻译
存放在 `locales/zh-CN/electron.json`。
这部分负责系统菜单、加载页面、提示框等。修改时，请确保 `"英文"` 键和源文件（如 `app.asar/dist/main.js`）中出现的字符串**完全一致**。

### 2. Web UI 界面翻译
存放在 `locales/zh-CN/webui.json`。
这部分负责 IDE 内的大部分界面。
它分为两个部分：
- `"exact"`: 完全匹配的字符串替换。
- `"regex"`: 正则表达式替换（支持 `$1` 等捕获组）。

如果你发现有新的英文文本，可以直接在这个文件中对应的位置添加键值对。

## 测试你的修改

1. 在修改完 JSON 文件后，在控制台运行 `python patch.py patch` 重新打包。
2. （重要）如果脚本提示已备份，你可能需要先运行 `python patch.py unpatch` 恢复环境，或直接强制覆盖。
3. 重新启动 IDE 以查看更改效果。

## 提交 Pull Request
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingTranslation`)
3. 提交你的更改 (`git commit -m 'Add some AmazingTranslation'`)
4. 推送到分支 (`git push origin feature/AmazingTranslation`)
5. 开启一个 Pull Request
