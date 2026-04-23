from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class BuildResult:
    output_html: Path
    output_csv: Path
    tool_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build affiliate-ready free tool comparison assets")
    parser.add_argument("--config", required=True, help="Input YAML config")
    parser.add_argument("--out", default="out", help="Output directory")
    return parser.parse_args()


def _normalize_tool(tool: dict) -> dict:
    required = ["name", "category", "link", "affiliate_link", "summary"]
    missing = [k for k in required if not tool.get(k)]
    if missing:
        raise ValueError(f"Tool entry missing required fields: {missing}")
    return {
        "name": str(tool["name"]).strip(),
        "category": str(tool["category"]).strip(),
        "summary": str(tool["summary"]).strip(),
        "link": str(tool["link"]).strip(),
        "affiliate_link": str(tool["affiliate_link"]).strip(),
        "pricing": str(tool.get("pricing", "unknown")).strip(),
        "rating": float(tool.get("rating", 0.0) or 0.0),
    }


def build_assets(config_path: Path, out_dir: Path) -> BuildResult:
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("Config must be a mapping")

    tools_raw = config.get("tools")
    if not isinstance(tools_raw, list) or not tools_raw:
        raise ValueError("Config must include a non-empty tools list")

    tools = [_normalize_tool(tool) for tool in tools_raw]
    tools.sort(key=lambda t: t["rating"], reverse=True)

    out_dir.mkdir(parents=True, exist_ok=True)

    template_dir = Path(__file__).resolve().parents[1] / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html.j2")
    html = template.render(
        page_title=config.get("page_title", "Free Tool Comparison"),
        disclosure=config.get(
            "disclosure",
            "Disclosure: Some links are affiliate links and may earn a commission at no extra cost.",
        ),
        tools=tools,
    )

    output_html = out_dir / "index.html"
    output_html.write_text(html, encoding="utf-8")

    output_csv = out_dir / "affiliate_export.csv"
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "category", "pricing", "rating", "link", "affiliate_link", "summary"],
        )
        writer.writeheader()
        writer.writerows(tools)

    return BuildResult(output_html=output_html, output_csv=output_csv, tool_count=len(tools))


def main() -> None:
    args = parse_args()
    result = build_assets(config_path=Path(args.config), out_dir=Path(args.out))
    print(f"Built {result.tool_count} tools -> {result.output_html}")


if __name__ == "__main__":
    main()
