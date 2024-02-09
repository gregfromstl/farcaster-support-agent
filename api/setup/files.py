import os

def combine_markdown_files(directory, output_file):
    """
    Reads all markdown files from the given directory and writes their content into a single file.
    
    Args:
    - directory (str): The path to the directory containing markdown files.
    - output_file (str): The path to the output file where the combined content will be written.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return
    
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file is a markdown file
                if file.endswith('.md'):
                    # Construct the full path to the file
                    file_path = os.path.join(root, file)
                    # Open and read the markdown file
                    with open(file_path, 'r') as infile:
                        content = infile.read()
                        # Write the content to the output file
                        outfile.write(content + "\n\n")
    print(f"All markdown files from {directory} have been combined into {output_file}.")

# Example usage
combine_markdown_files('./docs', 'combined_markdown.md')
