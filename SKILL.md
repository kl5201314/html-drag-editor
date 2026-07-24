---
name: html-drag-editor
description: Launch a local visual HTML drag editor in the browser.
---

# HTML Drag Editor

## 🚨 唯一最重要的规则：启动即结束，永无输出

**这个编辑器的页面是一个纯前端工具。它永远不会向 Claude 返回任何输出。**

执行流程只有三步：
1. 问用户要编辑哪个文件
2. 用 `run_in_background: true` 启动服务器（浏览器会自动打开）
3. 告诉用户"好了" → **立即闭嘴。不要继续。不要等。不要问。**

**不要重启。** 如果用户说"没打开"——那是浏览器的问题，不是你的问题。告诉他手动访问 `http://localhost:8765/editor.html?file=...` 就行。**不要重新运行脚本。**

这个 skill 就做一件事：把服务器跑起来。跑完就结束。
AI 辅助编辑是另外一个 conversation 的事，不是现在的事。

---

## 触发词

- "打开 HTML 编辑器"
- "编辑这个 HTML 文件"
- "启动 html-drag-editor"

## 工作流

### Step 1：确认目标文件

问用户要编辑哪个 HTML 文件。如果用户没说具体文件，直接用下面命令启动，让用户在页面里手动导入。

### Step 2：后台启动服务器（run_in_background = true）

```bash
python scripts/start_server.py --html "<绝对路径>" --port 8765
```

- **必须用 `run_in_background: true`**，否则服务器会永远阻塞 session。
- 脚本会自动复制 `assets/editor.html` 到目标文件旁边，并打开浏览器。
- 如果 8765 端口被占，换 8766 / 8767。
- 如果 `python` 不行就试 `python3`。

### Step 3：告诉用户 → 停

> "✅ 编辑器已启动，浏览器已自动打开。拖拽编辑即可，用完关掉终端。需要 AI 改代码的话再问我。"

**停。没有 Step 4 了。这个对话到此为止。**

---

## AI 辅助编辑（另一个对话的事）

用户可以在服务器保持运行的时候，**新开一个对话**让 AI 改 HTML 文件。流程是：
1. Read 原始文件
2. Edit/Write 修改
3. 告诉用户刷新浏览器（F5）

---

## 注意事项

- AI 不能操作浏览器 DOM，也不要去试
- "保存到原文件"只在 Chrome/Edge 的 File System Access API 下有效
- 目标文件叫 `editor.html` 时会被自动重命名为 `_target.html` 避免冲突
- `data-edit-id` 是编辑器注入的，导出时会自动清除
