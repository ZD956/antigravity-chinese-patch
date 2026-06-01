# Web UI Localization Dictionary Expansion Design

## Goal

Improve Antigravity Web UI Chinese localization coverage by expanding `locales/zh-CN/webui.json`, with settings screens as the first priority. The dictionary should translate fixed UI text such as settings labels, buttons, menus, tabs, status text, and common prompts.

## Scope

Translate high-confidence product UI strings mined from the existing extracted Web UI bundle, especially strings related to settings, preferences, models, account, editor behavior, notifications, shortcuts, integrations, and workspace controls.

Do not translate chat conversation content, large model responses, user input, code blocks, or arbitrary log/body text. Avoid broad regex rules that could rewrite dynamic conversation text.

## Approach

Use the existing `webui.json` structure and add targeted `exact` entries where possible. Add regex entries only for stable UI templates with clear boundaries. Prefer conservative translation coverage over aggressive rules that might affect model output.

Primary inputs are:

- `locales/zh-CN/webui.json`
- `extracted_webui/candidate_strings.txt`
- `extracted_webui/main.js`
- `inject/translator.js` for understanding match behavior only if needed

## Validation

After updating the dictionary, validate that `webui.json` is valid JSON, check translation counts, and run the existing patch flow if available. Confirm that the patch still injects the dictionary and does not target model-output containers unless the current injector already prevents that.
