#!/usr/bin/env python3
"""
DeepSeek 对话记录分类器

读取 DeepSeek 导出的 JSON 对话记录，根据主题自动分类到对应的 raw/ 子目录。

用法：
    python deepseek_classifier.py --input <input_dir> --output <output_dir> [--dry-run]
"""

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Conversation:
    """对话记录"""
    id: str
    title: str
    created_at: str
    messages: List[Dict]
    file_path: str


# 分类关键词映射
CATEGORY_KEYWORDS = {
    "chat/ai_dialogues": [
        "AI", "人工智能", "ChatGPT", "Claude", "DeepSeek", "大模型", "机器学习",
        "深度学习", "神经网络", "GPT", "LLM", "自然语言处理", "NLP"
    ],
    "notes/journal": [
        "日记", "心情", "感受", "反思", "总结", "回顾", "感悟", "人生", "生活",
        "情绪", "心理", "焦虑", "迷茫", "成长", "改变"
    ],
    "notes/study": [
        "学习", "教程", "课程", "笔记", "知识", "技能", "方法", "理论", "原理",
        "概念", "定义", "公式", "计算", "分析", "研究", "论文", "文献"
    ],
    "work/projects": [
        "项目", "工作", "任务", "需求", "设计", "开发", "测试", "上线", "部署",
        "代码", "编程", "程序", "软件", "系统", "架构", "数据库", "API"
    ],
    "work/documents": [
        "文档", "报告", "方案", "计划", "总结", "汇报", "PPT", "Word", "Excel",
        "简历", "求职", "面试", "职业", "晋升", "薪资"
    ],
    "interests/books": [
        "书籍", "读书", "阅读", "小说", "文学", "作者", "出版社", "推荐书单"
    ],
    "interests/articles": [
        "文章", "新闻", "资讯", "报道", "评论", "观点", "看法", "思考"
    ],
    "interests/videos": [
        "视频", "电影", "电视剧", "综艺", "动漫", "纪录片", "YouTube", "B站"
    ],
    "interests/websites": [
        "网站", "工具", "软件", "应用", "平台", "资源", "下载", "安装"
    ],
    "personal/life": [
        "生活", "日常", "饮食", "健康", "运动", "睡眠", "养生", "医疗", "疾病",
        "购物", "消费", "理财", "投资", "旅行", "旅游", "出行"
    ],
    "personal/relationships": [
        "感情", "恋爱", "婚姻", "家庭", "父母", "孩子", "朋友", "社交", "人际",
        "约会", "分手", "结婚", "离婚", "亲情", "友情"
    ],
    "personal/interests": [
        "爱好", "兴趣", "游戏", "音乐", "摄影", "绘画", "手工", "烹饪", "美食",
        "运动", "健身", "跑步", "游泳", "篮球", "足球"
    ]
}


def load_conversation(file_path: str) -> Conversation:
    """加载对话记录"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Conversation(
        id=data.get("id", ""),
        title=data.get("title", ""),
        created_at=data.get("created_at", ""),
        messages=data.get("messages", []),
        file_path=file_path
    )


def classify_conversation(conv: Conversation) -> str:
    """根据标题和内容分类对话"""
    # 合并标题和所有消息内容
    text = conv.title + " "
    for msg in conv.messages:
        text += msg.get("content", "") + " "

    text = text.lower()

    # 计算每个类别的匹配分数
    scores: Dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        if score > 0:
            scores[category] = score

    # 返回得分最高的类别
    if scores:
        return max(scores, key=scores.get)

    # 如果没有匹配，返回默认类别
    return "notes/misc"


def classify_by_title_pattern(conv: Conversation) -> str:
    """根据标题模式分类"""
    title = conv.title

    # 学术论文相关
    if re.search(r"论文|研究|调查|分析|设计|方法|结论|摘要|参考文献", title):
        return "notes/study"

    # 工作相关
    if re.search(r"项目|工作|代码|编程|开发|系统|架构|数据库", title):
        return "work/projects"

    # 生活相关
    if re.search(r"生活|日常|健康|运动|饮食|睡眠|购物|理财", title):
        return "personal/life"

    # 感情相关
    if re.search(r"恋爱|婚姻|感情|约会|分手|结婚|家庭|父母", title):
        return "personal/relationships"

    # 技术相关
    if re.search(r"软件|工具|网站|平台|资源|下载|安装|配置", title):
        return "interests/websites"

    # 学习相关
    if re.search(r"学习|教程|课程|笔记|知识|技能|方法", title):
        return "notes/study"

    return None


def process_conversations(input_dir: str, output_dir: str, dry_run: bool = False) -> Dict:
    """处理所有对话记录"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # 统计信息
    stats = {
        "total": 0,
        "classified": {},
        "errors": []
    }

    # 遍历所有 JSON 文件
    for json_file in input_path.glob("*.json"):
        try:
            stats["total"] += 1

            # 加载对话
            conv = load_conversation(str(json_file))

            # 先尝试根据标题模式分类
            category = classify_by_title_pattern(conv)

            # 如果标题模式没有匹配，使用关键词分类
            if category is None:
                category = classify_conversation(conv)

            # 更新统计
            if category not in stats["classified"]:
                stats["classified"][category] = []
            stats["classified"][category].append({
                "file": json_file.name,
                "title": conv.title,
                "created_at": conv.created_at
            })

            # 如果不是 dry-run，复制文件到对应目录
            if not dry_run:
                target_dir = output_path / category
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_dir / json_file.name
                shutil.copy2(str(json_file), str(target_file))

            print(f"✅ {json_file.name} → {category}")

        except Exception as e:
            stats["errors"].append({
                "file": json_file.name,
                "error": str(e)
            })
            print(f"❌ {json_file.name}: {e}")

    return stats


def generate_report(stats: Dict, output_dir: str):
    """生成分类报告"""
    report_path = Path(output_dir) / "classification_report.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# DeepSeek 对话记录分类报告\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 总计\n\n")
        f.write(f"- 总文件数：{stats['total']}\n")
        f.write(f"- 成功分类：{stats['total'] - len(stats['errors'])}\n")
        f.write(f"- 分类失败：{len(stats['errors'])}\n\n")

        f.write(f"## 分类统计\n\n")
        f.write(f"| 类别 | 数量 |\n")
        f.write(f"|------|------|\n")
        for category, items in sorted(stats["classified"].items()):
            f.write(f"| {category} | {len(items)} |\n")

        f.write(f"\n## 详细列表\n\n")
        for category, items in sorted(stats["classified"].items()):
            f.write(f"### {category}\n\n")
            for item in items:
                f.write(f"- **{item['title']}** ({item['created_at']})\n")
            f.write("\n")

        if stats["errors"]:
            f.write(f"## 错误列表\n\n")
            for error in stats["errors"]:
                f.write(f"- **{error['file']}**: {error['error']}\n")

    print(f"\n📊 分类报告已生成：{report_path}")


def main():
    # 设置控制台编码为 UTF-8
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="DeepSeek 对话记录分类器")
    parser.add_argument("--input", "-i", required=True, help="输入目录（包含 JSON 文件）")
    parser.add_argument("--output", "-o", required=True, help="输出目录（分类后的目录）")
    parser.add_argument("--dry-run", "-n", action="store_true", help="仅显示分类结果，不实际移动文件")

    args = parser.parse_args()

    print(f"[DIR] 输入目录：{args.input}")
    print(f"[DIR] 输出目录：{args.output}")
    print(f"[MODE] 模式：{'dry-run' if args.dry_run else '实际执行'}\n")

    # 处理对话记录
    stats = process_conversations(args.input, args.output, args.dry_run)

    # 生成报告
    generate_report(stats, args.output)

    # 打印统计
    print(f"\n[STATS] 分类统计：")
    print(f"   总文件数：{stats['total']}")
    print(f"   成功分类：{stats['total'] - len(stats['errors'])}")
    print(f"   分类失败：{len(stats['errors'])}")
    print(f"\n[DIST] 分类分布：")
    for category, items in sorted(stats["classified"].items()):
        print(f"   {category}: {len(items)}")


if __name__ == "__main__":
    main()
