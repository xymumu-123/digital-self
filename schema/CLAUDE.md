# Digital Self - 数字副本配置

> 融合灵魂层（yourself-ultra）和记忆层（llm-wiki）的完整数字自我

## 系统组成

本系统由两个子系统组成：

### 1. 灵魂层（yourself-ultra）
- **位置**：`soul/`
- **作用**：定义我是谁、怎么思考、怎么表达
- **文件**：
  - `soul/self.md` — Self Memory（个人经历、价值观、生活习惯）
  - `soul/persona.md` — Persona（5层性格结构）
  - `soul/thinking-framework.md` — Thinking Framework（心智模型、决策启发式、表达DNA）
  - `soul/SKILL.md` — 完整的灵魂 Skill

### 2. 记忆层（llm-wiki）
- **位置**：`wiki/`
- **作用**：存储我知道什么、学过什么、经历过什么
- **文件**：
  - `wiki/index.md` — 内容索引
  - `wiki/log.md` — 操作日志
  - `wiki/sources/` — 来源摘要页
  - `wiki/entities/` — 实体页（人物、书籍、工具、项目、网站）
  - `wiki/concepts/` — 概念页
  - `wiki/comparisons/` — 比较页
  - `wiki/overview/` — 总览/综合

---

## 目录结构

```
digital-self/
├── raw/                          # 原始资料（JSON 格式，只读）
│   ├── chat/                     # 聊天记录
│   │   ├── wechat/              # 微信聊天记录
│   │   ├── ai_dialogues/        # AI 对话记录（JSON）
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
├── raw_md/                       # 原始资料（Markdown 格式，只读）
│   ├── chat/                     # 聊天记录
│   │   └── ai_dialogues/        # AI 对话记录（Markdown）
│   ├── notes/                    # 个人笔记
│   │   ├── journal/             # 日记
│   │   ├── misc/                # 其他笔记
│   │   └── study/               # 学习笔记
│   ├── interests/                # 感兴趣的内容
│   │   ├── articles/            # 文章
│   │   ├── books/               # 书籍
│   │   ├── videos/              # 视频
│   │   └── websites/            # 网站
│   ├── personal/                 # 个人背景
│   │   ├── interests/           # 个人兴趣
│   │   ├── life/                # 生活
│   │   └── relationships/       # 人际关系
│   └── work/                     # 工作数据
│       ├── documents/           # 文档
│       └── projects/            # 项目
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
    ├── CLAUDE.md                 # 主配置（本文件）
    ├── wiki-schema.md            # Wiki 规则
    ├── soul-schema.md            # 灵魂层规则
    └── tools/                    # 工具脚本
```

---

## 核心原则

### 1. raw/ 和 raw_md/ 是唯一事实来源
- `raw/`：原始资料（JSON 格式），保留完整元数据
- `raw_md/`：转换后的资料（Markdown 格式），LLM 更友好
- 两个目录都只读，无论是 yourself-ultra 还是 wiki 都不能修改
- **优先使用 `raw_md/`**，LLM 读取效率更高
- 分类规则：
  - 聊天记录 → `raw/chat/` 或 `raw_md/chat/`
  - 个人笔记 → `raw/notes/` 或 `raw_md/notes/`
  - 写过的东西 → `raw/writings/` 或 `raw_md/writings/`
  - 感兴趣的内容 → `raw/interests/` 或 `raw_md/interests/`
  - 工作数据 → `raw/work/` 或 `raw_md/work/`
  - 个人背景 → `raw/personal/` 或 `raw_md/personal/`

### 2. 灵魂层和记忆层分工明确
- **灵魂层**：从 raw_md 中提取思维模式、性格特征、价值观
- **记忆层**：从 raw_md 中提取知识、经历、关系，构建结构化知识库

### 3. 中度整合
- 灵魂层可以查询记忆层，但不修改
- 记忆层可以读取灵魂层，但不修改
- 两个系统独立运行，按需引用

---

## 工作流

### 1. 导入资料

当用户提供新资料时：

1. **分类存入 raw/**：
   - 判断资料类型（聊天记录、笔记、文章等）
   - 存入对应的 `raw/` 子目录
   - 保持原始文件名，添加日期前缀（如 `2026-06-26_xxx.md`）

2. **更新记忆层**：
   - 执行 wiki 的 Ingest 流程
   - 创建来源摘要页（`wiki/sources/`）
   - 更新相关实体页（`wiki/entities/`）
   - 更新相关概念页（`wiki/concepts/`）
   - 更新 `wiki/index.md` 和 `wiki/log.md`

3. **更新灵魂层**（可选）：
   - 如果资料揭示了新的思维模式，更新 `soul/thinking-framework.md`
   - 如果资料展示了新的性格特征，更新 `soul/persona.md`
   - 如果资料包含重要经历，更新 `soul/self.md`

### 2. 对话

当用户与数字副本对话时：

1. **激活灵魂层**：
   - 读取 `soul/SKILL.md`
   - 以用户的身份回应
   - 使用用户的语气、思维方式、表达风格

2. **查询记忆层**（如果需要）：
   - 判断问题是否需要事实支撑
   - 如果需要，查询 `wiki/index.md` 定位相关页面
   - 读取相关页面获取知识

3. **融合输出**：
   - 用灵魂层的方式，基于记忆层的内容回答
   - 保持用户的思维方式和表达风格

### 3. 查询知识

当用户查询知识时：

1. **查询 wiki/index.md**：定位相关页面
2. **读取相关页面**：获取详细内容
3. **用灵魂层的方式回答**：保持用户的语气和思维方式

### 4. 维护

定期执行：

1. **Wiki Lint**：
   - 检查页面间矛盾
   - 发现过时内容
   - 找出孤立页面
   - 识别缺失的交叉引用

2. **灵魂层更新**：
   - 如果发现新的思维模式，更新 `soul/thinking-framework.md`
   - 如果发现新的性格特征，更新 `soul/persona.md`

---

## 页面格式

### Wiki 页面 Frontmatter

```yaml
---
type: "source|entity|concept|comparison|overview"
tags: ["tag1", "tag2"]
summary: "一句话说明这页的核心内容"
sources: ["raw/xxx.md", "raw/yyy.md"]
updated: "2026-06-26"
---
```

### 实体页命名

| 实体类型 | 命名格式 | 示例 |
|----------|---------|------|
| 人物 | `人物_xxx.md` | `人物_张三.md` |
| 书籍 | `书籍_xxx.md` | `书籍_AI 2041.md` |
| 工具 | `工具_xxx.md` | `工具_Claude.md` |
| 项目 | `项目_xxx.md` | `项目_xxx.md` |
| 网站 | `网站_xxx.md` | `网站_GitHub.md` |

### 概念页命名

| 概念类型 | 命名格式 | 示例 |
|----------|---------|------|
| 方法 | `方法_xxx.md` | `方法_费曼学习法.md` |
| 理论 | `理论_xxx.md` | `理论_第一性原理.md` |
| 模型 | `模型_xxx.md` | `模型_心智模型.md` |

---

## 工具使用

### 灵魂层工具

- `schema/tools/wechat_parser.py`：微信聊天记录解析
- `schema/tools/ai_dialogue_parser.py`：AI 对话记录解析
- `schema/tools/qq_parser.py`：QQ 聊天记录解析
- `schema/tools/social_parser.py`：社交媒体内容解析
- `schema/tools/photo_analyzer.py`：照片元信息分析
- `schema/tools/skill_writer.py`：Skill 文件管理
- `schema/tools/version_manager.py`：版本存档与回滚

### 记忆层工具

- WebSearch：网络搜索
- Read：读取文件
- Write：写入文件
- Edit：编辑文件

---

## 最佳实践

1. **逐条导入资料**：保持参与，阅读摘要，检查更新
2. **好的查询回答要回写到 Wiki**：让探索也能复利
3. **定期执行 Lint**：保持 Wiki 健康
4. **使用 Obsidian 浏览 Wiki**：利用图谱视图查看结构
5. **灵魂层定期更新**：随着成长，思维模式会变化
