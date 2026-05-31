import json
import os
import re
import subprocess


def get_git_files():
    res = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    return [
        f
        for f in res.stdout.split("\n")
        if f and f not in ["descriptions.json"]
    ]


def get_latest_commit():
    try:
        f_res = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            capture_output=True,
            text=True,
        )
        files = [
            f
            for f in f_res.stdout.strip().split("\n")
            if f and f not in ["descriptions.json"]
        ]
        m_res = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True
        )
        return files, m_res.stdout.strip()
    except:
        return [], ""


def load_desc():
    if os.path.exists("descriptions.json"):
        with open("descriptions.json", "r") as f:
            return json.load(f)
    return {}


def save_desc(data):
    with open("descriptions.json", "w") as f:
        json.dump(data, f, indent=2)


def parse_custom_input(raw_str):
    """
    Splits by bare commas (next line indicator)
    Preserves escaped commas (\,) as literal text characters
    """
    if not raw_str.strip():
        return []
    # Split on commas NOT preceded by a backslash
    raw_lines = re.split(r"(?<!\\),", raw_str)

    processed_lines = []
    for line in raw_lines:
        # Convert escaped commas back to literal commas and clean whitespace
        cleaned = line.replace(r"\,", ",").strip()
        if cleaned:
            processed_lines.append(cleaned)
    return processed_lines


def format_for_input_box(lines_list):
    """Converts internal array back into the user string format with escaped commas"""
    if not lines_list:
        return ""
    return ", ".join([line.replace(",", r"\,") for line in lines_list])
