#!/usr/bin/env python3
"""
Markdown to Confluence Converter
Converts Markdown files to Confluence-compatible Markdown format (.txt)

Usage:
    python md_to_confluence.py input.md [output.txt]
    
If output file is not specified, it will create: input-Confluence.txt
"""

import sys
import re
import os


def convert_md_to_confluence(input_content):
    """
    Convert Markdown content to Confluence-compatible format.
    
    Args:
        input_content (str): Original Markdown content
        
    Returns:
        str: Confluence-compatible Markdown content
    """
    lines = input_content.split('\n')
    converted_lines = []
    in_code_block = False
    code_language = None
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                # Starting code block
                in_code_block = True
                # Extract language if specified
                code_language = line.strip()[3:].strip()
                if code_language:
                    converted_lines.append(f'```{code_language}')
                else:
                    converted_lines.append('```')
            else:
                # Ending code block
                in_code_block = False
                code_language = None
                converted_lines.append('```')
            continue
        
        # Don't process lines inside code blocks
        if in_code_block:
            converted_lines.append(line)
            continue
        
        # Convert headers (already in standard format, just keep them)
        if line.startswith('#'):
            converted_lines.append(line)
            continue
        
        # Convert tables (already in standard format, just keep them)
        if line.strip().startswith('|'):
            converted_lines.append(line)
            continue
        
        # Convert horizontal rules
        if line.strip() in ['---', '***', '___']:
            converted_lines.append('---')
            continue
        
        # Keep everything else as-is (bullets, numbered lists, text, etc.)
        converted_lines.append(line)
    
    return '\n'.join(converted_lines)


def process_file(input_path, output_path=None):
    """
    Process a Markdown file and convert it to Confluence format.
    
    Args:
        input_path (str): Path to input .md file
        output_path (str, optional): Path to output .txt file
        
    Returns:
        str: Path to the output file
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not input_path.lower().endswith('.md'):
        raise ValueError("Input file must be a .md (Markdown) file")
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}-Confluence.txt"
    
    # Read input file
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        input_content = f.read()
    
    # Convert content
    print("Converting to Confluence-compatible format...")
    output_content = convert_md_to_confluence(input_content)
    
    # Write output file
    print(f"Writing: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"✅ Conversion complete!")
    print(f"Output file: {output_path}")
    
    return output_path


def main():
    """Main function to handle command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python md_to_confluence.py input.md [output.txt]")
        print("\nExample:")
        print("  python md_to_confluence.py document.md")
        print("  python md_to_confluence.py document.md custom-output.txt")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        process_file(input_path, output_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
