import json

dict_additions = {
    "Manage your plan, credentials, and general preferences.": "管理您的计划、凭据和常规首选项。",
    "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 将收集使用数据以帮助 Google 提升性能和功能。",
    "Marketing Emails": "营销邮件",
    "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收来自 Google Antigravity 的产品更新、提示和促销信息。",
    "Your Plan: Google AI Pro": "您的计划：Google AI Pro",
    "You can upgrade to a Google AI Ultra plan to receive the highest rate limits.": "您可以升级到 Google AI Ultra 计划以获得最高的速率限制。",
    "Email": "电子邮箱",
    "Sign Out": "退出登录",
    "By using this app, you agree to its ": "使用此应用即表示您同意其 ",
    "Terms of Service": "服务条款",
    "Configure global allowed and denied resource permissions.": "配置全局允许和拒绝的资源权限。",
    "Project-Specific Settings": "项目专用设置",
    "Modify scoped permissions, folders, and agent settings like Sandbox and Terminal Command Execution.": "修改范围权限、文件夹以及智能体设置（如沙盒和终端命令执行）。",
    "File Permissions": "文件权限",
    "Network Permissions": "网络权限",
    "Terminal & Tooling Permissions": "终端和工具权限",
    "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题和显示首选项。",
    "Configure the browser subagent. It requires ": "配置浏览器子智能体。需要安装 ",
    "Google Chrome": "Google Chrome",
    " to be installed. The browser subagent can be invoked by typing /browser in the conversation input box.": "。可以通过在对话输入框中输入 /browser 来调用浏览器子智能体。",
    "Inherits from global settings. Local permissions have higher priority.": "继承自全局设置。本地权限具有更高的优先级。",
    "Keyboard shortcuts for quick navigation and control.": "用于快速导航和控制的快捷键。",
    "RECOMMENDED": "推荐",
    "Focus Input": "聚焦输入框",
    "NAVIGATION": "导航",
    "Go Back": "后退",
    "Go Forward": "前进",
    "File Picker": "文件选择器",
    "Select Previous Conversation": "选择上一个对话",
    "Select Next Conversation": "选择下一个对话",
    "Toggle Model Selector": "切换模型选择器",
    "Toggle Voice Recording": "切换语音录制",
    "Find in Pane": "在窗格中查找",
    "LAYOUT CONTROLS": "布局控制",
    "Toggle Auxiliary Pane": "切换辅助窗格",
    "Zoom In": "放大",
    "Zoom Out": "缩小",
    "Reset Zoom": "重置缩放",
    "Toggle Developer Tools": "切换开发者工具",
    "Minimize": "最小化",
    "Maximize": "最大化",
    "Group By": "分组方式",
    "Sort Conversations": "排序对话",
    "Alphabetical (A-Z)": "按字母顺序 (A-Z)",
    "Subtitles": "副标题",
    "Worktree": "工作树",
    "No Subtitle": "无副标题",
    "Bug Report": "错误报告",
    "Feature Request": "功能请求",
    "General Feedback": "一般反馈",
    "Description": "描述",
    "Please describe the issue in detail. The more actionable your feedback, the quicker our team can address your request. Some helpful information includes:": "请详细描述您的问题。您的反馈越具体，我们的团队就能越快处理您的请求。一些有用的信息包括：",
    "Steps to reproduce the issue": "重现问题的步骤",
    "Expected behavior": "预期行为",
    "Actual behavior": "实际行为",
    "Any error messages": "任何错误消息",
    "Any relevant information": "任何相关信息",
    "Steps to Reproduce": "重现步骤",
    "Please list the steps to reproduce the issue": "请列出重现该问题的步骤",
    "Attach a screenshot (optional)": "附上截图（可选）",
    "Attach Antigravity server logs": "附上 Antigravity 服务器日志",
}

json_path = 'locales/zh-CN/webui.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'exact' not in data:
    data['exact'] = {}

for k, v in dict_additions.items():
    data['exact'][k] = v

if 'regex' not in data:
    data['regex'] = {}

data['regex']['^Send feedback as (.+)$'] = '以 \\\\1 的身份发送反馈'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Dictionary updated with ALL screenshot strings!')
