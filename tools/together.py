import os
from pathlib import Path

def concatenate_dialog_files(output_file='combined_dialog.txt'):
    base_dir = Path.cwd()
    dialog_files = [f for f in base_dir.rglob('*.txt') if f.stem.endswith('dialog')]
    
    with open(base_dir / output_file, 'w', encoding='utf-8') as outfile:
        for txt_file in dialog_files:
            try:
                with open(txt_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
            except UnicodeDecodeError:
                try:
                    with open(txt_file, 'r', encoding='cp1252') as infile:
                        content = infile.read()
                except UnicodeDecodeError:
                    print(f"Skipping {txt_file}: Unable to decode")
                    continue
            
            outfile.write(f'### File: {txt_file.name} ###\n')
            outfile.write(content + '\n\n')

if __name__ == '__main__':
    concatenate_dialog_files()
