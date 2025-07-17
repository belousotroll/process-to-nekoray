#!/usr/bin/env python3
import os
import json
import argparse
import sys
from pathlib import Path

def find_executables(directories):
    """
    Recursively traverse the given directories and collect
    all unique .exe file names.
    """
    processes = set()
    for dir_path in directories:
        base = Path(dir_path)
        if not base.is_dir():
            print(f"Warning: '{base}' is not a directory, skipping.", file=sys.stderr)
            continue
        for exe_path in base.rglob("*.exe"):
            processes.add(exe_path.name)
    return sorted(processes)

def build_nekoray_block(process_names, outbound="direct"):
    """
    Build a JSON rule block for Nekoray.
    """
    return {
        "process_name": process_names,
        "outbound": outbound
    }

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories and generate a Nekoray config block"
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the JSON settings file (must contain 'scanning_dirs')"
    )
    parser.add_argument(
        "--out", "-o",
        help="Output file path (defaults to stdout)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["route", "tun"],
        default="route",
        help="Output format: 'route' (default) or 'tun'"
    )
    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"Error reading config file '{args.config}': {e}", file=sys.stderr)
        sys.exit(1)

    dirs = cfg.get("scanning_dirs")
    if not isinstance(dirs, list) or not dirs:
        print("Config file does not contain a valid 'scanning_dirs' list.", file=sys.stderr)
        sys.exit(1)

    # Find executables
    processes = find_executables(dirs)
    if not processes:
        print("No .exe files found in the specified directories.", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if args.format == "route":
        result = {"rules": [build_nekoray_block(processes)]}
        out_text = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        # Plain text list, one process per line
        out_text = "\n".join(processes)

    # Write to file or stdout
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out_text)
            print(f"Generated output saved to '{args.out}'.")
        except Exception as e:
            print(f"Error writing to '{args.out}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(out_text)

if __name__ == "__main__":
    main()
