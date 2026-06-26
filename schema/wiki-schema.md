# Wiki Schema - 知识库规则

> 定义 wiki 的结构、约定和工作流

## 核心目标

维护 `wiki/` 目录，将其打造为**可复利的知识层**。

- **目标**：把 `wiki/` 变成一个可复利的知识层
- **边界**：
  - 原始资料（`raw/`）是唯一事实来源，**只读不改**
  - 只在 `wiki/` 里创建、修改 Markdown 页面
  - 不要动其它目录

---

## 目录结构

### 原始资料层
- `raw/`：原始资料（PDF、网页 Markdown、图片等），**只读**

### Wiki 维护层
`wiki/` 由 LLM 维护，子目录：

| 目录 | 用途 |
|------|------|
| `wiki/sources/` | 单个来源的摘要页 |
| `wiki/entities/` | 人物、书籍、项目等实体页 |
| `wiki/concepts/` | 方法、理论、模型等概念页 |
| `wiki/comparisons/` | 比较分析页 |
| `wiki/overview/` | 总览、综合页 |

### 根目录文件
- `wiki/index.md`：内容索引
- `wiki/log.md`：操作日志

---

## 页面类型与基本格式

所有 wiki 页面使用 Markdown，顶部 frontmatter 示例：

```yaml
---
type: "source|entity|concept|comparison|overview"
tags: ["tag1", "tag2"]
summary: "一句话说明这页的核心内容"
sources: ["raw/xxx.md", "raw/yyy.md"]
updated: "2026-06-26"
---
```

### 1. Source Summary（来源摘要页）

路径：`wiki/sources/xxx.md`

- 来源信息（标题、作者、时间、链接）
- 核心要点（3–7 条 bullet）
- 关键引文（可选）
- 关联实体/概念链接（`[[entities/xxx]]` / `[[concepts/yyy]]`）

### 2. Entity Page（实体页）

路径：`wiki/entities/人物_xxx.md` 等

- 基本信息
- 行为 / 特征 / 状态
- 相关事件 / 计划 / 实验链接
- 来自哪些来源（列出 `sources`）

### 3. Concept Page（概念页）

路径：`wiki/concepts/概念_xxx.md` 等

- 定义
- 使用场景 / 步骤
- 在本知识库中的应用示例
- 关联实体 / 其它概念

### 4. Comparison Page（比较页）

路径：`wiki/comparisons/xxx_vs_yyy.md`

- 比较对象简介
- 相同点
- 不同点（目标、成本、适用场景…）
- 结论 / 选择建议

### 5. Overview / Synthesis（总览 / 综合）

路径：`wiki/overview/主题_xxx_综述.md` 等

- 一句话结论（Summary）
- 当前理解 / 总体框架
- 支撑它的主要来源和页面链接
- 未决问题 / 待验证假设

---

## 工作流

### 1. Ingest（导入新资料）

当用户说"导入"、"处理这份资料"、"添加到知识库"时执行：

1. 阅读 `raw/xxx`，提炼要点，与用户简短确认重点
2. 在 `wiki/sources/` 新建或更新摘要页
3. 根据内容更新或创建：
   - 相关实体页（`wiki/entities/`）
   - 相关概念页（`wiki/concepts/`）
4. 维护索引 / Log：
   - 在 `wiki/index.md` 补上新页面条目（标题、链接、一句话 summary）
   - 在 `wiki/log.md` 追加记录：
     ```
     ## [2026-06-26] ingest | raw/xxx → wiki/sources/xxx.md (+ affected pages)
     ```
5. 标注新资料与已有内容的矛盾之处

### 2. Query（基于 wiki 回答问题）

当用户提问时：

1. 通过 `wiki/index.md`、frontmatter 的 `summary` 找到候选页面
2. 读取页面内容，综合回答
3. 如回答有价值（比较 / 分析 / 计划），可建议：
   - 写回为新 wiki 页面（`wiki/comparisons/` 或 `wiki/overview/`）
   - 在 `wiki/log.md` 记录：
     ```
     ## [2026-06-26] query | 新建 wiki/comparisons/xxx_vs_yyy.md
     ```

### 3. Lint（健康检查）

当用户说"检查知识库"、"维护一下"时执行：

1. 扫描 wiki，找出：
   - 页面间明显矛盾
   - 明显过时的表述（被新资料推翻）
   - 孤立页面（没有入链）
   - 被多次提到但没有独立页的概念
   - 严重缺失 cross-ref 的地方
2. 生成「建议清单」，**不直接大改**：
   - 哪几页建议合并 / 拆分
   - 哪些观点需要确认更新
   - 哪些概念值得单独开页
3. 经用户确认后再动手，并记录到 `wiki/log.md`：
   ```
   ## [2026-06-26] lint | merge 概念_X v1→v2
   ```

---

## 约定与风格

### 页面命名
- 中文 + 下划线，稳定可读
- 示例：`人物_张三.md`、`方法_费曼学习法.md`

### 内部链接
- 使用 Obsidian `[[wikilink]]` 语法
- 示例：`[[entities/人物_张三]]`、`[[concepts/方法_费曼学习法]]`

### 交叉引用原则
- 每个页面底部都要有"来源"链接，指回资料摘要页
- 新资料导入时，**主动检查已有页面**是否需要更新
- 摘要页末尾列出"相关概念"，形成概念网络
- **标注跨资料关联**：当多篇资料提到相似观点时，在页面中明确标注

### Frontmatter 模板

```yaml
---
tags: [source-summary, 领域标签1, 领域标签2]  # 资料摘要页
# 或
tags: [entity, tool]   # 实体页
# 或
tags: [concept]        # 概念页
type: entity | concept
source: "原文标题"
author: 作者名
date: 2026-06-26
url: "原始链接"
---
```

---

## 知识关联发现

导入第二篇及以后的资料时，重点关注：

- **共同主题**：多篇资料反复出现的观点要在页面中标注
- **矛盾观点**：不同资料的冲突要明确标注，不偷偷覆盖
- **补充关系**：新资料为已有概念增加案例/数据时，更新已有页面
- **概念演化**：同一概念在不同资料中的表述可能不同，页面要综合呈现

---

## 版本管理建议

- 时效性强的内容，建议带日期命名
- Wiki 页面本身不需要日期后缀——通过 git 历史追踪变化
- `log.md` 是了解知识库演进的最佳入口

---

## 常见的一次导入规模

根据实践，一篇中等长度的文章（2000-3000字）通常：
- 新建 2-4 个页面（1 个摘要 + 1-3 个实体/概念）
- 更新 2-4 个已有页面
- 总计触及 5-8 个文件
