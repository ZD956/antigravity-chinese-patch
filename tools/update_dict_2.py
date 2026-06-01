import json

dict_additions = {
    'Configure allowed terminal commands.': '配置允许的终端命令。',
    'Configure allowed commands outside the sandbox.': '配置沙盒外允许的命令。',
    'Configure external tools via Model Context Protocol.': '通过模型上下文协议 (MCP) 配置外部工具。',
    'Installed MCP Servers': '已安装的 MCP 服务器',
    'No MCP Servers': '无 MCP 服务器',
    "You currently don't have any MCP Servers installed. Add an MCP server above": '您当前未安装任何 MCP 服务器。请在上方添加 MCP 服务器',
    'Inherits from global settings. Local permissions have higher priority.': '继承自全局设置。本地权限具有更高的优先级。',
    'Configure the browser subagent. It requires Google Chrome to be installed. The browser subagent can be invoked by typing /browser in the conversation input box.': '配置浏览器子智能体。需要安装 Google Chrome。可通过在对话框输入 /browser 调用浏览器子智能体。',
    'Conversation Picker': '对话选择器',
    'File Search': '文件搜索',
    'LAYOUT CONTROLS': '布局控制',
    'RECOMMENDED': '推荐',
    'NAVIGATION': '导航'
}

json_path = 'locales/zh-CN/webui.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'exact' not in data:
    data['exact'] = {}

for k, v in dict_additions.items():
    data['exact'][k] = v

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated 121100-121222 strings')
