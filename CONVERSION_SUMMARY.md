# 资料转换总结

## 转换完成

✅ **830 个 JSON 文件已成功转换为 Markdown 格式**

---

## 转换统计

| 类别 | JSON 文件数 | Markdown 文件数 | 状态 |
|------|------------|----------------|------|
| chat/ai_dialogues | 52 | 52 | ✅ |
| interests/articles | 8 | 8 | ✅ |
| interests/books | 2 | 2 | ✅ |
| interests/videos | 3 | 3 | ✅ |
| interests/websites | 31 | 31 | ✅ |
| notes/journal | 38 | 38 | ✅ |
| notes/misc | 239 | 239 | ✅ |
| notes/study | 267 | 267 | ✅ |
| personal/interests | 6 | 6 | ✅ |
| personal/life | 24 | 24 | ✅ |
| personal/relationships | 35 | 35 | ✅ |
| work/documents | 20 | 20 | ✅ |
| work/projects | 105 | 105 | ✅ |
| **总计** | **830** | **830** | ✅ |

---

## 目录结构

### 原始 JSON 格式（raw/）
```
digital-self/raw/
├── chat/ai_dialogues/         # 52 个 JSON 文件
├── interests/                 # 44 个 JSON 文件
├── notes/                     # 544 个 JSON 文件
├── personal/                  # 65 个 JSON 文件
└── work/                      # 125 个 JSON 文件
```

### 转换后 Markdown 格式（raw_md/）
```
digital-self/raw_md/
├── chat/ai_dialogues/         # 52 个 Markdown 文件
├── interests/                 # 44 个 Markdown 文件
├── notes/                     # 544 个 Markdown 文件
├── personal/                  # 65 个 Markdown 文件
└── work/                      # 125 个 Markdown 文件
```

---

## Markdown 格式示例

转换前（JSON）：
```json
{
  "id": "xxx",
  "title": "20岁积蓄旅行利弊分析",
  "created_at": "2025-05-10 17:36:55",
  "messages": [
    {
      "timestamp": "2025-05-10 17:36:56",
      "content": "人真的应该在20岁的年纪..."
    }
  ]
}
```

转换后（Markdown）：
```markdown
# 20岁积蓄旅行利弊分析

> 创建时间：2025-05-10 17:36:55

---

**[2025-05-10 17:36:56]**

人真的应该在20岁的年纪，把自己的积蓄全部用来旅行，感受世界吗？

---

*文件名：20岁积蓄旅行利弊分析_2025-05-10.json*
*ID：xxx*
```

---

## 保留的信息

✅ **标题**：保留原始标题
✅ **对话日期**：保留创建时间
✅ **每句话的时间戳**：保留每条消息的时间戳
✅ **消息内容**：保留完整内容，包括换行格式
✅ **元数据**：保留文件名和 ID

---

## 使用建议

### 1. 优先使用 Markdown 格式
- LLM 读取效率更高
- 节省 token
- 更容易提取关键信息

### 2. 保留 JSON 格式
- 保留完整元数据
- 便于程序处理
- 作为备份

### 3. 后续处理
- 可以进一步提取关键信息
- 可以生成摘要
- 可以合并相关对话

---

## 下一步

1. **初始化系统**：运行 `/digital-self`
2. **开始对话**：与数字副本对话
3. **持续优化**：根据使用情况，调整资料

---

## 工具

### 分类工具
```bash
python schema/tools/deepseek_classifier.py --input <输入目录> --output digital-self/raw
```

### 转换工具
```bash
python schema/tools/json_to_markdown.py --input <输入目录> --output <输出目录> --recursive
```

---

> 转换完成时间：2026-06-26
