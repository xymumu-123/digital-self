# 使用指南

## 前置条件

- [Claude Code](https://claude.ai/code) 已安装
- Python 3.9+（用于数据处理工具）

## 安装

### 方式一：克隆到项目目录

```bash
git clone https://github.com/你的用户名/digital-self.git
```

将克隆下来的文件夹放到你的项目目录中。

### 方式二：手动安装

将 `digital-self` 文件夹复制到你的项目中：

```
你的项目/
├── skills/
│   └── digital-self/    ← 放在这里
├── CLAUDE.md
└── ...
```

## 快速开始

### 1. 蒸馏自己

在 Claude Code 中对话：

```
/digital-self
```

然后说"蒸馏我自己"，按照引导提供你的资料：

- **微信聊天记录**：导出后放到 `raw/chat/wechat/`
- **AI对话记录**：导出后放到 `raw/chat/ai_dialogues/`
- **个人笔记**：放到 `raw/notes/`
- **写过的东西**：放到 `raw/writings/`
- **工作资料**：放到 `raw/work/`
- **个人背景**：放到 `raw/personal/`

系统会自动分析你的资料，生成灵魂层（`soul/`）和记忆层（`wiki/`）。

### 2. 日常使用

激活数字副本：

```
/digital-self
```

然后直接对话：

- "用我的方式回答这个问题"
- "我之前学过什么关于XXX的"
- "帮我回忆一下XXX"
- "和我聊天"

### 3. 导入新资料

当有新资料时，直接说：

- "我有新资料"
- "导入这个"
- "添加到知识库"

系统会自动分类存入 `raw/` 并更新记忆层。

### 4. 查询知识

- "我之前学过什么"
- "我对XXX的看法是什么"
- "我写过什么关于XXX的"

### 5. 维护

- "检查知识库" — 执行 Wiki Lint，检查矛盾和孤立页面
- "更新我的灵魂" — 重新分析资料，更新灵魂层
- "退出" — 退出数字副本模式

## 目录结构

```
digital-self/
├── SKILL.md              # 技能定义文件（Claude Code 入口）
├── README.md             # 项目说明
├── USAGE.md              # 本文件
├── raw/                  # 原始资料（你的真实数据）
│   ├── chat/             # 聊天记录
│   │   ├── wechat/       # 微信聊天记录
│   │   └── ai_dialogues/ # AI对话记录
│   ├── notes/            # 笔记
│   ├── writings/         # 写作作品
│   ├── work/             # 工作资料
│   ├── personal/         # 个人背景
│   └── interests/        # 兴趣资料
├── soul/                 # 灵魂层（自动生成）
│   ├── SKILL.md          # 完整灵魂层（整合版）
│   ├── self.md           # 自我记忆
│   ├── persona.md        # 人格模型
│   └── thinking-framework.md  # 思维框架
├── wiki/                 # 记忆层（自动生成）
│   ├── index.md          # 内容索引
│   ├── log.md            # 操作日志
│   ├── sources/          # 来源摘要
│   ├── entities/         # 实体页
│   ├── concepts/         # 概念页
│   └── overview/         # 总览
└── schema/               # 配置和工具
    ├── tools/            # Python脚本
    │   ├── wechat_parser.py        # 微信聊天记录解析
    │   ├── ai_dialogue_parser.py   # AI对话记录解析
    │   └── ...
    ├── prompts/          # 提示词模板
    └── references/       # 参考文档
```

## 数据处理工具

### 微信聊天记录解析

```bash
python schema/tools/wechat_parser.py <输入文件> <输出目录>
```

### AI对话记录解析

```bash
python schema/tools/ai_dialogue_parser.py <输入文件> <输出目录>
```

### JSON转Markdown

```bash
python schema/tools/json_to_markdown.py <输入文件> <输出目录>
```

## 灵魂层模板

`soul/` 目录下的文件包含待填写的模板。蒸馏过程会自动填充这些内容。你也可以手动编辑：

- **self.md**：你的事实性自我认知（身份、价值观、经历）
- **persona.md**：你的人格模型（说话风格、情感模式、行为特征）
- **thinking-framework.md**：你的思维框架（心智模型、决策启发式）

## 注意事项

- `raw/` 目录包含你的个人数据，**不要上传到公开仓库**
- 如果要公开分享，只上传框架（`soul/` 模板 + `schema/` + `wiki/` 模板）
- 灵魂层的质量取决于你提供的资料的丰富程度
- 建议定期补充新资料，保持数字副本的时效性

## 常见问题

**Q: 数字副本能完全替代我吗？**

A: 不能。它基于你提供的资料推断，缺乏面对面交流、日常行为等更立体的信息。它是你的一面镜子，不是你的替代品。

**Q: 资料越多越好吗？**

A: 是的。微信聊天记录是最有价值的来源，因为它包含你和真人交流时的真实表达方式。AI对话记录只能反映你和AI说话的方式。

**Q: 灵魂层可以手动修改吗？**

A: 可以。你可以直接编辑 `soul/` 下的任何文件。也可以对数字副本说"不对，我不会这样说"，它会自动纠正。

**Q: 数据安全吗？**

A: 所有数据都在本地，不会上传到任何服务器。但要注意不要将 `raw/` 目录推送到公开的 GitHub 仓库。
