from pathlib import Path

from src.build_engine import build_assets


def test_build_assets(tmp_path: Path) -> None:
    config = tmp_path / "tools.yaml"
    config.write_text(
        """
page_title: Demo
tools:
  - name: Tool One
    category: seo
    summary: test tool
    link: https://example.com/tool1
    affiliate_link: https://example.com/tool1?ref=abc
    pricing: free
    rating: 4.8
""".strip()
    )

    out_dir = tmp_path / "out"
    result = build_assets(config_path=config, out_dir=out_dir)
    assert result.output_html.exists()
    assert result.output_csv.exists()
