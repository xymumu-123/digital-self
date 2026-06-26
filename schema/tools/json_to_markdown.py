#!/usr/bin/env python3
"""
JSON → Markdown 转换器

将 DeepSeek 导出的 JSON 对话记录转换为 Markdown 格式，保留：
- 标题
- 对话日期
- 每句话的时间戳

用法：
    python json_to_markdown.py --input <input_dir> --output <output_dir>
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def load_json_file(file_path: str) -> Dict:
    """加载 JSON 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_timestamp(timestamp: str) -> str:
    """格式化时间戳"""
    try:
        # 尝试解析时间戳
        if "T" in timestamp:
            # ISO 格式
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        else:
            # 普通格式
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        # 如果解析失败，直接返回原字符串
        return timestamp


def convert_to_markdown(data: Dict, file_name: str) -> str:
    """将 JSON 数据转换为 Markdown"""
    lines = []

    # 标题
    title = data.get("title", "未命名对话")
    lines.append(f"# {title}")
    lines.append("")

    # 对话日期
    created_at = data.get("created_at", "")
    if created_at:
        lines.append(f"> 创建时间：{format_timestamp(created_at)}")
        lines.append("")

    # 分隔线
    lines.append("---")
    lines.append("")

    # 消息列表
    messages = data.get("messages", [])
    for i, msg in enumerate(messages, 1):
        # 每句话的时间戳
        timestamp = msg.get("timestamp", "")
        if timestamp:
            lines.append(f"**[{format_timestamp(timestamp)}]**")
            lines.append("")

        # 消息内容
        content = msg.get("content", "")
        if content:
            # 保留原始换行格式
            content_lines = content.split("\n")
            for line in content_lines:
                lines.append(line)
            lines.append("")

        # 消息间分隔（除了最后一条）
        if i < len(messages):
            lines.append("---")
            lines.append("")

    # 文件信息
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*文件名：{file_name}*")
    if data.get("id"):
        lines.append(f"*ID：{data['id']}*")

    return "\n".join(lines)


def process_directory(input_dir: str, output_dir: str):
    """处理目录中的所有 JSON 文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # 统计信息
    stats = {
        "total": 0,
        "success": 0,
        "errors": []
    }

    # 遍历所有 JSON 文件
    for json_file in input_path.glob("*.json"):
        try:
            stats["total"] += 1

            # 加载 JSON
            data = load_json_file(str(json_file))

            # 转换为 Markdown
            markdown_content = convert_to_markdown(data, json_file.name)

            # 输出文件路径（保持相同的目录结构）
            relative_path = json_file.relative_to(input_path)
            output_file = output_path / relative_path.with_suffix(".md")

            # 创建输出目录
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # 写入 Markdown 文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            stats["success"] += 1
            print(f"✅ {json_file.name} → {output_file.name}")

        except Exception as e:
            stats["errors"].append({
                "file": json_file.name,
                "error": str(e)
            })
            print(f"❌ {json_file.name}: {e}")

    return stats


def main():
    # 设置控制台编码为 UTF-8
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="JSON → Markdown 转换器")
    parser.add_argument("--input", "-i", required=True, help="输入目录（包含 JSON 文件）")
    parser.add_argument("--output", "-o", required=True, help="输出目录（Markdown 文件）")
    parser.add_argument("--recursive", "-r", action="store_true", help="递归处理子目录")

    args = parser.parse_args()

    print(f"[DIR] 输入目录：{args.input}")
    print(f"[DIR] 输出目录：{args.output}")
    print(f"[MODE] 递归：{'是' if args.recursive else '否'}")
    print()

    # 处理目录
    if args.recursive:
        # 递归处理所有子目录
        input_path = Path(args.input)
        total_stats = {"total": 0, "success": 0, "errors": []}

        # 遍历所有子目录（包括嵌套目录）
        for json_file in input_path.rglob("*.json"):
            try:
                total_stats["total"] += 1

                # 加载 JSON
                data = load_json_file(str(json_file))

                # 转换为 Markdown
                markdown_content = convert_to_markdown(data, json_file.name)

                # 输出文件路径（保持相同的目录结构）
                relative_path = json_file.relative_to(input_path)
                output_file = Path(args.output) / relative_path.with_suffix(".md")

                # 创建输出目录
                output_file.parent.mkdir(parents=True, exist_ok=True)

                # 写入 Markdown 文件
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                total_stats["success"] += 1
                print(f"✅ {json_file.name} → {output_file.name}")

            except Exception as e:
                total_stats["errors"].append({
                    "file": json_file.name,
                    "error": str(e)
                })
                print(f"❌ {json_file.name}: {e}")

        stats = total_stats
    else:
        # 只处理指定目录
        stats = process_directory(args.input, args.output)

    # 打印统计
    print(f"\n[STATS] 转换统计：")
    print(f"   总文件数：{stats['total']}")
    print(f"   成功转换：{stats['success']}")
    print(f"   转换失败：{len(stats['errors'])}")

    if stats['errors']:
        print(f"\n[ERRORS] 错误列表：")
        for error in stats['errors']:
            print(f"   - {error['file']}: {error['error']}")


if __name__ == "__main__":
    main()
