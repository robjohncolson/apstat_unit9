import csv
import os
import glob

def find_tsv_files():
    # Look for files with .tsv extension in current and subdirectories
    tsv_files = []
    
    # Get the script's directory and go up one level
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Walk through directory tree starting from parent directory
    print("\nSearching for TSV files...")
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.tsv'):
                full_path = os.path.join(root, file)
                tsv_files.append(full_path)
                print(f"- {full_path}")
    
    if tsv_files:
        return tsv_files
    
    print("\nNo .tsv files found. Please ensure your tab-delimited files have the .tsv extension.")
    return []

def process_tsv_to_csv():
    input_files = find_tsv_files()
    
    if not input_files:
        print("No suitable input files found. Please ensure you have tab-delimited text files available.")
        return

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write Blooket template headers
        writer.writerow(BLOOKET_TEMPLATE_HEADER_ROW)
        writer.writerow(COLUMN_HEADERS)

        question_number = 1
        for tsv_file in input_files:
            if not os.path.exists(tsv_file):
                print(f"Skipping non-existent file: {tsv_file}")
                continue

            try:
                with open(tsv_file, 'r', encoding='utf-8') as tsvfile:
                    reader = csv.DictReader(tsvfile, delimiter='\t')
                    
                    # Validate TSV structure
                    required_columns = {'Question Text', 'Answer 1', 'Answer 2', 
                                      'Correct Answer(s)', 'Time Limit (sec)'}
                    if not required_columns.issubset(reader.fieldnames):
                        print(f"Skipping invalid TSV: {tsv_file}")
                        print(f"Missing required columns. Found: {reader.fieldnames}")
                        continue

                    for row in reader:
                        # Skip empty rows
                        if not row.get('Question Text', '').strip():
                            continue

                        # Process answers, handling optional fields
                        answers = [
                            row['Answer 1'].strip(),
                            row['Answer 2'].strip(),
                            row.get('Answer 3', '').strip(),
                            row.get('Answer 4', '').strip()
                        ]

                        # Get correct answers (handle comma-separated values)
                        correct_answers = row['Correct Answer(s)'].strip().replace(" ", "")
                        
                        # Build CSV row with proper formatting
                        csv_row = [
                            question_number,
                            row['Question Text'].strip(),
                            *answers[:4],  # Unpack first 4 answers
                            row.get('Time Limit (sec)', '60').strip(),
                            correct_answers
                        ]
                        
                        # Add empty columns to reach 23 total
                        csv_row += [""] * (23 - len(csv_row))
                        writer.writerow(csv_row)
                        question_number += 1

            except Exception as e:
                print(f"Error processing {tsv_file}: {str(e)}")
                continue

    print(f"\nSuccessfully generated {OUTPUT_CSV} with {question_number-1} questions")

# Constants remain the same
OUTPUT_CSV = input("Enter the first part of the output filename (e.g. o3minihi): ") + "_blooket_questions.csv"
BLOOKET_TEMPLATE_HEADER_ROW = ["Blooket Import Template"] + [""] * 22
COLUMN_HEADERS = [
    "Question #",
    "Question Text",
    "Answer 1",
    "Answer 2",
    "Answer 3\n(Optional)",
    "Answer 4\n(Optional)",
    "Time Limit (sec)\n(Max: 300 seconds)",
    "Correct Answer(s)\n(Only include Answer #)"
] + [""] * 15

if __name__ == "__main__":
    process_tsv_to_csv()