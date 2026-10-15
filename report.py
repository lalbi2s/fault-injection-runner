from runner import Result


def verdict(result: Result) -> str:
    return "PASS" if result.passed else "FAIL"


def summary_line(results: list[Result]) -> str:
    passed = sum(1 for result in results if result.passed)
    return f"{passed} passed, {len(results) - passed} failed"


def format_console(results: list[Result]) -> str:
    lines = []
    for result in results:
        lines.append(f"[{verdict(result)}] {result.name}: {result.reason}")
        for event in result.events:
            lines.append(f"    {event}")
    lines.append("")
    lines.append(f"Summary: {summary_line(results)}")
    return "\n".join(lines)


def format_markdown(results: list[Result]) -> str:
    lines = ["# Fault injection report", "", f"Summary: {summary_line(results)}", ""]
    for result in results:
        lines.append(f"## {result.name}: {verdict(result)}")
        lines.append("")
        lines.append(result.reason)
        lines.append("")
        if result.events:
            lines.append("Timeline:")
            lines.append("")
            for event in result.events:
                lines.append(f"- {event}")
        else:
            lines.append("No events.")
        lines.append("")
    return "\n".join(lines)


def write_markdown(results: list[Result], path: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(format_markdown(results))
