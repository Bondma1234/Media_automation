r"""媒体自动化测试入口。

默认补齐 Allure 结果目录，调用方式示例：

    python .\main.py .\tests\kuwo\test_kuwo_smoke.py -q -rs
    python .\main.py -m "smoke and kuwo" -q -rs
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


def main() -> int:
    args = list(sys.argv[1:])
    if not any(arg.startswith("--alluredir") for arg in args):
        Path("output/allure_results").mkdir(parents=True, exist_ok=True)
        args.append("--alluredir=output/allure_results")
    return pytest.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
