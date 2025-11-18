#!/usr/bin/env python3
"""
Mermaid Diagram Extractor and PNG Converter
Extracts Mermaid diagrams from Markdown files and converts them to HD PNG images

Features:
    - High-quality HD images (3x scale, 2400px width)
    - Transparent background
    - Professional output quality

Requirements:
    - Node.js installed
    - @mermaid-js/mermaid-cli package (npm install -g @mermaid-js/mermaid-cli)

Usage:
    python mermaid_to_png.py input.md [output_dir]

If output_dir is not specified, images will be saved in: ./mermaid_images/
"""

import sys
import os
import re
import subprocess
import tempfile
from pathlib import Path


def extract_mermaid_diagrams(input_content):
    """
    Extract all Mermaid diagrams from Markdown content.

    Args:
        input_content (str): Markdown file content

    Returns:
        list: List of tuples (diagram_number, diagram_code)
    """
    diagrams = []

    # Pattern to match mermaid code blocks
    pattern = r'```mermaid\n(.*?)```'
    matches = re.findall(pattern, input_content, re.DOTALL)

    for idx, diagram_code in enumerate(matches, start=1):
        diagrams.append((idx, diagram_code.strip()))

    return diagrams


def check_mermaid_cli():
    """
    Check if mermaid-cli (mmdc) is installed.

    Returns:
        bool: True if installed, False otherwise
    """
    try:
        result = subprocess.run(
            ['mmdc', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def convert_mermaid_to_png(diagram_code, output_path):
    """
    Convert a single Mermaid diagram to PNG using mermaid-cli.

    Args:
        diagram_code (str): Mermaid diagram code
        output_path (str): Path where PNG should be saved

    Returns:
        bool: True if successful, False otherwise
    """
    # Create temporary file for mermaid code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
        temp_file.write(diagram_code)
        temp_file_path = temp_file.name

    try:
        # Run mermaid-cli to convert to PNG with HD quality settings
        # -s: scale factor (3 = 3x resolution for HD quality)
        # -w: width (larger width for better quality)
        # -b: transparent background
        result = subprocess.run(
            ['mmdc', '-i', temp_file_path, '-o', output_path,
             '-b', 'transparent', '-s', '3', '-w', '2400'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  ❌ Timeout: Conversion took too long")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
        except:
            pass


def process_file(input_path, output_dir=None):
    """
    Process a Markdown file and extract all Mermaid diagrams as PNGs.

    Args:
        input_path (str): Path to input .md file
        output_dir (str, optional): Directory to save PNG files

    Returns:
        list: List of paths to generated PNG files
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_path.lower().endswith('.md'):
        raise ValueError("Input file must be a .md (Markdown) file")

    # Check if mermaid-cli is installed
    if not check_mermaid_cli():
        raise EnvironmentError(
            "mermaid-cli (mmdc) is not installed.\n"
            "Install it using: npm install -g @mermaid-js/mermaid-cli"
        )

    # Setup output directory
    if output_dir is None:
        output_dir = "./mermaid_images"

    os.makedirs(output_dir, exist_ok=True)

    # Get base name for output files
    base_name = Path(input_path).stem

    # Read input file
    print(f"📖 Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        input_content = f.read()

    # Extract diagrams
    print("🔍 Extracting Mermaid diagrams...")
    diagrams = extract_mermaid_diagrams(input_content)

    if not diagrams:
        print("⚠️  No Mermaid diagrams found in the file")
        return []

    print(f"✅ Found {len(diagrams)} diagram(s)")
    print()

    # Convert each diagram to PNG
    output_files = []
    for diagram_num, diagram_code in diagrams:
        output_filename = f"{base_name}_diagram_{diagram_num}.png"
        output_path = os.path.join(output_dir, output_filename)

        print(f"🎨 Converting diagram {diagram_num}/{len(diagrams)}...")

        if convert_mermaid_to_png(diagram_code, output_path):
            print(f"  ✅ Saved: {output_path}")
            output_files.append(output_path)
        else:
            print(f"  ❌ Failed to convert diagram {diagram_num}")

    print()
    print(f"{'='*60}")
    print(f"🎉 Conversion complete!")
    print(f"📊 Successfully converted: {len(output_files)}/{len(diagrams)} diagrams")
    print(f"📁 Output directory: {os.path.abspath(output_dir)}")
    print(f"{'='*60}")

    return output_files


def main():
    """Main function to handle command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python mermaid_to_png.py input.md [output_dir]")
        print("\nExamples:")
        print("  python mermaid_to_png.py document.md")
        print("  python mermaid_to_png.py document.md ./diagrams")
        print("\nRequirements:")
        print("  - Node.js installed")
        print("  - mermaid-cli: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        process_file(input_path, output_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()