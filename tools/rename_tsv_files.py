import os
import glob

def rename_tsv_files():
    # Find all .txt files in current directory and subdirectories
    txt_files = glob.glob('**/*.txt', recursive=True)
    
    # Filter for files with '_tsv' in their name
    tsv_files = [f for f in txt_files if '_tsv' in f]
    
    # Rename each file
    for txt_file in tsv_files:
        # Create new filename by replacing .txt with .tsv
        tsv_file = txt_file.replace('.txt', '.tsv')
        
        try:
            os.rename(txt_file, tsv_file)
            print(f'Renamed: {txt_file} -> {tsv_file}')
        except OSError as e:
            print(f'Error renaming {txt_file}: {e}')

if __name__ == '__main__':
    rename_tsv_files() 