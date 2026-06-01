# Web UI Localization Dictionary Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Antigravity Web UI Chinese dictionary coverage for fixed UI text, prioritizing settings and avoiding chat/model-output content.

**Architecture:** This is a data-only localization change centered on `locales/zh-CN/webui.json`. We will mine high-confidence UI strings from the extracted Web UI bundle, add conservative `exact` translations, and only add anchored `regex` translations for stable UI templates that cannot reasonably hit conversation content.

**Tech Stack:** Python 3 for JSON validation/counting, existing project patcher, JSON localization dictionary, JavaScript injector already present in `inject/translator.js`.

---

## File Structure

- Modify: `locales/zh-CN/webui.json` — add fixed UI translations under `exact`, and a small number of safe anchored templates under `regex` if needed.
- Read only: `extracted_webui/candidate_strings.txt` — source of candidate UI strings.
- Read only: `extracted_webui/main.js` — source context for settings/UI strings when candidate entries are ambiguous.
- Read only: `inject/translator.js` — confirm dictionary application behavior if needed.
- Optional run only: `patch.py` — existing patch workflow to inject the updated dictionary.

## Task 1: Baseline Dictionary and Candidate Audit

**Files:**
- Read: `locales/zh-CN/webui.json`
- Read: `extracted_webui/candidate_strings.txt`
- Read: `extracted_webui/main.js`

- [ ] **Step 1: Count current dictionary entries**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
p = Path('/c/Users/zhoujunnan/Desktop/antigravity-chinese-patch/locales/zh-CN/webui.json')
data = json.loads(p.read_text(encoding='utf-8'))
print('exact', len(data.get('exact', {})))
print('regex', len(data.get('regex', {})))
PY
```

Expected: command prints the current exact and regex counts without JSON parse errors.

- [ ] **Step 2: Identify settings-related untranslated candidates**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
root = Path('/c/Users/zhoujunnan/Desktop/antigravity-chinese-patch')
webui = json.loads((root/'locales/zh-CN/webui.json').read_text(encoding='utf-8'))
existing = set(webui.get('exact', {}))
keywords = [
    'setting', 'preference', 'model', 'account', 'profile', 'theme', 'workspace',
    'project', 'folder', 'file access', 'permission', 'review', 'browser', 'mcp',
    'hook', 'scheduled', 'task', 'notification', 'shortcut', 'editor', 'terminal',
    'allowlist', 'auth', 'credit', 'quota', 'plan', 'privacy', 'security'
]
for line in (root/'extracted_webui/candidate_strings.txt').read_text(encoding='utf-8', errors='ignore').splitlines():
    s = line.strip()
    if not s or s in existing:
        continue
    low = s.lower()
    if any(k in low for k in keywords):
        print(s)
PY
```

Expected: output is a review list of untranslated settings/UI candidate strings.

- [ ] **Step 3: Inspect source context for ambiguous candidates**

For any string that might be chat/model-output text, inspect `extracted_webui/main.js` around the literal using the Grep tool instead of translating it blindly. Only keep strings that are fixed UI labels, buttons, settings descriptions, empty states, or product error/status messages.

## Task 2: Add High-Confidence Exact Translations

**Files:**
- Modify: `locales/zh-CN/webui.json`

- [ ] **Step 1: Add exact entries for settings and fixed UI text**

Edit the `exact` object in `locales/zh-CN/webui.json`. Keep valid JSON and preserve the existing structure. Add only entries that are visible fixed UI strings. Use this translation style:

```json
{
  "General": "通用",
  "Appearance": "外观",
  "Advanced": "高级",
  "Notifications": "通知",
  "Privacy": "隐私",
  "Security": "安全",
  "Integrations": "集成",
  "Models": "模型",
  "Custom Models": "自定义模型",
  "Model Provider": "模型提供商",
  "API Key": "API 密钥",
  "Base URL": "基础 URL",
  "Display Name": "显示名称",
  "Description": "描述",
  "Instructions": "指令",
  "Permissions": "权限",
  "Allow": "允许",
  "Deny": "拒绝",
  "Always allow": "始终允许",
  "Always deny": "始终拒绝",
  "Ask every time": "每次询问",
  "File Access Policy": "文件访问策略",
  "Web Access Policy": "网页访问策略",
  "Review Policy": "审查策略",
  "Require approval": "需要批准",
  "Auto approve": "自动批准",
  "Never allow": "永不允许",
  "Open in editor": "在编辑器中打开",
  "Open in browser": "在浏览器中打开",
  "Open in terminal": "在终端中打开",
  "Show hidden files": "显示隐藏文件",
  "Hide hidden files": "隐藏隐藏文件",
  "Enable notifications": "启用通知",
  "Disable notifications": "禁用通知",
  "Reset to default": "重置为默认值",
  "Reset Settings": "重置设置",
  "Save Changes": "保存更改",
  "Discard Changes": "放弃更改",
  "Unsaved changes": "未保存的更改",
  "No changes": "没有更改",
  "Manage": "管理",
  "Configure": "配置",
  "Connected": "已连接",
  "Disconnected": "未连接",
  "Connect": "连接",
  "Disconnect": "断开连接",
  "Authorize": "授权",
  "Revoke access": "撤销访问权限",
  "Authentication": "身份验证",
  "Not authenticated": "未认证",
  "Authenticated": "已认证"
}
```

Do not duplicate keys that already exist. If a key already exists, keep the existing translation unless it is clearly wrong.

- [ ] **Step 2: Add additional exact entries from the audit list**

For each high-confidence candidate from Task 1, add it to `exact` with a concise Chinese translation. Exclude these categories:

```text
- long prose likely generated by the assistant/model
- user-authored chat message content
- code snippets or terminal output
- arbitrary log body text
- markdown fragments from conversation messages
- strings with many interpolated variables unless they are clearly UI templates
```

- [ ] **Step 3: Validate JSON after editing**

Run:

```bash
python -m json.tool /c/Users/zhoujunnan/Desktop/antigravity-chinese-patch/locales/zh-CN/webui.json >/dev/null
```

Expected: no output and exit code 0.

## Task 3: Add Conservative Regex Templates Only If Needed

**Files:**
- Modify: `locales/zh-CN/webui.json`

- [ ] **Step 1: Review candidate templates**

Only add regex rules when the English string is a short, stable UI template with predictable dynamic content. Safe examples:

```json
{
  "^(\\d+) workspaces?$": "$1 个工作区",
  "^(\\d+) projects?$": "$1 个项目",
  "^(\\d+) models?$": "$1 个模型",
  "^Last updated (.*)$": "最后更新于 $1",
  "^Created (.*)$": "创建于 $1",
  "^Updated (.*)$": "更新于 $1",
  "^Delete (.*)\\?$": "要删除 $1 吗？",
  "^Remove (.*)\\?$": "要移除 $1 吗？"
}
```

Do not add broad rules that would translate arbitrary natural language in chat messages.

- [ ] **Step 2: Validate JSON after regex edits**

Run:

```bash
python -m json.tool /c/Users/zhoujunnan/Desktop/antigravity-chinese-patch/locales/zh-CN/webui.json >/dev/null
```

Expected: no output and exit code 0.

## Task 4: Validate Counts and Patch Flow

**Files:**
- Read: `locales/zh-CN/webui.json`
- Run: `patch.py`

- [ ] **Step 1: Count final dictionary entries**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
p = Path('/c/Users/zhoujunnan/Desktop/antigravity-chinese-patch/locales/zh-CN/webui.json')
data = json.loads(p.read_text(encoding='utf-8'))
print('exact', len(data.get('exact', {})))
print('regex', len(data.get('regex', {})))
PY
```

Expected: exact count is higher than the baseline; regex count is unchanged or only slightly higher.

- [ ] **Step 2: Run existing patch workflow**

Run from the project directory:

```bash
python patch.py
```

Expected: patch completes successfully, repacks or updates the target ASAR using the existing workflow, and reports no JSON or ASAR errors.

- [ ] **Step 3: Confirm injected dictionary counts if patch output or files expose them**

If the patch workflow prints injected dictionary counts, verify they match `webui.json`. If not, inspect the generated/injected preload bundle only enough to confirm the updated keys are present.

## Task 5: Manual Verification Notes

**Files:**
- No required file changes.

- [ ] **Step 1: Launch Antigravity and inspect settings screens**

Open Antigravity normally. Navigate through Settings, model/account/project/workspace/file-access/MCP/task-related screens. Confirm many more fixed labels and buttons are Chinese.

- [ ] **Step 2: Verify chat/model output remains untouched**

Open an existing or new conversation containing English assistant output. Confirm the large model response text is not broadly rewritten by the dictionary. Small fixed UI controls around the message may be Chinese.

- [ ] **Step 3: Record any remaining untranslated fixed UI text**

If important settings labels remain untranslated, copy the exact English text for another dictionary pass.

## Self-Review

- Spec coverage: The plan covers settings-first dictionary expansion, conservative exact translations, avoiding model output, JSON validation, patch verification, and manual UI checks.
- Placeholder scan: No placeholder tasks or undefined implementation steps remain.
- Scope check: This is one focused dictionary expansion and validation pass, not a broader injector rewrite.
