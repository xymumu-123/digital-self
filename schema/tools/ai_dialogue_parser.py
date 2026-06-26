#!/usr/bin/env python3
"""
AI 对话记录解析器

解析用户在AI对话中的输入部分，提取思维模式、决策模式、心智模型雏形。

支持的格式：
- ChatGPT/Claude 导出 JSON
- Markdown 格式对话记录
- 纯文本格式对话记录
- JSONL 格式

用法：
    python ai_dialogue_parser.py --file <path> --output <output_path> [--format auto|json|md|txt|jsonl]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class DialogueEntry:
    """对话条目"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None
    topic: Optional[str] = None


@dataclass
class AnalysisResult:
    """分析结果"""
    total_messages: int
    user_messages: int
    assistant_messages: int
    avg_user_message_length: float
    topics: List[str]
    thinking_patterns: List[str]
    decision_patterns: List[str]
    value_indicators: List[str]
    raw_dialogues: List[DialogueEntry]


class AIDialogueParser:
    """AI 对话记录解析器"""

    def __init__(self):
        self.dialogues: List[DialogueEntry] = []

    def parse(self, file_path: str, format_type: str = "auto") -> AnalysisResult:
        """解析对话记录文件"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 自动检测格式
        if format_type == "auto":
            format_type = self._detect_format(path)

        # 根据格式解析
        if format_type == "json":
            self._parse_json(path)
        elif format_type == "jsonl":
            self._parse_jsonl(path)
        elif format_type == "md":
            self._parse_markdown(path)
        elif format_type == "txt":
            self._parse_text(path)
        else:
            raise ValueError(f"不支持的格式: {format_type}")

        # 分析结果
        return self._analyze()

    def _detect_format(self, path: Path) -> str:
        """自动检测文件格式"""
        suffix = path.suffix.lower()
        if suffix == ".json":
            return "json"
        elif suffix == ".jsonl":
            return "jsonl"
        elif suffix == ".md":
            return "md"
        elif suffix == ".txt":
            return "txt"
        else:
            # 尝试从内容推断
            with open(path, "r", encoding="utf-8") as f:
                content = f.read(1000)
                if content.strip().startswith("{") or content.strip().startswith("["):
                    return "json"
                elif "**User**" in content or "**Human**" in content or "## User" in content:
                    return "md"
                else:
                    return "txt"

    def _parse_json(self, path: Path):
        """解析 JSON 格式（ChatGPT/Claude 导出）"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 处理不同的 JSON 结构
        if isinstance(data, list):
            # 直接是对话列表
            for item in data:
                self._extract_from_json_item(item)
        elif isinstance(data, dict):
            # 可能是包装对象
            if "messages" in data:
                for item in data["messages"]:
                    self._extract_from_json_item(item)
            elif "conversations" in data:
                for item in data["conversations"]:
                    self._extract_from_json_item(item)
            elif "mapping" in data:
                # ChatGPT 导出格式
                for key, value in data["mapping"].items():
                    if "message" in value:
                        self._extract_from_json_item(value["message"])

    def _parse_jsonl(self, path: Path):
        """解析 JSONL 格式"""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        self._extract_from_json_item(item)
                    except json.JSONDecodeError:
                        continue

    def _parse_markdown(self, path: Path):
        """解析 Markdown 格式对话记录"""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 匹配多种 Markdown 对话格式
        patterns = [
            # **User**: ... **Assistant**: ...
            r"\*\*(User|Human|Me|我)\*\*\s*[:：]\s*(.*?)(?=\*\*(User|Human|Me|我|Assistant|AI|Claude|ChatGPT)\*\*|$)",
            # ## User ... ## Assistant ...
            r"##\s*(User|Human|Me|我)\s*[:：]?\s*(.*?)(?=##\s*(User|Human|Me|我|Assistant|AI|Claude|ChatGPT)|$)",
            # > User: ... > Assistant: ...
            r">\s*(User|Human|Me|我)\s*[:：]\s*(.*?)(?=>\s*(User|Human|Me|我|Assistant|AI|Claude|ChatGPT)|$)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                for match in matches:
                    role = "user" if match[0].lower() in ["user", "human", "me", "我"] else "assistant"
                    text = match[1].strip()
                    if text:
                        self.dialogues.append(DialogueEntry(role=role, content=text))
                break

    def _parse_text(self, path: Path):
        """解析纯文本格式对话记录"""
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_role = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检测角色标记
            role_match = re.match(r"^(User|Human|Me|我|Assistant|AI|Claude|ChatGPT)\s*[:：]", line, re.IGNORECASE)
            if role_match:
                # 保存之前的内容
                if current_role and current_content:
                    self.dialogues.append(DialogueEntry(
                        role=current_role,
                        content="\n".join(current_content)
                    ))

                # 开始新段落
                role_text = role_match.group(1).lower()
                current_role = "user" if role_text in ["user", "human", "me", "我"] else "assistant"
                current_content = [line[role_match.end():].strip()]
            else:
                if current_role:
                    current_content.append(line)

        # 保存最后一段
        if current_role and current_content:
            self.dialogues.append(DialogueEntry(
                role=current_role,
                content="\n".join(current_content)
            ))

    def _extract_from_json_item(self, item: dict):
        """从 JSON 项中提取对话"""
        if not isinstance(item, dict):
            return

        # 提取角色
        role = None
        if "role" in item:
            role_str = item["role"].lower()
            if role_str in ["user", "human", "me"]:
                role = "user"
            elif role_str in ["assistant", "ai", "claude", "chatgpt"]:
                role = "assistant"
        elif "sender" in item:
            role_str = item["sender"].lower()
            if role_str in ["user", "human", "me"]:
                role = "user"
            else:
                role = "assistant"

        # 提取内容
        content = None
        if "content" in item:
            content = item["content"]
            if isinstance(content, list):
                # 多模态内容，提取文本部分
                content = " ".join([
                    c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"
                ])
        elif "text" in item:
            content = item["text"]
        elif "message" in item:
            content = item["message"]

        # 提取时间戳
        timestamp = item.get("created_at") or item.get("timestamp") or item.get("create_time")

        if role and content:
            self.dialogues.append(DialogueEntry(
                role=role,
                content=str(content),
                timestamp=str(timestamp) if timestamp else None
            ))

    def _analyze(self) -> AnalysisResult:
        """分析对话内容"""
        user_messages = [d for d in self.dialogues if d.role == "user"]
        assistant_messages = [d for d in self.dialogues if d.role == "assistant"]

        # 计算平均消息长度
        avg_length = sum(len(d.content) for d in user_messages) / len(user_messages) if user_messages else 0

        # 提取主题
        topics = self._extract_topics(user_messages)

        # 分析思维模式
        thinking_patterns = self._analyze_thinking_patterns(user_messages)

        # 分析决策模式
        decision_patterns = self._analyze_decision_patterns(user_messages)

        # 分析价值观
        value_indicators = self._analyze_values(user_messages)

        return AnalysisResult(
            total_messages=len(self.dialogues),
            user_messages=len(user_messages),
            assistant_messages=len(assistant_messages),
            avg_user_message_length=avg_length,
            topics=topics,
            thinking_patterns=thinking_patterns,
            decision_patterns=decision_patterns,
            value_indicators=value_indicators,
            raw_dialogues=self.dialogues
        )

    def _extract_topics(self, messages: List[DialogueEntry]) -> List[str]:
        """提取对话主题"""
        topics = set()
        topic_keywords = {
            "工作": ["工作", "职业", "事业", "项目", "任务", "同事", "领导", "老板", "公司"],
            "学习": ["学习", "知识", "课程", "书籍", "读书", "技能", "培训"],
            "生活": ["生活", "日常", "作息", "饮食", "健康", "运动"],
            "情感": ["感情", "爱情", "恋爱", "分手", "对象", "男朋友", "女朋友", "婚姻"],
            "家庭": ["家人", "父母", "家庭", "亲戚", "爸妈"],
            "社交": ["朋友", "社交", "聚会", "人际关系"],
            "技术": ["代码", "编程", "技术", "开发", "程序", "软件", "AI", "人工智能"],
            "创意": ["创意", "设计", "艺术", "写作", "创作"],
            "哲学": ["人生", "意义", "价值", "哲学", "思考", "反思"],
            "决策": ["选择", "决定", "权衡", "考虑", "犹豫", "纠结"],
        }

        for msg in messages:
            content = msg.content.lower()
            for topic, keywords in topic_keywords.items():
                if any(kw in content for kw in keywords):
                    topics.add(topic)

        return list(topics)

    def _analyze_thinking_patterns(self, messages: List[DialogueEntry]) -> List[str]:
        """分析思维模式"""
        patterns = []

        # 分析问题类型
        question_count = sum(1 for m in messages if "？" in m.content or "?" in m.content)
        if question_count > len(messages) * 0.3:
            patterns.append("善于提问，通过问题探索")

        # 分析逻辑词使用
        logic_words = ["因为", "所以", "因此", "但是", "然而", "不过", "虽然", "如果", "那么"]
        logic_count = sum(1 for m in messages if any(w in m.content for w in logic_words))
        if logic_count > len(messages) * 0.2:
            patterns.append("逻辑性强，善于因果推理")

        # 分析类比使用
        analogy_words = ["就像", "类似于", "好比", "相当于", "仿佛", "如同"]
        analogy_count = sum(1 for m in messages if any(w in m.content for w in analogy_words))
        if analogy_count > 3:
            patterns.append("善于使用类比")

        # 分析举例
        example_words = ["比如", "例如", "举例", "举个例子", "比如说"]
        example_count = sum(1 for m in messages if any(w in m.content for w in example_words))
        if example_count > 3:
            patterns.append("善于举例说明")

        # 分析反思
        reflection_words = ["反思", "思考", "想", "琢磨", "琢磨", "寻思"]
        reflection_count = sum(1 for m in messages if any(w in m.content for w in reflection_words))
        if reflection_count > 3:
            patterns.append("善于反思")

        # 分析消息长度
        long_messages = sum(1 for m in messages if len(m.content) > 200)
        short_messages = sum(1 for m in messages if len(m.content) < 50)
        if long_messages > len(messages) * 0.5:
            patterns.append("表达详细，喜欢深入阐述")
        elif short_messages > len(messages) * 0.5:
            patterns.append("表达简洁，言简意赅")

        return patterns

    def _analyze_decision_patterns(self, messages: List[DialogueEntry]) -> List[str]:
        """分析决策模式"""
        patterns = []

        # 分析决策相关词汇
        decision_words = ["选择", "决定", "权衡", "考虑", "犹豫", "纠结", "取舍"]
        decision_messages = [m for m in messages if any(w in m.content for w in decision_words)]

        if decision_messages:
            # 分析决策风格
            rational_words = ["分析", "数据", "逻辑", "理性", "客观", "证据"]
            emotional_words = ["感觉", "直觉", "情绪", "感受", "喜欢", "讨厌"]

            rational_count = sum(1 for m in decision_messages if any(w in m.content for w in rational_words))
            emotional_count = sum(1 for m in decision_messages if any(w in m.content for w in emotional_words))

            if rational_count > emotional_count:
                patterns.append("决策偏理性，重视数据和逻辑")
            elif emotional_count > rational_count:
                patterns.append("决策偏感性，重视直觉和感受")
            else:
                patterns.append("决策兼顾理性和感性")

            # 分析决策速度
            hesitation_words = ["犹豫", "纠结", "不知道", "怎么办", "难以抉择"]
            hesitation_count = sum(1 for m in decision_messages if any(w in m.content for w in hesitation_words))
            if hesitation_count > len(decision_messages) * 0.3:
                patterns.append("决策时容易纠结，需要充分思考")

        return patterns

    def _analyze_values(self, messages: List[DialogueEntry]) -> List[str]:
        """分析价值观"""
        values = []

        # 价值关键词映射
        value_keywords = {
            "重视效率": ["效率", "快速", "高效", "节省时间", "生产力"],
            "追求成长": ["成长", "进步", "学习", "提升", "变得更好"],
            "重视自由": ["自由", "独立", "自主", "不受约束", "灵活"],
            "重视稳定": ["稳定", "安全", "确定", "可控", "风险"],
            "重视关系": ["关系", "朋友", "家人", "陪伴", "连接"],
            "追求意义": ["意义", "价值", "目的", "使命", "重要"],
            "重视创造": ["创造", "创新", "设计", "构建", "做东西"],
            "追求真实": ["真实", "诚实", "坦诚", "直接", "不装"],
        }

        for msg in messages:
            content = msg.content
            for value, keywords in value_keywords.items():
                if any(kw in content for kw in keywords):
                    if value not in values:
                        values.append(value)

        return values


def extract_user_input_only(file_path: str, output_path: str, format_type: str = "auto"):
    """仅提取用户输入部分"""
    parser = AIDialogueParser()
    result = parser.parse(file_path, format_type)

    # 过滤出用户消息
    user_messages = [d for d in result.raw_dialogues if d.role == "user"]

    # 写入输出文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 用户对话记录（仅用户输入）\n\n")
        f.write(f"- 来源文件: {file_path}\n")
        f.write(f"- 总消息数: {result.total_messages}\n")
        f.write(f"- 用户消息数: {result.user_messages}\n")
        f.write(f"- 平均消息长度: {result.avg_user_message_length:.0f} 字符\n\n")

        f.write(f"## 思维模式分析\n\n")
        for pattern in result.thinking_patterns:
            f.write(f"- {pattern}\n")

        f.write(f"\n## 决策模式分析\n\n")
        for pattern in result.decision_patterns:
            f.write(f"- {pattern}\n")

        f.write(f"\n## 价值取向分析\n\n")
        for value in result.value_indicators:
            f.write(f"- {value}\n")

        f.write(f"\n## 主题分布\n\n")
        for topic in result.topics:
            f.write(f"- {topic}\n")

        f.write(f"\n---\n\n")
        f.write(f"## 用户消息原文\n\n")

        for i, msg in enumerate(user_messages, 1):
            f.write(f"### 消息 {i}\n\n")
            f.write(f"{msg.content}\n\n")
            if msg.timestamp:
                f.write(f"*时间: {msg.timestamp}*\n\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="AI 对话记录解析器")
    parser.add_argument("--file", "-f", required=True, help="输入文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--format", default="auto", choices=["auto", "json", "jsonl", "md", "txt"],
                        help="输入文件格式（默认自动检测）")
    parser.add_argument("--user-only", action="store_true", help="仅提取用户输入部分")

    args = parser.parse_args()

    try:
        if args.user_only:
            result = extract_user_input_only(args.file, args.output, args.format)
        else:
            parser = AIDialogueParser()
            result = parser.parse(args.file, args.format)

            # 输出完整分析结果
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(asdict(result), f, ensure_ascii=False, indent=2)

        print(f"✅ 解析完成")
        print(f"   总消息数: {result.total_messages}")
        print(f"   用户消息数: {result.user_messages}")
        print(f"   平均消息长度: {result.avg_user_message_length:.0f} 字符")
        print(f"   输出文件: {args.output}")

    except Exception as e:
        print(f"❌ 解析失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
