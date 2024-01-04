import os
import markdown

file_path = 'README.md'

def markdown_parser(file_path):
    with open(file_path) as f:
        print(f.readlines())

if __name__ == "__main__":
    markdown_parser(file_path)