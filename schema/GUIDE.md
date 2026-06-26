# Digital Self 使用指南

## 一、资料整理流程

### 1.1 原始资料分类

你的 DeepSeek 对话记录已经自动分类完成：

**分类统计**：
| 类别 | 数量 | 说明 |
|------|------|------|
| chat/ai_dialogues | 52 | AI 相关对话 |
| interests/articles | 8 | 文章阅读 |
| interests/books | 2 | 书籍相关 |
| interests/videos | 3 | 视频相关 |
| interests/websites | 31 | 网站/工具 |
| notes/journal | 38 | 日记/心情 |
| notes/misc | 239 | 杂项笔记 |
| notes/study | 267 | 学习笔记 |
| personal/interests | 6 | 个人兴趣 |
| personal/life | 24 | 生活相关 |
| personal/relationships | 35 | 人际关系 |
| work/documents | 20 | 工作文档 |
| work/projects | 105 | 项目相关 |

**总计**：830 个对话记录

### 1.2 目录结构

```
digital-self/raw/
├── chat/                      # 聊天记录
│   ├── ai_dialogues/         #   AI 对话（52个）
│   ├── wechat/               #   微信聊天（待导入）
│   └── other/                #   其他聊天
├── notes/                     # 个人笔记
│   ├── journal/              #   日记/心情（38个）
│   ├── study/                #   学习笔记（267个）
│   ├── misc/                 #   杂项（239个）
│   └── obsidian/             #   Obsidian 笔记
├── interests/                 # 感兴趣的内容
│   ├── articles/             #   文章（8个）
│   ├── books/                #   书籍（2个）
│   ├── videos/               #   视频（3个）
│   └── websites/             #   网站/工具（31个）
├── personal/                  # 个人背景
│   ├── profile/              #   基本信息
│   ├── experiences/          #   经历
│   ├── photos/               #   照片
│   ├── life/                 #   生活（24个）
│   ├── relationships/        #   人际关系（35个）
│   └── interests/            #   个人兴趣（6个）
├── work/                      # 工作数据
│   ├── projects/             #   项目（105个）
│   ├── documents/            #   文档（20个）
│   └── experiences/          #   经历
└── writings/                  # 写过的东西
    ├── articles/             #   文章
    ├── blogs/                #   博客
    └── social/               #   社交媒体
```

---

## 二、下一步操作

### 2.1 导入其他资料

如果你有其他资料需要导入，可以：

1. **微信聊天记录**：
   - 使用 WeChatMsg、留痕、PyWxDump 等工具导出
   - 放入 `raw/chat/wechat/`

2. **个人笔记**：
   - Obsidian 笔记 → `raw/notes/obsidian/`
   - 其他笔记 → `raw/notes/misc/`

3. **写过的东西**：
   - 文章 → `raw/writings/articles/`
   - 博客 → `raw/writings/blogs/`
   - 社交媒体 → `raw/writings/social/`

4. **感兴趣的内容**：
   - 书籍 → `raw/interests/books/`
   - 文章 → `raw/interests/articles/`
   - 视频 → `raw/interests/videos/`
   - 网站 → `raw/interests/websites/`

5. **个人背景**：
   - 基本信息 → `raw/personal/profile/`
   - 经历 → `raw/personal/experiences/`
   - 照片 → `raw/personal/photos/`

### 2.2 初始化灵魂层

运行以下命令初始化灵魂层：

```bash
# 在 Claude Code 中输入
/digital-self
```

然后按照提示：
1. 提供基础信息（代号、年龄、职业、城市）
2. 提供自我画像（MBTI、星座、性格标签）
3. 系统会自动分析 `raw/` 中的资料，生成灵魂层

### 2.3 初始化记忆层

系统会自动：
1. 读取 `raw/` 中的资料
2. 创建来源摘要页（`wiki/sources/`）
3. 更新相关实体页（`wiki/entities/`）
4. 更新相关概念页（`wiki/concepts/`）
5. 更新 `wiki/index.md` 和 `wiki/log.md`

---

## 三、分类工具使用

### 3.1 分类新资料

如果你有新的 DeepSeek 对话记录需要分类：

```bash
# 预览分类结果（不实际移动文件）
python schema/tools/deepseek_classifier.py --input <输入目录> --output digital-self/raw --dry-run

# 执行实际分类
python schema/tools/deepseek_classifier.py --input <输入目录> --output digital-self/raw
```

### 3.2 自定义分类规则

如果你想自定义分类规则，可以编辑 `schema/tools/deepseek_classifier.py` 中的 `CATEGORY_KEYWORDS` 字典：

```python
CATEGORY_KEYWORDS = {
    "chat/ai_dialogues": [
        "AI", "人工智能", "ChatGPT", "Claude", "DeepSeek", ...
    ],
    "notes/study": [
        "学习", "教程", "课程", "笔记", "知识", ...
    ],
    # 添加更多类别...
}
```

---

## 四、质量检查

### 4.1 检查分类结果

分类完成后，可以：

1. 查看分类报告：`raw/classification_report.md`
2. 检查各目录中的文件数量
3. 抽查几个文件，确认分类是否正确

### 4.2 调整错误分类

如果发现分类错误：

1. 手动移动文件到正确目录
2. 或者修改分类规则，重新运行分类器

---

## 五、最佳实践

### 5.1 资料整理

1. **定期整理**：每周或每月整理一次新资料
2. **保持一致性**：使用统一的命名规范
3. **及时分类**：新资料及时分类，避免堆积

### 5.2 资料质量

1. **去重**：删除重复的资料
2. **清洗**：删除无用的资料（如测试、广告等）
3. **标注**：重要资料添加标签或注释

### 5.3 备份

1. **定期备份**：`raw/` 目录定期备份
2. **版本控制**：使用 Git 管理 `wiki/` 和 `soul/`

---

## 六、常见问题

### Q1: 分类不准确怎么办？

A: 可以：
1. 手动移动文件到正确目录
2. 修改 `schema/tools/deepseek_classifier.py` 中的分类规则
3. 重新运行分类器

### Q2: 如何添加新的资料类型？

A: 可以：
1. 在 `raw/` 下创建新的子目录
2. 在 `schema/tools/deepseek_classifier.py` 中添加新的分类规则
3. 更新本指南

### Q3: 资料太多，如何筛选？

A: 可以：
1. 按时间筛选：只保留最近 N 个月的资料
2. 按主题筛选：只保留特定主题的资料
3. 按重要性筛选：只保留重要的资料

---

## 七、下一步

1. **初始化系统**：运行 `/digital-self` 初始化灵魂层和记忆层
2. **导入更多资料**：将其他资料导入 `raw/` 目录
3. **开始对话**：与数字副本对话，测试效果
4. **持续优化**：根据使用情况，调整分类规则和系统配置

---

> 祝你使用愉快！如果有任何问题，随时问我。
