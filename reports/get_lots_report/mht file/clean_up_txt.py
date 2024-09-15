def clean_text_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove leading/trailing spaces and blank lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

# Example usage
input_file_path = 'output copy.txt'
output_file_path = 'output_trimmed.txt'
clean_text_file(input_file_path, output_file_path)