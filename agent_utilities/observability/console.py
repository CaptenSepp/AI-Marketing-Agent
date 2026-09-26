import sys

SEPARATOR = "_" * 30


def print_console_section(
    title: str,
    explanation: str,
    status: str = "",
    details: str = "",
) -> None:
    """Print one clearly separated, immediately visible process update."""
    print(f"\n{SEPARATOR} {title} {SEPARATOR}\n", file=sys.stderr, flush=True)
    print(explanation, file=sys.stderr, flush=True)
    if status:
        print(f"\nStatus: {status}", file=sys.stderr, flush=True)
    if details:
        print(f"\n{details}", file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)


def write_log_only_section(title: str, details: str) -> None:
    """Write verbose diagnostics to a redirected run log, never to the terminal."""
    output = f"\n{SEPARATOR} {title} {SEPARATOR}\n\n{details}\n\n"
    writer = getattr(sys.stderr, "write_log_only", None)
    if writer:
        writer(output)


def print_session_info(
    session_id: str | None = None,
    active_llm: str | None = None,
    tool_used: str | None = None,
    note: str | None = None,
) -> None:
    """Prints clean single-line session, LLM, and tool diagnostics with empty lines in between."""
    lines = []
    if session_id:
        lines.append(f"Session ID: {session_id}")
    if active_llm:
        lines.append(f"Active LLM: {active_llm}")
    if tool_used:
        lines.append(f"Tool Used: {tool_used}")
    if note:
        lines.append(f"Note: {note}")
    if lines:
        print(
            "\n\n" + "\n\n".join(lines) + "\n\n",
            file=sys.stderr,
            flush=True,
        )
