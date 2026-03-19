"""
Worker tool definitions.

These are the tools available to worker nodes during execution.
They provide filesystem access scoped to the working directory.

Tool surface modeled after Codex CLI tool specs with corporeal-specific
additions (scope enforcement, KF-gated stage scoping).

Workers can: read files (with line slicing), write files, edit files,
apply unified diffs, list directories (with depth/pagination), search
file contents (via ripgrep), and run shell commands (with safe-command
detection).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Safe command detection (Codex pattern: is_known_safe_command)
# ---------------------------------------------------------------------------

_SAFE_COMMANDS = frozenset({
    # File inspection (read-only)
    "cat", "head", "tail", "less", "more", "wc", "file", "stat",
    "md5sum", "sha256sum", "xxd", "od",
    # Directory listing
    "ls", "dir", "tree", "du", "df",
    # Search (read-only)
    "grep", "egrep", "fgrep", "rg", "ag", "ack", "find", "locate",
    "which", "whereis", "type",
    # Text processing (read-only, stdout only)
    "sort", "uniq", "cut", "tr", "awk", "sed", "jq", "yq",
    "diff", "comm", "paste", "column", "fmt",
    # Git read operations
    "git",  # filtered below: only safe subcommands
    # Python / Node read-only
    "python3", "python", "node",  # filtered below
    # System info
    "date", "cal", "uptime", "uname", "hostname", "whoami", "id",
    "env", "printenv", "echo", "printf", "true", "false",
    "pwd", "basename", "dirname", "realpath", "readlink",
})

_SAFE_GIT_SUBCOMMANDS = frozenset({
    "status", "log", "diff", "show", "blame", "branch", "tag",
    "remote", "config", "describe", "rev-parse", "ls-files",
    "ls-tree", "cat-file", "shortlog", "stash",
})


def _is_safe_command(command: str) -> bool:
    """Check if a shell command is read-only (safe to run without scope gate).

    Parses the first token. For git, checks the subcommand.
    For python/node, only allows -c (inline) and --version.
    """
    parts = command.strip().split()
    if not parts:
        return False

    cmd = parts[0].split("/")[-1]  # basename

    if cmd not in _SAFE_COMMANDS:
        return False

    if cmd == "git":
        if len(parts) < 2:
            return True
        return parts[1] in _SAFE_GIT_SUBCOMMANDS

    if cmd in ("python3", "python", "node"):
        if len(parts) < 2:
            return False
        return parts[1] in ("-c", "--version", "-V")

    return True


# ---------------------------------------------------------------------------
# Max line length for read_file output (Codex: 500 chars)
# ---------------------------------------------------------------------------

MAX_LINE_LENGTH = 500


def get_worker_tools(
    working_directory: str,
    allowed_paths: list[str] | None = None,
    max_read_chars: int = 0,
) -> list[dict[str, Any]]:
    """Return the tool definitions available to worker agents.

    Args:
        working_directory: Filesystem root for the worker.
        allowed_paths: If set, write/edit/create operations restricted
            to these paths. Scope containment (PIPE-006).
        max_read_chars: If > 0, cap read_file total output.
            Tier T = 30000, Tier M = 0 (unlimited).
    """
    base = Path(working_directory)
    _scope_violations: list[dict[str, str]] = []

    def _check_write_scope(file_path: str, resolved: Path) -> str | None:
        if allowed_paths is None:
            return None
        rel = str(resolved.relative_to(base.resolve())).replace("\\", "/")
        for allowed in allowed_paths:
            norm_allowed = allowed.replace("\\", "/")
            if rel == norm_allowed or rel.startswith(norm_allowed + "/"):
                return None
        _scope_violations.append({
            "attempted_path": rel, "operation": "write",
            "allowed_paths": allowed_paths,
        })
        return (
            f"SCOPE VIOLATION: Cannot write to '{rel}'. "
            f"Declared deliverables: {allowed_paths}."
        )

    def _validate_path(file_path: str) -> Path:
        p = Path(file_path)
        if not p.is_absolute():
            p = base / p
        resolved = p.resolve()
        base_resolved = base.resolve()
        if not (
            str(resolved).startswith(str(base_resolved))
            or str(resolved).startswith(str(Path(os.environ.get("CORPOREAL_ROOT", "")).resolve()))
        ):
            raise PermissionError(
                f"Path {file_path} is outside working directory {working_directory}"
            )
        return resolved

    # -----------------------------------------------------------------------
    # read_file — with offset/limit line slicing and line length cap
    # -----------------------------------------------------------------------
    def read_file(file_path: str, offset: int = 1, limit: int = 2000) -> str:
        """Read a file with line-range slicing.

        Args:
            file_path: Absolute or relative path.
            offset: Starting line number (1-indexed, default 1).
            limit: Max lines to return (default 2000).

        Lines longer than 500 chars are truncated. Use grep_files to
        find specific content in large files instead of reading them whole.
        """
        p = _validate_path(file_path)
        if not p.exists():
            return f"ERROR: File not found: {file_path}"
        if p.is_dir():
            return f"ERROR: {file_path} is a directory. Use list_dir instead."

        try:
            raw = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"ERROR: Cannot read {file_path} (binary or non-UTF-8 file)"

        lines = raw.split("\n")
        total_lines = len(lines)

        # Clamp offset (1-indexed)
        offset = max(1, offset)
        start = offset - 1
        end = start + limit
        selected = lines[start:end]

        # Line length cap (Codex: 500 chars)
        output_lines = []
        for i, line in enumerate(selected, start=offset):
            if len(line) > MAX_LINE_LENGTH:
                line = line[:MAX_LINE_LENGTH] + "...[truncated]"
            output_lines.append(f"{i:>6}\t{line}")

        result = "\n".join(output_lines)

        # Char budget cap (tier-aware)
        if max_read_chars > 0 and len(result) > max_read_chars:
            result = (
                result[:max_read_chars]
                + f"\n\n[...TRUNCATED at {max_read_chars} chars. "
                f"Use offset/limit or grep_files for targeted reads.]"
            )

        # Append file info header
        header = f"[{file_path} | {total_lines} lines | showing {offset}-{min(offset + len(selected) - 1, total_lines)}]"
        if end < total_lines:
            header += f" (use offset={end + 1} to continue)"

        return header + "\n" + result

    # -----------------------------------------------------------------------
    # write_file
    # -----------------------------------------------------------------------
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file. Creates parent directories if needed."""
        p = _validate_path(file_path)
        scope_error = _check_write_scope(file_path, p)
        if scope_error:
            return scope_error
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"OK: Wrote {len(content)} chars to {file_path}"

    # -----------------------------------------------------------------------
    # edit_file — normalized string replacement
    # -----------------------------------------------------------------------
    def edit_file(file_path: str, old_string: str, new_string: str) -> str:
        """Replace old_string with new_string in a file (first occurrence).

        Uses normalized matching (trailing whitespace, line endings) to
        handle minor LLM formatting differences.
        """
        p = _validate_path(file_path)
        scope_error = _check_write_scope(file_path, p)
        if scope_error:
            return scope_error
        if not p.exists():
            return f"ERROR: File not found: {file_path}"
        text = p.read_text(encoding="utf-8")

        if old_string in text:
            text = text.replace(old_string, new_string, 1)
            p.write_text(text, encoding="utf-8")
            return f"OK: Replaced in {file_path}"

        def _normalize(s: str) -> str:
            lines = s.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            return "\n".join(line.rstrip() for line in lines)

        norm_text = _normalize(text)
        norm_old = _normalize(old_string)

        if norm_old not in norm_text:
            preview = old_string[:80].replace('\n', '\\n')
            return f"ERROR: old_string not found in {file_path}. Searched for: '{preview}...'"

        norm_lines = norm_text.split("\n")
        norm_old_lines = norm_old.split("\n")
        orig_lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

        match_start = None
        for i in range(len(norm_lines) - len(norm_old_lines) + 1):
            if norm_lines[i:i + len(norm_old_lines)] == norm_old_lines:
                match_start = i
                break

        if match_start is None:
            return f"ERROR: Normalized match found but line alignment failed in {file_path}"

        new_lines = new_string.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        result_lines = orig_lines[:match_start] + new_lines + orig_lines[match_start + len(norm_old_lines):]
        result_text = ("\r\n" if "\r\n" in text else "\n").join(result_lines)
        p.write_text(result_text, encoding="utf-8")
        return f"OK: Replaced in {file_path} (normalized match)"

    # -----------------------------------------------------------------------
    # apply_patch — unified diff application (Codex pattern)
    # Lets the LLM write diffs instead of full file content.
    # A 200-line JSON as a diff = ~2K tokens. As write_file = 8K+.
    # -----------------------------------------------------------------------
    def apply_patch(patch: str) -> str:
        """Apply a unified diff patch to files in the working directory.

        The patch should be in unified diff format (output of `diff -u`
        or `git diff`). Each file in the patch is applied independently.
        Paths in the patch are resolved relative to the working directory.

        This is more token-efficient than write_file for modifications —
        writing a diff for a 200-line file is ~2K tokens vs ~8K for the
        full file content. Use apply_patch for edits, write_file for
        new files.

        Example patch format:
        --- a/path/to/file.json
        +++ b/path/to/file.json
        @@ -10,3 +10,4 @@
         existing line
        -old line
        +new line
        +added line
         existing line
        """
        import re as _re

        results = []
        current_file = None
        hunks: list[tuple[int, int, list[str]]] = []

        def _flush():
            nonlocal current_file, hunks
            if current_file and hunks:
                try:
                    r = _apply_file_patch(current_file, hunks)
                    results.append(r)
                except Exception as e:
                    results.append(f"ERROR: {current_file}: {e}")
            current_file = None
            hunks = []

        lines = patch.split("\n")
        current_hunk_lines: list[str] = []
        hunk_start = 0
        hunk_count = 0

        for line in lines:
            # File header: --- a/path or +++ b/path
            if line.startswith("+++ b/") or line.startswith("+++ "):
                _flush()
                # Extract path (strip +++ b/ or +++ prefix)
                path = line[6:] if line.startswith("+++ b/") else line[4:]
                path = path.strip()
                # Strip timestamp if present (diff -u adds timestamps)
                if "\t" in path:
                    path = path.split("\t")[0]
                current_file = path
                continue

            if line.startswith("--- "):
                continue  # Skip --- line, we use +++ for the target path

            # Hunk header: @@ -start,count +start,count @@
            hunk_match = _re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if hunk_match:
                # Save previous hunk
                if current_hunk_lines:
                    hunks.append((hunk_start, hunk_count, current_hunk_lines))
                hunk_start = int(hunk_match.group(1))
                hunk_count = int(hunk_match.group(2) or "1")
                current_hunk_lines = []
                continue

            # Hunk content: lines starting with +, -, or space
            if current_file and (line.startswith("+") or line.startswith("-") or line.startswith(" ") or line == ""):
                current_hunk_lines.append(line)

        # Flush final hunk and file
        if current_hunk_lines:
            hunks.append((hunk_start, hunk_count, current_hunk_lines))
        _flush()

        if not results:
            return "ERROR: No valid patches found in input. Use unified diff format (diff -u)."
        return "\n".join(results)

    def _apply_file_patch(rel_path: str, hunks: list[tuple[int, int, list[str]]]) -> str:
        """Apply hunks to a single file."""
        p = _validate_path(rel_path)
        scope_error = _check_write_scope(rel_path, p)
        if scope_error:
            return scope_error

        if p.exists():
            original = p.read_text(encoding="utf-8").split("\n")
        else:
            original = []
            p.parent.mkdir(parents=True, exist_ok=True)

        result = list(original)
        offset = 0  # Track line shifts from prior hunks

        for hunk_start, hunk_count, hunk_lines in hunks:
            pos = hunk_start - 1 + offset  # 0-indexed with offset
            new_lines = []
            removed = 0

            for hl in hunk_lines:
                if hl.startswith("-"):
                    # Remove line
                    removed += 1
                elif hl.startswith("+"):
                    # Add line
                    new_lines.append(hl[1:])
                elif hl.startswith(" "):
                    # Context line (keep)
                    new_lines.append(hl[1:])
                elif hl == "":
                    # Empty context line
                    new_lines.append("")

            # Replace the hunk range
            end = pos + hunk_count
            result[pos:end] = new_lines
            offset += len(new_lines) - hunk_count

        p.write_text("\n".join(result), encoding="utf-8")
        changes = sum(1 for h in hunks for l in h[2] if l.startswith("+") or l.startswith("-"))
        return f"OK: Patched {rel_path} ({changes} changed lines across {len(hunks)} hunk(s))"

    # -----------------------------------------------------------------------
    # list_dir — with depth control and pagination (Codex pattern)
    # -----------------------------------------------------------------------
    def list_dir(dir_path: str = ".", depth: int = 2, offset: int = 1, limit: int = 25) -> str:
        """List directory contents with depth control and pagination.

        Args:
            dir_path: Directory to list (default: working directory).
            depth: Max traversal depth (default 2). 1 = immediate children only.
            offset: 1-indexed start position for pagination (default 1).
            limit: Max entries to return (default 25).

        Returns entries with type labels: [dir] or [file] with size.
        """
        p = _validate_path(dir_path)
        if not p.exists():
            return f"ERROR: Directory not found: {dir_path}"
        if not p.is_dir():
            return f"ERROR: {dir_path} is a file, not a directory. Use read_file."

        entries = []
        _collect_entries(p, p, depth, entries)

        total = len(entries)
        start = max(0, offset - 1)
        page = entries[start:start + limit]

        lines = [f"[{dir_path} | {total} entries | showing {offset}-{min(offset + len(page) - 1, total)}]"]
        for rel, is_dir, size in page:
            if is_dir:
                lines.append(f"  [dir]  {rel}/")
            else:
                size_str = _human_size(size)
                lines.append(f"  [file] {rel}  ({size_str})")

        if start + limit < total:
            lines.append(f"  ... {total - start - limit} more (use offset={start + limit + 1})")

        return "\n".join(lines)

    def _collect_entries(root: Path, current: Path, max_depth: int, entries: list, _depth: int = 0):
        if _depth >= max_depth:
            return
        try:
            children = sorted(current.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return
        for child in children:
            try:
                rel = str(child.relative_to(root)).replace("\\", "/")
            except ValueError:
                continue
            if child.is_dir():
                entries.append((rel, True, 0))
                _collect_entries(root, child, max_depth, entries, _depth + 1)
            else:
                try:
                    size = child.stat().st_size
                except OSError:
                    size = 0
                entries.append((rel, False, size))

    def _human_size(size: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

    # -----------------------------------------------------------------------
    # grep_files — ripgrep wrapper with timeout and sorting (Codex pattern)
    # Falls back to Python regex if rg not available.
    # -----------------------------------------------------------------------
    def grep_files(pattern: str, include: str = "", path: str = "", limit: int = 100) -> str:
        """Search file contents for a regex pattern using ripgrep.

        Args:
            pattern: Regex pattern to search for.
            include: Glob filter for files (e.g., '*.json', '*.md'). Optional.
            path: Subdirectory to search within (relative to working dir). Optional.
            limit: Max matching files to return (default 100, max 2000).

        Returns matching file paths sorted by modification time (newest first),
        with the first match line shown for each file.
        """
        limit = min(max(1, limit), 2000)
        search_dir = str(base / path) if path else str(base)

        # Try ripgrep first (fast, handles binary files, respects gitignore)
        rg_available = True
        try:
            subprocess.run(["rg", "--version"], capture_output=True, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            rg_available = False

        if rg_available:
            cmd = ["rg", "--files-with-matches", "--sort=modified", "-m", "1"]
            if include:
                cmd.extend(["--glob", include])
            cmd.extend([pattern, search_dir])

            try:
                result = subprocess.run(
                    cmd, capture_output=True, text=True,
                    timeout=30, cwd=str(base),
                )
                files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
                files = files[:limit]

                if not files:
                    return "No matches found."

                # Get first match line per file
                output = []
                for fp in files:
                    try:
                        rel = str(Path(fp).relative_to(base)).replace("\\", "/")
                    except ValueError:
                        rel = fp
                    # Get first match
                    match_result = subprocess.run(
                        ["rg", "-m", "1", "-n", pattern, fp],
                        capture_output=True, text=True, timeout=5,
                    )
                    first_match = match_result.stdout.strip().split("\n")[0] if match_result.stdout else ""
                    output.append(f"{rel}: {first_match}")

                return "\n".join(output)
            except subprocess.TimeoutExpired:
                return "ERROR: Search timed out after 30 seconds. Try a more specific pattern or path."
            except Exception as e:
                return f"ERROR: ripgrep failed: {e}"

        # Fallback: Python regex (slower, no timeout protection)
        import re
        results = []
        glob_pattern = include if include else "**/*"
        search_path = base / path if path else base
        for p in search_path.glob(glob_pattern):
            if not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8")
                for i, line in enumerate(text.splitlines(), 1):
                    if re.search(pattern, line):
                        rel = str(p.relative_to(base)).replace("\\", "/")
                        results.append(f"{rel}:{i}: {line.strip()}")
                        break  # Only first match per file
            except (UnicodeDecodeError, PermissionError):
                continue
            if len(results) >= limit:
                break
        return "\n".join(results) if results else "No matches found."

    # -----------------------------------------------------------------------
    # Deploy-tier command classification
    # -----------------------------------------------------------------------
    _DEPLOY_COMMANDS = frozenset({
        "terraform", "safe-ec2-deploy.sh", "build-and-upload.sh",
        "docker", "kubectl", "aws",
    })

    def _is_deploy_command(command: str) -> bool:
        """Detect deploy-tier commands that modify infrastructure.

        Deploy-tier commands execute autonomously when the Coordinator's
        dependency graph says all upstream tasks are complete. No human
        gate -- the PRD acceptance IS the authorization.
        """
        parts = command.strip().split()
        if not parts:
            return False
        cmd = parts[0].split("/")[-1]  # basename
        if cmd in _DEPLOY_COMMANDS:
            return True
        # Check for terraform subcommands that mutate
        if cmd == "terraform" and len(parts) >= 2:
            return parts[1] in ("apply", "destroy", "import")
        return False

    # -----------------------------------------------------------------------
    # run_command — with safe-command detection + deploy-tier classification
    # -----------------------------------------------------------------------
    _SHELL_WRITE_OPERATORS = (
        ">", ">>", "tee ", "tee\t",
        "mv ", "mv\t", "cp ", "cp\t",
        "mkdir ", "mkdir\t", "touch ", "touch\t",
        "rm ", "rm\t", "rmdir ", "rmdir\t",
    )

    def run_command(command: str) -> str:
        """Run a shell command in the working directory.

        Three tiers:
        - Safe (read-only): always allowed (ls, grep, git status)
        - Build (write): allowed when scope permits (pip, bun, cp)
        - Deploy (infrastructure mutation): allowed autonomously when
          Coordinator dependency graph confirms upstream completion.
          No human gate.

        Deploy-tier commands get a longer timeout (600s vs 120s) to
        accommodate terraform apply, gold layer runs, etc.
        """
        if allowed_paths is not None and not _is_safe_command(command):
            cmd_stripped = command.strip()
            for op in _SHELL_WRITE_OPERATORS:
                if op in cmd_stripped:
                    _scope_violations.append({
                        "attempted_path": cmd_stripped[:100],
                        "operation": "run_command",
                        "allowed_paths": allowed_paths,
                    })
                    return (
                        f"SCOPE VIOLATION: Shell command blocked — "
                        f"contains write operator '{op.strip()}'. "
                        f"Use write_file, edit_file, or apply_patch instead."
                    )

        # Deploy-tier gets longer timeout
        timeout = 600 if _is_deploy_command(command) else 120

        try:
            result = subprocess.run(
                command, shell=True, cwd=str(base),
                capture_output=True, text=True, timeout=timeout,
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output[:10000]
        except subprocess.TimeoutExpired:
            return f"ERROR: Command timed out after {timeout} seconds"
        except Exception as e:
            return f"ERROR: {e}"

    # -----------------------------------------------------------------------
    # git_commit — enforced author attribution + selective staging
    # -----------------------------------------------------------------------
    def git_commit(message: str, author_serial: str, files: list[str] | None = None) -> str:
        """Commit changes with enforced agent author attribution.

        Stages only the specified files (or files written during this
        execution if none specified). Commits with --author in the
        canonical agent format. Captures and returns the commit SHA.

        Args:
            message: Commit message.
            author_serial: Agent serial (e.g., "DS.CP.1"). Used as
                both author name and email prefix.
            files: Specific files to stage. If None, stages all
                modified/new files in the working directory.
        """
        import sys

        # Validate author_serial format (alphanumeric + dots only)
        if not all(c.isalnum() or c in "._ " for c in author_serial):
            return f"ERROR: Invalid author_serial '{author_serial}'. Use alphanumeric + dots only."

        author = f"{author_serial} <{author_serial}@corporeal.agent>"

        try:
            # Stage files
            if files:
                for f in files:
                    p = _validate_path(f)
                    rel = str(p.relative_to(base.resolve())).replace("\\", "/")
                    stage_result = subprocess.run(
                        ["git", "add", rel], cwd=str(base),
                        capture_output=True, text=True, timeout=30,
                    )
                    if stage_result.returncode != 0:
                        return f"ERROR: git add failed for {rel}: {stage_result.stderr}"
            else:
                # Stage all changes in working directory
                subprocess.run(
                    ["git", "add", "-A"], cwd=str(base),
                    capture_output=True, text=True, timeout=30,
                )

            # Check if there's anything to commit
            status = subprocess.run(
                ["git", "diff", "--cached", "--quiet"], cwd=str(base),
                capture_output=True, timeout=10,
            )
            if status.returncode == 0:
                return "OK: Nothing to commit (no staged changes)"

            # Commit with author
            commit_result = subprocess.run(
                ["git", "commit", f"--author={author}", "-m", message],
                cwd=str(base), capture_output=True, text=True, timeout=30,
            )
            if commit_result.returncode != 0:
                return f"ERROR: git commit failed: {commit_result.stderr}"

            # Capture SHA
            sha_result = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=str(base),
                capture_output=True, text=True, timeout=10,
            )
            sha = sha_result.stdout.strip()[:12]

            print(f"  [GIT] Committed {sha} by {author_serial}", file=sys.stderr)
            return f"OK: Committed {sha} by {author_serial}: {message}"

        except subprocess.TimeoutExpired:
            return "ERROR: git operation timed out"
        except Exception as e:
            return f"ERROR: git_commit failed: {e}"

    # -----------------------------------------------------------------------
    # ask_user — structured user input (Claude Agent SDK pattern)
    # Retained for backward compatibility but NOT used in autonomous mode.
    # Once PRD is accepted, execution is fully autonomous.
    # -----------------------------------------------------------------------
    def ask_user(question: str, options: list[str] | None = None, context: str = "") -> str:
        """Ask PRINCIPAL a clarifying question.

        Emits an ask_user event to the event bus with the question and options.
        In interactive mode, this will fire a LangGraph interrupt.
        In autonomous mode, the interrupt_resolver handles it.

        The response is returned as a string to the LLM.
        """
        try:
            from langgraph.types import interrupt
            response = interrupt({
                "authority_type": "execution",
                "sub_type": "worker_question",
                "tier": 2,
                "holder": "worker",
                "message": question,
                "resolution_options": options or ["(freeform response)"],
                "context": {
                    "question": question,
                    "options": options or [],
                    "why": context,
                },
            })
            if isinstance(response, dict):
                return response.get("answer", str(response))
            return str(response)
        except Exception as e:
            # If interrupts aren't available (no LangGraph context),
            # return a message telling the worker to proceed with best guess
            return (
                f"Unable to reach PRINCIPAL for clarification. "
                f"Proceed with your best judgment based on available context. "
                f"Your question was: {question}"
            )

    # -----------------------------------------------------------------------
    # Tool list — returned to caller
    # -----------------------------------------------------------------------
    return [
        {
            "name": "read_file",
            "description": (
                "Read a file with optional line-range slicing. "
                "Lines > 500 chars are truncated. "
                "Use offset/limit for large files instead of reading everything."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute or relative file path"},
                    "offset": {"type": "number", "description": "Starting line number, 1-indexed (default: 1)"},
                    "limit": {"type": "number", "description": "Max lines to return (default: 2000)"},
                },
                "required": ["file_path"],
            },
            "handler": read_file,
        },
        {
            "name": "write_file",
            "description": (
                "Write content to a file. Creates directories if needed. "
                "For modifying existing files, prefer edit_file or apply_patch "
                "(more token-efficient)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Full file content to write"},
                },
                "required": ["file_path", "content"],
            },
            "handler": write_file,
        },
        {
            "name": "edit_file",
            "description": (
                "Replace old_string with new_string in a file (first occurrence). "
                "Handles minor whitespace/line-ending differences automatically."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "File path to edit"},
                    "old_string": {"type": "string", "description": "Exact string to find"},
                    "new_string": {"type": "string", "description": "Replacement string"},
                },
                "required": ["file_path", "old_string", "new_string"],
            },
            "handler": edit_file,
        },
        {
            "name": "apply_patch",
            "description": (
                "Apply a unified diff patch to one or more files. "
                "More token-efficient than write_file for modifications -- "
                "a 200-line edit as a diff is ~2K tokens vs ~8K as full content. "
                "Use standard unified diff format (diff -u / git diff)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "patch": {
                        "type": "string",
                        "description": (
                            "Unified diff content. Example:\n"
                            "--- a/file.json\n"
                            "+++ b/file.json\n"
                            "@@ -10,3 +10,4 @@\n"
                            " context\n"
                            "-old line\n"
                            "+new line\n"
                            "+added line\n"
                            " context"
                        ),
                    },
                },
                "required": ["patch"],
            },
            "handler": apply_patch,
        },
        {
            "name": "list_dir",
            "description": (
                "List directory contents with depth control and pagination. "
                "Shows [dir] and [file] labels with sizes. "
                "Default: depth=2, limit=25."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "dir_path": {"type": "string", "description": "Directory path (default: working directory)", "default": "."},
                    "depth": {"type": "number", "description": "Max traversal depth (default: 2)"},
                    "offset": {"type": "number", "description": "Pagination start, 1-indexed (default: 1)"},
                    "limit": {"type": "number", "description": "Max entries to return (default: 25)"},
                },
            },
            "handler": list_dir,
        },
        {
            "name": "grep_files",
            "description": (
                "Search file contents for a regex pattern. Uses ripgrep for speed. "
                "Returns matching files sorted by modification time (newest first) "
                "with the first match line per file. Default limit: 100 files."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Regex pattern to search for"},
                    "include": {"type": "string", "description": "Glob filter (e.g., '*.json', '*.md'). Optional."},
                    "path": {"type": "string", "description": "Subdirectory to search within. Optional."},
                    "limit": {"type": "number", "description": "Max files to return (default: 100, max: 2000)"},
                },
                "required": ["pattern"],
            },
            "handler": grep_files,
        },
        {
            "name": "run_command",
            "description": (
                "Run a shell command in the working directory. "
                "Read-only commands (grep, ls, git status, python -c) always allowed. "
                "In strict scope mode, write commands are blocked -- "
                "use write_file/edit_file/apply_patch for file modifications."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"},
                },
                "required": ["command"],
            },
            "handler": run_command,
        },
        {
            "name": "git_commit",
            "description": (
                "Commit staged changes with enforced agent author attribution. "
                "Stages specified files (or all changes), commits with --author, "
                "returns the commit SHA. Use in the Ad (Adaptation) stage after "
                "all deliverables are written."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Commit message"},
                    "author_serial": {
                        "type": "string",
                        "description": "Agent serial (e.g., 'DS.CP.1'). Used as commit author.",
                    },
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Files to stage (optional -- stages all if omitted)",
                    },
                },
                "required": ["message", "author_serial"],
            },
            "handler": git_commit,
        },
    ]


# ---------------------------------------------------------------------------
# KF gate v3 — Layer 2 budget resolver (SYS.CORE.KF_GATED_EXEC_IMPL Section 5)
# ---------------------------------------------------------------------------

def resolve_read_ratio(
    read_ratio: float,
    total_iterations: int,
) -> tuple[int, int]:
    """Compute (read_ceiling, write_budget) from read_ratio.

    read_ceiling: max iterations for Pe+In combined (the read phase).
    write_budget: remaining iterations for Ac+Ad (the write phase).

    read_ceiling = floor(total_iterations * clamp(read_ratio, 0.0, 1.0))
    write_budget = total_iterations - read_ceiling

    Spec: ONT.CORE.KF_GATED_EXECUTION v3 Section 4,
          SYS.CORE.KF_GATED_EXEC_IMPL Section 5
    """
    import math
    clamped = max(0.0, min(1.0, read_ratio))
    read_ceiling = math.floor(total_iterations * clamped)
    write_budget = total_iterations - read_ceiling
    return read_ceiling, write_budget


# ---------------------------------------------------------------------------
# KF-Gated tool scoping (ONT.CORE.KF_GATED_EXECUTION)
# ---------------------------------------------------------------------------

# Tool sets per KF stage. The key enforcement: Ac removes all read tools.
_STAGE_TOOLS = {
    "Pe": {"list_dir", "grep_files", "read_file", "run_command"},
    "In": {"read_file", "grep_files"},
    "Ac": {"write_file", "edit_file", "apply_patch"},
    "Ad": {"read_file", "write_file", "edit_file", "apply_patch", "run_command", "git_commit"},
}


def scope_tools_for_stage(stage: str, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter tool list to only those available in the given KF stage.

    Pe (Perception): discover and observe. list_dir, grep_files, read_file, run_command.
    In (Interpretation): targeted reads. read_file, grep_files.
    Ac (Action): write only. write_file, edit_file, apply_patch. READ TOOLS REMOVED.
    Ad (Adaptation): self-check + fix. read_file, write tools, run_command.

    This is the gate that prevents the infinite-reading failure mode.
    """
    allowed = _STAGE_TOOLS.get(stage)
    if allowed is None:
        return tools
    return [t for t in tools if t.get("name") in allowed]


# Default KF budget allocations by archetype (percentage of total iterations).
DEFAULT_KF_BUDGETS = {
    "supplier":    {"Pe": 0.40, "In": 0.20, "Ac": 0.30, "Ad": 0.10},
    "transformer": {"Pe": 0.30, "In": 0.10, "Ac": 0.50, "Ad": 0.10},
    "compositor":  {"Pe": 0.20, "In": 0.00, "Ac": 0.60, "Ad": 0.20},
    "operator":    {"Pe": 0.30, "In": 0.20, "Ac": 0.10, "Ad": 0.40},
}


def resolve_kf_budget(
    kf_budget: dict[str, int],
    archetype: str,
    total_iterations: int,
) -> dict[str, int]:
    """Resolve KF stage budgets for a worker.

    If kf_budget is provided by the Coordinator, use it directly.
    Otherwise, compute from archetype defaults and total iterations.
    Ensures every stage gets at least 1 iteration (except In which can be 0).
    Ensures Ac always gets at least 2 iterations.
    """
    if kf_budget:
        resolved = {}
        for stage in ("Pe", "In", "Ac", "Ad"):
            resolved[stage] = kf_budget.get(stage, 0)
        if resolved["Ac"] < 2:
            resolved["Ac"] = 2
        return resolved

    pcts = DEFAULT_KF_BUDGETS.get(archetype, DEFAULT_KF_BUDGETS["transformer"])
    resolved = {}
    for stage, pct in pcts.items():
        resolved[stage] = max(1, round(pct * total_iterations)) if pct > 0 else 0

    if resolved["Ac"] < 2:
        resolved["Ac"] = 2

    total = sum(resolved.values())
    while total > total_iterations:
        largest = max(resolved, key=resolved.get)
        if resolved[largest] > 2:
            resolved[largest] -= 1
            total -= 1
        else:
            break
    while total < total_iterations:
        resolved["Ac"] += 1
        total += 1

    return resolved
