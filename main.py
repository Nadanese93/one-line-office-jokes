#!/usr/bin/env python3
"""Write the One-Line Office Jokes entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, no network, no reads from anywhere else. The entry is a
single line with no trailing newline, written atomically via a temp file
plus os.replace.
"""

import os
import tempfile

ENTRY = "The water cooler is the only meeting where everyone shows up on time — and nobody takes notes."


def main() -> None:
    if not 1 <= len(ENTRY) <= 199:
        raise ValueError(f"entry must be 1-199 characters, got {len(ENTRY)}")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        os.replace(tmp_path, dest)
        # Read-back verification: the file on disk must be byte-identical
        # to the entry, otherwise the write silently failed.
        with open(dest, "rb") as f:
            written = f.read()
        if written != ENTRY.encode("utf-8"):
            raise RuntimeError("entry.txt read-back mismatch after write")
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
