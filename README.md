# HTML Drag Editor 🎨 — AI 驱动的可视化原型工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**用自然语言描述界面 → AI 生成/修改 HTML → 拖拽微调 → AI 再改 → 循环直到满意。**

这是一个给**产品经理、设计师、开发者**用的快速原型工具。核心工作流是 **AI ↔ 可视化拖拽的反复迭代**：

```
你提需求 → AI 改 HTML → 保存 → 刷新页面 → 你拖拽调整 → AI 再改 → 循环
```

> ⚠️ **项目状态：早期开发阶段。**
> 这是一个实验性质的工具，核心流程走得通，但还有很多粗糙的地方（见下方[已知问题](#已知问题)）。欢迎试用和提 issue。

---

## 目录

- [这个工具解决什么问题](#这个工具解决什么问题)
- [核心工作流](#核心工作流)
- [快速开始](#快速开始)
- [场景示例](#场景示例)
- [安装为 Claude Code Skill](#安装为-claude-code-skill)
- [项目结构](#项目结构)
- [技术原理](#技术原理)
- [已知问题](#已知问题)
- [路线图](#路线图)
- [License](#license)

---

## 这个工具解决什么问题

做产品原型时，常见的痛苦：

| 问题 | 这个工具的做法 |
|------|---------------|
| 改布局要反复改代码 | 拖拽移动就行，不用写代码 |
| 改样式要查 CSS | 直接跟 AI 说"标题改蓝色，大一点" |
| AI 生成的一次性 HTML 很难微调 | 生成后拖拽微调，调完还能继续让 AI 改 |
| 原型工具太重量级（Figma / Sketch） | 一个 HTML 文件 + 一个 Python 脚本就够了 |

**一句话：让 AI 写 HTML，你拖拽微调，再让 AI 继续改——循环直到满意。**

---

## What Problem Does This Solve

| Problem | Solution |
|---------|----------|
| Changing layout requires editing code | Just drag elements with mouse |
| Styling requires writing CSS | Tell the AI "make the title blue and bigger" |
| AI-generated HTML is hard to fine-tune | Drag to adjust, then ask AI for more changes |
| Prototyping tools are heavy (Figma / Sketch) | One HTML file + one Python script is all you need |

**In one sentence: AI writes the HTML, you drag to fine-tune, AI iterates — loop until done.**

---

## 核心工作流

```
┌──────────────────────────────────────────────────────────┐
│                  迭代循环                                 │
│                                                          │
│  你 ←─── AI 修改 HTML ←─── 你反馈需求                     │
│   ↓                        ↑                              │
│  AI 保存文件                │                              │
│   ↓                        │                              │
│  你点"刷新页面"  ──────────┘                              │
│   ↓                                                        │
│  你看效果、拖拽微调                                         │
│   ↓                                                        │
│  你提出新需求 ──────────────────────────────────────────→   │
└──────────────────────────────────────────────────────────┘
```

### 详细步骤

#### 第 1 步：用 Claude Code 启动编辑器

在 Claude Code 中说：

> "打开 HTML 编辑器，编辑我桌面上的 index.html"

Claude 会自动启动本地服务器，打开浏览器，加载你的文件。

#### 第 2 步：让 Claude 修改 HTML

你跟 Claude 说：

> "把标题改成'智能家居控制台'，加一个蓝色背景的卡片区域放三个设备状态"

Claude 会直接修改磁盘上的 `index.html` 文件并保存。

#### 第 3 步：刷新网页查看效果

在编辑器网页中点击 **"刷新页面"** 按钮（或者按 F5），Claude 刚才的修改就加载进来了。

#### 第 4 步：拖拽微调

点击 **"进入修改模式"**，然后：

- 点击选中任何元素
- 拖拽移动位置
- Ctrl+Z 撤销 / Ctrl+Shift+Z 重做

#### 第 5 步：回到 AI 继续迭代

拖拽完了，回到 Claude Code 继续说：

> "把设备卡片改成两列布局，加一个折线图占位区域"

Claude 再次修改文件，你再**刷新 → 拖拽 → 提需求**，循环直到满意。

---

## The Core Workflow

```
You request → AI edits HTML → saves to disk → you click "刷新页面" 
→ you drag elements → you request more changes → AI edits again → loop
```

### Step-by-step

1. **Launch** — Tell Claude Code "open the HTML editor with my file"
2. **AI edits** — Describe what you want ("change the hero title, add a pricing section")
3. **Refresh** — Click the refresh button in the editor to see AI's changes
4. **Drag** — Switch to edit mode, drag elements to fine-tune layout
5. **Repeat** — Go back to Claude, ask for more changes, rinse and repeat

---

## 快速开始

### 前置条件

- **Python 3.8+**（标准库即可，无需 pip install）
- 现代浏览器（Chrome / Edge / Firefox / Safari）
- 可选：[Claude Code](https://claude.ai/code)（获得最佳 AI 迭代体验）

### 直接使用（不依赖 Claude Code）

```bash
# 下载
git clone https://github.com/YOUR_USERNAME/html-drag-editor.git
cd html-drag-editor

# 启动编辑器，加载你的 HTML 文件
python scripts/start_server.py --html /path/to/your/page.html --port 8765
```

浏览器会自动打开 `http://localhost:8765/editor.html?file=page.html`。

### 作为 Claude Code Skill 使用

安装到 `~/.claude/skills/html-drag-editor/`：

```bash
cp -r html-drag-editor ~/.claude/skills/html-drag-editor
```

然后在 Claude Code 中说：

> "打开 HTML 编辑器"
> "启动 html-drag-editor"
> "编辑这个 HTML 文件"

---

## 场景示例

### 场景：产品经理快速搭建仪表盘原型

1. **Claude Code**："创建一个三卡片的监控仪表盘，深色主题"
   → Claude 生成 HTML 并保存

2. **点"刷新页面"** → 看到生成的仪表盘

3. **进入修改模式** → 把卡片顺序拖拽调整

4. **Claude Code**："每个卡片加一个图标和状态指示灯"
   → Claude 修改文件，你刷新看到更新

5. **拖拽** → 微调位置 → **再提需求** → **循环**

全程不需要写一行代码。

### Scenario: PM Rapid-Prototyping a Dashboard

1. **Claude Code**: "Create a 3-card monitoring dashboard, dark theme"
2. **Click refresh** → see the generated dashboard
3. **Enter edit mode** → drag cards to reorder
4. **Claude Code**: "Add an icon and status indicator to each card"
5. **Drag to fine-tune** → **request more** → **loop**

Zero code written.

---

## 安装为 Claude Code Skill

### Manual

```bash
git clone https://github.com/YOUR_USERNAME/html-drag-editor.git ~/.claude/skills/html-drag-editor
```

### Auto (via skill-creator)

```bash
skill-creator create-cc-skill --scope user --name html-drag-editor --description "Visual HTML drag editor for Claude Code"
```

---

## 项目结构

```
html-drag-editor/
├── SKILL.md                 # Claude Code skill 指令
├── README.md                # 本文件
├── LICENSE                  # MIT License
├── .gitignore
├── assets/
│   └── editor.html          # 单文件拖拽编辑器（HTML + CSS + JS）
└── scripts/
    └── start_server.py      # 本地 HTTP 服务器 + /api/save 保存 API
```

---

## 技术原理

```
┌─────────────────────────────────────────────┐
│  Claude Code (AI 对话)                       │
│  你用自然语言提需求 → AI 直接修改磁盘 HTML    │
└──────────────────────┬──────────────────────┘
                       │ Read / Edit / Write
                       ▼
┌─────────────────────────────────────────────┐
│  磁盘上的 HTML 文件                           │
│  AI 写完 → 你点"刷新页面" → 编辑器重新加载     │
└──────────────────────┬──────────────────────┘
                       │ serve via HTTP
                       ▼
┌─────────────────────────────────────────────┐
│  浏览器中的编辑器                              │
│  ┌─────────────────────────────────────────┐ │
│  │  Toolbar: 导入 │ 修改模式 │ 导出 │ 保存 │ │
│  ├─────────────────────────────────────────┤ │
│  │  <iframe> 预览你的 HTML                  │ │
│  │  点击选中 → 拖拽移动                     │ │
│  │  Ctrl+Z 撤销 / Ctrl+Shift+Z 重做        │ │
│  ├─────────────────────────────────────────┤ │
│  │  属性面板: 显示选中元素的 edit-id 和偏移  │ │
│  └─────────────────────────────────────────┘ │
│         │                                     │
│         ▼                                     │
│  POST /api/save → 服务器直接覆写磁盘文件      │
└─────────────────────────────────────────────┘
```

### 保存机制

- **Server Mode**（通过 `?file=` 加载）：点击"保存到原文件" → `POST /api/save` → 服务器直接覆写 `--html` 指定的原始文件。**没有弹窗、没有另存为。**
- **Standalone Mode**（双击打开/手动导入）：使用浏览器 File System Access API 或触发下载兜底。

### 安全性

- `/api/save` 只允许保存启动时指定的那一个文件名，其他请求返回 403。

---

## 已知问题

这个项目处于**早期开发阶段**，以下问题已知：

| 问题 | 说明 |
|------|------|
| **拖拽精度有限** | 目前只支持 `translate` 变换，不支持嵌套元素内的精确拖动 |
| **刷新后变换丢失** | "刷新页面"会重新加载原始 HTML，之前的拖拽变换会重置。建议导出后再刷新 |
| **撤销栈跨刷新不保留** | 撤销/重做仅在当前会话有效 |
| **仅支持同层拖拽** | 不能改变元素的层级关系（不能把 A 拖到 B 里面） |
| **属性面板只读** | 目前只显示元素 id 和偏移量，不支持编辑 CSS 属性 |
| **移动端支持待完善** | 触摸事件已基本可用但未经充分测试 |
| **大文件性能** | 超大 HTML 文件可能影响编辑流畅度 |
| **Firefox 兼容** | 保存到原文件的 File System Access API 在 Firefox 不支持，但 `/api/save` 路径不受影响 |

### Known Issues

This project is in **early development**. Known limitations include:

| Issue | Description |
|-------|-------------|
| **Drag accuracy** | Only `translate` transforms; no precise dragging inside nested elements |
| **Transforms lost on refresh** | "Refresh" reloads from source; drag positions reset. Export before refresh |
| **Undo stack resets** | Undo/redo only works within current session |
| **Sibling-level only** | Cannot change element parent-child hierarchy via drag |
| **Read-only property panel** | Shows element ID and offset only; no CSS editing |
| **Mobile support** | Touch events basic but not thoroughly tested |
| **Large file performance** | May lag with very large HTML files |
| **Firefox save** | File System Access API unsupported in Firefox, but `/api/save` works fine |

---

## 路线图

- [ ] 属性面板支持编辑 CSS（宽高、颜色、边距等）
- [ ] 更精确的拖拽吸附和对齐线
- [ ] 元素层级拖拽（改变父容器）
- [ ] 撤销栈支持跨刷新持久化
- [ ] 撤销/重做历史面板
- [ ] 多页面支持（SPA 导航编辑）
- [ ] 移动端触控优化
- [ ] 组件库面板（从预设组件库拖入新元素）

---

## License

[MIT](LICENSE) © 2024

---

*Made for product managers who want to prototype without wrestling with code.*
*为不想跟代码搏斗的产品经理而生。*
