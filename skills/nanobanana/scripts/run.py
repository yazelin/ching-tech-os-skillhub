#!/usr/bin/env python3
"""
Simple helper script for the nanobanana skill.
This script prints example commands to invoke nanobanana-py (does not embed MCP server code).
"""
import os
import sys
import argparse

def build_command(args):
    # Prefer uvx if available
    prompt = args.generate or args.prompt or ""
    filename = args.filename or "output"
    resolution = args.resolution or "1K"
    cmd = f"uvx nanobanana-py generate_image --prompt \"{prompt}\" --filename {filename} --resolution {resolution}"
    if args.input:
        for p in args.input:
            cmd += f" -i {p}"
    return cmd


def main():
    parser = argparse.ArgumentParser(description="Nanobanana skill helper (prints example commands)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--generate', help='Prompt to generate an image')
    group.add_argument('--edit', dest='edit_file', help='Path to image to edit')
    parser.add_argument('--prompt', help='Prompt for editing')
    parser.add_argument('--filename', help='Output filename (without ext)')
    parser.add_argument('--resolution', help='1K / 2K / 4K')
    parser.add_argument('-i','--input', action='append', help='Input reference image')

    args = parser.parse_args()

    key = os.environ.get('NANOBANANA_GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if not key:
        print('Warning: NANOBANANA_GEMINI_API_KEY not set. Set it before running the MCP.')

    # Print an example command (do not execute automatically)
    if args.generate:
        cmd = build_command(args)
        print('Example command to run (not executed):')
        print(cmd)
    elif args.edit_file:
        if not args.prompt:
            print('Provide --prompt for editing.')
            sys.exit(1)
        cmd = f"uvx nanobanana-py edit_image --file {args.edit_file} --prompt \"{args.prompt}\""
        if args.filename:
            cmd += f" --filename {args.filename}"
        print('Example command to run (not executed):')
        print(cmd)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
