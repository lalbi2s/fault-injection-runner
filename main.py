import argparse
import logging
import sys

from report import format_console, write_markdown
from runner import run_scenario
from scenario import load_scenario


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Run fault injection scenarios against the simulator."
    )
    parser.add_argument("scenarios", nargs="+", help="scenario JSON files")
    parser.add_argument(
        "--report", default="report.md", help="Markdown report path (default: report.md)"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="log events while running"
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    results = [run_scenario(load_scenario(path)) for path in args.scenarios]

    print(format_console(results))
    write_markdown(results, args.report)

    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
