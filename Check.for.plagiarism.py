# author：8891689
import os
import re
from collections import defaultdict

def process_file(file_path, sequence_counts):
    pattern = re.compile(r'R:[a-zA-Z0-9]{63,65}')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                sequences = pattern.findall(line)
                for sequence in sequences:
                    sequence_counts[sequence] += 1
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def find_and_log_duplicates(folder_path, output_file):
    sequence_counts = defaultdict(int)

    # Process each file
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, sequence_counts)

            # Optional: Periodically write intermediate results to disk
            if len(sequence_counts) > 100000:  # Threshold to write intermediate results
                with open(output_file, 'a', encoding='utf-8') as out_f:
                    out_f.write("The following are the repeated sequences and their number of occurrences(starting with 'R:' and with a length between 63 and 65 characters):\n")
                    for sequence, count in sequence_counts.items():
                        if count >= 2:
                            out_f.write(f"sequence: {sequence}, Occurrence: {count}\n")
                sequence_counts.clear()  # Clear in-memory data

    # Write remaining results to output file
    with open(output_file, 'a', encoding='utf-8') as out_f:
        out_f.write("The following are the repeated sequences and their occurrence counts (starting with 'R:' and with lengths between 63 and 65):\n")
        for sequence, count in sequence_counts.items():
            if count >= 2:
                out_f.write(f"sequence: {sequence}, Occurrence: {count}\n")

    return sequence_counts

def main():
    folder_path = os.getcwd()  # Current working directory
    output_file = os.path.join(folder_path, "duplicates_log.txt")
    
    if os.path.exists(output_file):
        os.remove(output_file)  # Clear previous output files

    sequence_counts = find_and_log_duplicates(folder_path, output_file)
    
    if any(count >= 2 for count in sequence_counts.values()):  # Check if there is a sequence with a number of occurrences greater than or equal to 2
        print(f"Results saved to {output_file}")
    else:
        print("No duplicate sequences found。")

    input("Press any key to exit...")

if __name__ == "__main__":
    main()

