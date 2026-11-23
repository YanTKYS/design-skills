#!/usr/bin/env python3
"""skills/<名前>/ の Agent Skill を、1つずつ一時フォルダーへ単独でコピーして検査する。

検査すること（https://agentskills.io/specification の最低限の制約）：
  1. SKILL.md の YAML frontmatter が、実際の YAML パーサー（PyYAML）で読めること
  2. name・description があり、name がフォルダー名と同じで、文字種・長さの制約を満たすこと
  3. SKILL.md と references/ などの Markdown の相対リンク、本文で名前を挙げた assets/ のファイルが、
     Skill のフォルダーの中に実在すること（フォルダーの外を指さないこと）
  4. フォルダーの中の LICENSE が、リポジトリ直下の LICENSE と同じ内容であること。frontmatter の license が MIT であること
また、README の「デザインを選ぶ」に載せた Skill（skills/<名前>/SKILL.md へのリンク）と、skills/ にある
Skill のフォルダーが、過不足なく一致すること（件数は固定しない）。

外部リンクの到達、エージェントによる自動選択、見た目は検査しない。

使い方：pip install -r scripts/requirements.txt && python scripts/validate-skills.py
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
ROOT_LICENSE = ROOT / "LICENSE"
LICENSE_ID = "MIT"
GALLERY_HEADING = "## デザインを選ぶ"
GALLERY_RE = re.compile(r"^## デザインを選ぶ[ \t]*\r?$(.*?)(?=^## |\Z)", re.M | re.S)
GALLERY_LINK_RE = re.compile(r"\]\(skills/([^/)\s]+)/SKILL\.md\)")
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
CODE_BLOCK_RE = re.compile(r"```.*?```", re.S)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
ASSET_RE = re.compile(r"assets/([\w.-]+\.\w+)")


def check_skill(skill_dir: Path) -> list[str]:
    """skill_dir（単独でコピーしたフォルダー）を検査し、問題の一覧を返す。"""
    problems: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md がない"]
    text = skill_md.read_text(encoding="utf-8")

    # 1. frontmatter を実際の YAML として読む
    m = FRONTMATTER_RE.match(text)
    if not m:
        return ["SKILL.md の先頭に --- で囲んだ YAML frontmatter がない"]
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return [f"frontmatter が YAML として読めない：{e}"]
    if not isinstance(data, dict):
        return ["frontmatter が YAML の対応表（キー: 値）になっていない"]

    # 2. 必須の項目と制約
    unknown = set(data) - ALLOWED_KEYS
    if unknown:
        problems.append(f"仕様にないキー：{', '.join(sorted(unknown))}")
    name = data.get("name")
    if not isinstance(name, str) or not name:
        problems.append("name がない（文字列で書く）")
    else:
        if name != skill_dir.name:
            problems.append(f"name「{name}」がフォルダー名「{skill_dir.name}」と違う")
        if not NAME_RE.match(name) or len(name) > 64:
            problems.append(f"name「{name}」は小文字英数字とハイフン（先頭・末尾・連続なし）、64字以内")
    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        problems.append("description がない（文字列で書く）")
    elif len(desc) > 1024:
        problems.append(f"description が1024字を超える（{len(desc)}字）")
    comp = data.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or len(comp) > 500):
        problems.append("compatibility は500字以内の文字列")
    lic = data.get("license")
    if lic != LICENSE_ID:
        problems.append(f"license が「{LICENSE_ID}」でない（今は {lic!r}）")
    meta = data.get("metadata")
    if meta is not None and (not isinstance(meta, dict) or not all(isinstance(v, str) for v in meta.values())):
        problems.append("metadata は「キー: 文字列」の対応表")

    # 3. 相対リンクと assets/ の参照が、Skill のフォルダーの中に実在する
    root = skill_dir.resolve()
    for md in sorted(skill_dir.rglob("*.md")):
        body = md.read_text(encoding="utf-8")
        rel = md.relative_to(skill_dir)
        for target in LINK_RE.findall(CODE_BLOCK_RE.sub("", body)):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            dest = (md.parent / target.split("#")[0]).resolve()
            if root not in dest.parents and dest != root:
                problems.append(f"{rel}: {target} が Skill のフォルダーの外を指す")
            elif not dest.exists():
                problems.append(f"{rel}: {target} の参照先がない")
        for asset in sorted(set(ASSET_RE.findall(body))):
            if not (skill_dir / "assets" / asset).is_file():
                problems.append(f"{rel}: assets/{asset} がない")
    return problems


def check_license_file(skill_dir: Path, root_license: bytes) -> list[str]:
    """skill_dir（単独でコピーしたフォルダー）の LICENSE が、リポジトリ直下の LICENSE と同じかを見る。"""
    lic = skill_dir / "LICENSE"
    if not lic.is_file():
        return ["LICENSE がない（リポジトリ直下の LICENSE と同じものを置く）"]
    if lic.read_bytes() != root_license:
        return ["LICENSE がリポジトリ直下の LICENSE と違う"]
    return []


def check_readme(dir_names: set[str]) -> list[str]:
    """README の「デザインを選ぶ」に載せた Skill と、skills/ のフォルダーを照らし合わせる。"""
    if not README.is_file():
        return ["README.md がない"]
    gallery = GALLERY_RE.search(README.read_text(encoding="utf-8"))
    if not gallery:
        return [f"README.md に「{GALLERY_HEADING}」の見出しがない"]
    listed = set(GALLERY_LINK_RE.findall(gallery.group(1)))
    problems = [f"README に載っているが skills/{n}/ がない" for n in sorted(listed - dir_names)]
    problems += [f"skills/{n}/ があるが README の「デザインを選ぶ」に載っていない" for n in sorted(dir_names - listed)]
    return problems


def main() -> int:
    dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    if not dirs:
        print("skills/ に Skill がない")
        return 1
    if not ROOT_LICENSE.is_file():
        print("NG  リポジトリ直下に LICENSE がない")
        return 1
    root_license = ROOT_LICENSE.read_bytes()
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for src in dirs:
            # Skill はフォルダーごと単独でコピーして使うので、ほかのファイルがない場所で検査する
            copy = Path(tmp) / src.name
            shutil.copytree(src, copy)
            problems = check_skill(copy) + check_license_file(copy, root_license)
            if problems:
                failed += 1
                print(f"NG  {src.name}")
                for p in problems:
                    print(f"    - {p}")
            else:
                print(f"OK  {src.name}")
    print(f"{len(dirs) - failed}/{len(dirs)} の Skill が検査を通過")
    readme_problems = check_readme({d.name for d in dirs})
    if readme_problems:
        print("NG  README の掲載と skills/ のフォルダーが一致しない")
        for p in readme_problems:
            print(f"    - {p}")
    else:
        print("OK  README の掲載と skills/ のフォルダーが一致")
    return 1 if failed or readme_problems else 0


if __name__ == "__main__":
    sys.exit(main())
