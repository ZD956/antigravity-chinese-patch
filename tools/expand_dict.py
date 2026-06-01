import json

with open('locales/zh-CN/webui.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add all the strings from the screenshots
missing_ui = {
    'Chat Settings': '聊天设置',
    'Verbose agent chat': '详细的智能体聊天',
    'Display and preserve intermediate thinking steps': '显示并保留中间思考过程',
    'Select light, dark, or inherit system settings.': '选择浅色、深色或跟随系统设置。',
    'Light Theme': '浅色主题',
    'Preset': '预设',
    'Default Light': '默认浅色',
    'Background': '背景色',
    'Foreground': '前景色',
    'Accent': '强调色',
    'Dark Theme': '深色主题',
    'Default Dark': '默认深色',
    
    'Browser Settings': '浏览器设置',
    'Configure the browser subagent. It requires Google Chrome to be installed. The browser subagent can be invoked by typing /browser in the conversation input box.': '配置浏览器子智能体。这需要安装 Google Chrome。可以在对话输入框中输入 /browser 来调用浏览器子智能体。',
    'Browser Javascript Execution Policy': '浏览器 Javascript 执行策略',
    'Controls whether the agent can run custom JavaScript to automate complex browser actions.': '控制智能体是否可以运行自定义 JavaScript 来自动执行复杂的浏览器操作。',
    'Actuation Permissions': '操作权限',
    'Browser Actuation Rules': '浏览器操作规则',
    'Configure allowed and denied URLs for browser actuation.': '配置允许和拒绝浏览器操作的 URL。',
    
    'App Settings': '应用设置',
    'Manage application settings.': '管理应用程序设置。',
    'Prevent Sleep': '防止休眠',
    'Prevent the computer from sleeping while the app is running.': '防止计算机在应用程序运行时休眠。',
    'Keep In Menu Bar': '保持在菜单栏',
    'The app will be accessible from the menu bar and will keep running in the background when all windows are closed.': '应用程序将可以从菜单栏访问，并在所有窗口关闭时继续在后台运行。',
    'Notifications': '通知',
    'Notification Settings': '通知设置',
    'To modify notification settings, open your operating system\'s system preferences.': '要修改通知设置，请打开操作系统的系统偏好设置。',
    'System Preferences': '系统偏好设置',
    
    'Enable AI Credit Overages': '启用 AI 额度超额使用',
    'When toggled on, Antigravity will use your AI credits to fulfill model requests once you\'re out of model quota. Antigravity will always use your model quota first before using AI credits.': '开启后，当你耗尽模型配额时，Antigravity 将使用你的 AI 额度来满足模型请求。Antigravity 始终会优先使用模型配额。',
    'View your available model quota and AI credits. Model quota refreshes periodically based on your plan. Enable AI Credit Overages to continue using models when your quota is exhausted.': '查看你可用的模型配额和 AI 额度。模型配额会根据你的套餐定期刷新。当配额耗尽时，请启用“AI 额度超额使用”以继续使用模型。',
    
    'Configure default behaviors, skills, and MCP servers.': '配置默认行为、技能和 MCP 服务器。',
    'Token Usage': 'Token 使用情况',
    'The breakdown below shows token usage from customizations like skills, rules, and MCP. If the budget is exceeded, large customizations will be truncated automatically.': '以下细分显示了技能、规则和 MCP 等自定义设置的 Token 使用情况。如果超出预算，大型自定义设置将被自动截断。',
    
    'Global': '全局',
    'Plugin: science': '插件: science',
    
    # Generic missing ones
    'Workspace Settings': '工作区设置',
    'User Settings': '用户设置',
    'Sync Settings': '同步设置',
    'Rules': '规则',
    'MCP Servers': 'MCP 服务器',
    'Theme': '主题',
    'Font Family': '字体',
    'Font Size': '字体大小',
    'Line Height': '行高',
    'Word Wrap': '自动换行',
    'Cursor Style': '光标样式',
    'Render Whitespace': '渲染空白字符',
    'Format On Save': '保存时格式化',
    'Auto Save Delay': '自动保存延迟',
    'Tab Size': 'Tab 大小',
    'Insert Spaces': '插入空格',
    'Code Lens': '代码透镜',
    'Minimap': '小地图',
    'Telemetry': '遥测',
    'Crash Reporting': '崩溃报告',
    'Updates': '更新',
    'Check for updates': '检查更新',
    'Automatically download updates': '自动下载更新',
    'Privacy': '隐私',
    'Proxy': '代理',
    'Enable Telemetry': '启用遥测',
    'Check for Updates': '检查更新'
}

data['exact'].update(missing_ui)

# Add Regex support for dynamic strings
if 'regex' not in data:
    data['regex'] = {}

dynamic_strings = {
    r'^Refreshes in (\d+) hours?, (\d+) minutes?$': r'\1 小时 \2 分钟后刷新',
    r'^Refreshes in (\d+) minutes?$': r'\1 分钟后刷新',
    r'^Refreshes in (\d+) hours?$': r'\1 小时后刷新',
    r'^([\d\.]+)% of the customization budget is available.$': r'可用自定义预算为 \1%。',
    r'^Show (\d+) breakdowns$': r'显示 \1 项细分',
    r'^Show (\d+) breakdown$': r'显示 \1 项细分',
    r'^Hide (\d+) breakdowns?$': r'隐藏 \1 项细分'
}

data['regex'].update(dynamic_strings)

with open('locales/zh-CN/webui.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated webui.json with new strings and regex patterns.')
