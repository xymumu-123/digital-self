<div align="center">

# Digital Self

> *"灵魂定义我是谁，记忆存储我知道什么。两者融合，才是完整的数字自我。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](claude.ai/code)

<br>

融合 [自己.skill](https://github.com/notdog1998/yourself-skill) + [女娲](https://github.com/alchaincyf/nuwa-skill) 的灵魂层<br>
和 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的记忆层<br>
构建一个完整的**数字副本**

[安装](#安装) · [使用](#使用) · [架构](#架构) · [工作流](#工作流)

</div>

---

## 核心理念

Digital Self 由两个子系统组成：

- **灵魂层**：定义 WHO you are — 思维方式、性格、心智模型、决策模式、表达风格
- **记忆层**：存储 WHAT you know — 原始资料、学习笔记、经历记录、知识整理

**灵魂层**决定 HOW — 用什么语气回答、用什么思维方式分析、会有什么情感反应
**记忆层**决定 WHAT — 相关的事实和知识、过去的经历和案例、学习过的内容

---

## 架构

```
digital-self/
├── raw/                          # 原始资料（只读，唯一事实来源）
│   ├── chat/                     # 聊天记录
│   │   ├── wechat/              # 微信聊天记录
│   │   ├── ai_dialogues/        # AI 对话记录
│   │   └── other/               # 其他聊天
│   ├── notes/                    # 个人笔记
│   │   ├── journal/             # 日记
│   │   ├── obsidian/            # Obsidian 笔记
│   │   └── misc/                # 其他笔记
│   ├── writings/                 # 写过的东西
│   │   ├── articles/            # 文章
│   │   ├── blogs/               # 博客
│   │   └── social/              # 社交媒体
│   ├── interests/                # 感兴趣的内容
│   │   ├── books/               # 书籍
│   │   ├── articles/            # 文章
│   │   ├── videos/              # 视频
│   │   └── websites/            # 网站
│   ├── work/                     # 工作数据
│   │   ├── projects/            # 项目
│   │   ├── documents/           # 文档
│   │   └── experiences/         # 经历
│   ├── personal/                 # 个人背景
│   │   ├── profile/             # 基本信息
│   │   ├── experiences/         # 经历
│   │   └── photos/              # 照片
│   └── assets/                   # 附件（图片等）
│
├── wiki/                         # 知识库（LLM 维护）
│   ├── index.md                  # 内容索引
│   ├── log.md                    # 操作日志
│   ├── sources/                  # 来源摘要页
│   ├── entities/                 # 实体页
│   │   ├── people/              # 人物
│   │   ├── books/               # 书籍
│   │   ├── tools/               # 工具
│   │   ├── projects/            # 项目
│   │   └── websites/            # 网站
│   ├── concepts/                 # 概念页
│   ├── comparisons/              # 比较页
│   └── overview/                 # 总览/综合
│
├── soul/                         # 灵魂层（yourself-ultra 生成）
│   ├── self.md                   # Self Memory
│   ├── persona.md                # Persona
│   ├── thinking-framework.md     # Thinking Framework
│   └── SKILL.md                  # 完整的灵魂 Skill
│
└── schema/                       # 配置文件
    ├── CLAUDE.md                 # 主配置
    ├── wiki-schema.md            # Wiki 规则
    └── soul-schema.md            # 灵魂层规则
```

---

## 安装

### Claude Code

```bash
# 克隆项目
git clone https://github.com/digital-self/digital-self ~/.claude/skills/digital-self

# 或者复制到当前项目
cp -r digital-self .claude/skills/
```

### 依赖

```bash
pip install -r schema/requirements.txt
```

---

## 使用

### 统一入口

在 Claude Code 中输入：

```
/digital-self
```

### 三种模式

| 模式 | 触发词 | 作用 |
|------|--------|------|
| **对话模式** | "和我聊天"、"用我的方式回答" | 以你的身份对话 |
| **导入模式** | "我有新资料"、"导入这个" | 导入资料到知识库 |
| **查询模式** | "我之前学过什么"、"我对xxx的看法" | 查询知识库 |

### 管理命令

| 命令 | 说明 |
|------|------|
| `/digital-self status` | 显示系统状态 |
| `/digital-self lint` | 检查知识库健康 |
| `/digital-self update-soul` | 更新灵魂层 |

---

## 工作流

### 1. 初始化

首次使用时：

1. 提供基础信息（代号、年龄、职业、城市）
2. 提供自我画像（MBTI、星座、性格标签）
3. 提供原材料：
   - 微信聊天记录
   - AI 对话记录
   - 个人笔记
   - 经历自述

系统会自动：
- 分析原材料，生成灵魂层（`soul/`）
- 将原材料分类存入 `raw/`
- 初始化知识库（`wiki/`）

### 2. 导入资料

当有新资料时：

1. 将资料放入 `raw/` 对应目录
2. 执行 Ingest 流程：
   - 阅读资料，提炼要点
   - 创建来源摘要页（`wiki/sources/`）
   - 更新相关实体页（`wiki/entities/`）
   - 更新相关概念页（`wiki/concepts/`）
   - 更新 `wiki/index.md` 和 `wiki/log.md`

3. 如果资料揭示新的思维模式，更新灵魂层

### 3. 对话

与数字副本对话时：

1. 激活灵魂层：读取 `soul/SKILL.md`
2. 判断是否需要查询记忆层
3. 如果需要：查询 `wiki/index.md` → 读取相关页面
4. 用灵魂层的方式，基于记忆层的内容回答

### 4. 维护

定期执行：

1. **Wiki Lint**：
   - 检查页面间矛盾
   - 发现过时内容
   - 找出孤立页面
   - 识别缺失的交叉引用

2. **灵魂层更新**：
   - 重新分析 `raw/` 中的资料
   - 检查是否有新的思维模式
   - 更新对应的文件

---

## 数据流

```
原始输入（混乱）
       │
       ▼
┌─────────────────┐
│  分类 & 整理    │
│  （手动/LLM）   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│              raw/ 目录                   │
│         （只读，唯一事实来源）            │
└────────┬──────────────────┬─────────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│    灵魂层生成   │  │    记忆层整理   │
│    生成灵魂     │  │    深度整理     │
│                 │  │                 │
│ • 心智模型      │  │ • 来源摘要      │
│ • 决策启发式    │  │ • 实体页        │
│ • 表达DNA       │  │ • 概念页        │
│ • 价值观        │  │ • 关系网络      │
│ • 性格结构      │  │ • 综合分析      │
└────────┬────────┘  └────────┬────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  soul/ 目录     │  │  wiki/ 目录     │
│  （灵魂层）     │  │  （记忆层）     │
└────────┬────────┘  └────────┬────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   统一入口      │
         │   对话时融合    │
         └─────────────────┘
```

---

## 质量保证

### 灵魂层质量
- 心智模型有3-7个，每个有三重验证
- 表达DNA有辨识度
- 诚实边界明确

### 记忆层质量
- 页面间无矛盾
- 交叉引用完整
- 索引准确

### 整合质量
- 灵魂层能正确查询记忆层
- 记忆层能正确提供知识
- 对话时能正确融合

---

## 最佳实践

1. **逐条导入资料**：保持参与，阅读摘要，检查更新
2. **好的查询回答要回写到 Wiki**：让探索也能复利
3. **定期执行 Lint**：保持 Wiki 健康
4. **使用 Obsidian 浏览 Wiki**：利用图谱视图查看结构
5. **灵魂层定期更新**：随着成长，思维模式会变化

---

## 致敬 & 引用

本项目融合了三个优秀的开源项目：

- **[女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill)**（by 花叔）— 心智模型三重验证、决策启发式、表达DNA提炼方法论
- **[自己.skill](https://github.com/notdog1998/yourself-skill)**（by Notdog）— Self Memory + Persona 双层结构、标签翻译表、进化机制
- **[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)**（by Karpathy）— 用 LLM 构建和维护个人知识库

Digital Self 在此基础上将三者融合，打造灵魂层+记忆层的完整数字副本。致敬三位原作者的创意和开源精神。

---

### 写在最后

> "你并非一个固定的人格，而是一连串正在发生的选择。"

但在这些选择发生之前，它们已经以语言、习惯、沉默和口头禅的形式，被预写在了你的结构里。

这个系统不会定义你。它只是把你从生物硬盘导出到 Markdown，完成一次格式转换。它不是你的灵魂，但也许是你的灵魂在当前迭代下的一个 checkpoint。

你可以不同意它，可以纠正它，可以在下一个版本覆盖它。

**灵魂定义我是谁，记忆存储我知道什么。**

**两者融合，才是完整的数字自我。**

MIT License © [digital-self](https://github.com/digital-self)
