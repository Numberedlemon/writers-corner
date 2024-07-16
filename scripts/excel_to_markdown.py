"""
Tool Name: Excel-to-Markdown
Description: This script converts a tabulated scene-by-scene plan of a novel into a chapter-by-chapter markdown-based plan.

Usage:
    python excel-to-markdown.py [options]

Positional Arguments:
    input_file              Path to the input Excel file.
    output_dir              Path to the output directory.

Optional Arguments:
    -h, --help                          Show this help message and exit.
    -s, --sheet            <str>        Sheet name or index to read from the Excel file (default: 0).
    -l, --log_file         <str>        Path to the log file (default: log.log).
    -am, add_metadata      <bool>       Add metadata to .md file header? (default: False, requires --tags)
    -t, --tags             <str>        Tags to add to file header. Must be separated by comma and space (default: None).
    -g, --generate_metrics <bool>       Generate descriptive statistics and metrics? (default: False, requires matplotlib).
    -S, --save             <bool>       Save generated metrics? (default: False, requires -g to be True, does nothing otherwise).

External Dependencies:
    - pandas
    - matplotlib (soft requirement. Only if generate_metrics is true)

"""

import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse
from collections import Counter
import sys
from datetime import datetime
import os

def setup_logging(log_file):
    """Sets up the logging configuration."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s->%(funcName)s():%(lineno)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w'
    )
    
def get_number_of_rows(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        num_rows = df.shape[0]
        return num_rows
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file {file_path}: {e}")
        return None

def read_excel_file(file_path, sheet_name):
    
    """Reads the Excel file and returns a DataFrame."""
    
    logging.info(f"Attempting to parse sheet: '{sheet_name}' in file: '{file_path}'.")
    print(f"Attempting to parse sheet: '{sheet_name}' in file: '{file_path}'.")
    
    try:
        df = pd.read_excel(file_path, sheet_name = sheet_name)
        print(f"Successfully read sheet: '{sheet_name}' in file: '{file_path}'.")
        logging.info(f"Successfully read sheet: '{sheet_name}' in file: '{file_path}'.")
        return df
    
    except FileNotFoundError:
        print(f"\nError: The file {file_path} could not be found.")
        logging.error(f"Error: The file '{file_path}' could not be found.")
        sys.exit(1)
        
        
    except IOError as e:
        print(f"\nError: An error occurred while reading {file_path}. Please check that the file is not open in another program.")
        logging.error(f"Error: An error occurred while reading {file_path}. Please check that the file is not open in another program.")
        sys.exit(1)
        
        
    except Exception as e:
        print(f"\nError: An error occurred while reading sheet: '{sheet_name}' in file: '{file_path}': {e}")
        logging.error(f"Error: An error occurred while reading sheet: '{sheet_name}' in file: '{file_path}': {e}")
        sys.exit(1)
        
        
def parse_scenes(df, num_rows):
    
    logging.info(f"Parsing {num_rows} scenes.")
    
    try:
        chapters = {}
        for index, row in df.iterrows():
            week = row["Week"]
            arc = row["Arc"]
            chapter = row["Chapter"]
            setting = row["Location"]
            uniform = row["Uniform"]
            time = row["Time"]
            weather = row["Weather"]
            day = row["Day"]
            description = row['Description']
            pov = row["POV"]
            temp = row["Temperature"]
            
            if chapter not in chapters:
                    chapters[chapter] = {'scenes': [], 'settings': [], 'scene_counter': 1, 'day': [], 'POV': '', 'description': '', 'time': [], 'weather': [], 'descriptions': [], 'uniform': [], 'arc': 1, 'week': []}

            chapters[chapter]['scenes'].append(chapters[chapter]['scene_counter'])
            chapters[chapter]['arc'] = arc
            chapters[chapter]['scene_counter'] += 1
            chapters[chapter]['day'].append(day)
            chapters[chapter]['settings'].append(setting)
            chapters[chapter]['uniform'].append(uniform)
            chapters[chapter]['weather'].append(weather)
            chapters[chapter]['time'].append(time)
            chapters[chapter]['descriptions'].append(description)
            chapters[chapter]["POV"] = pov
            chapters[chapter]["temperature"] = temp
            chapters[chapter]["week"].append(week)

                
        logging.info(f"Successfully parsed {num_rows} scenes into {len(chapters)} chapters.")
               
        return chapters
    except Exception as e:
        print(f"Error: An error occurred while parsing scenes: {e}")
        logging.error(f"Error: An error occurred while parsing scenes: {e}")
        
def generate_markdown_content(chapters, tags, output_dir, am = True):
    """Generates Markdown content from the parsed data."""
    
    logging.info(f"Generating .md markdown files for {len(chapters)} chapters.")
    
    try:
        
        for chapter_key, chapter_data in chapters.items():
            
            markdown_content = ''

            # add metadata
            if am == True:
                markdown_content = add_metadata(markdown_content, pov = chapter_data["POV"], tags = ", ".join(tags), arc = chapter_data["arc"])
            
            markdown_content += f"# Chapter {chapter_key}\n"
            
            scenes = chapter_data["scenes"]
            days = chapter_data["day"]
            descriptions = chapter_data["descriptions"]
            pov = chapter_data["POV"]
            uniform = chapter_data["uniform"]
            weather = chapter_data["weather"]
            settings = chapter_data["settings"]
            time = chapter_data["time"]
            temp = chapter_data["temperature"]
            week = chapter_data["week"]
            
            markdown_content += f"## Scenes\n"
        
            for i in range(len(scenes)):
                scene_number = i + 1
                
                markdown_content += f"### Scene {scene_number}\n\n"
                markdown_content += f" - POV: {pov}\n"
                markdown_content += f" - Date and Time: {time[i]}\n" 
                markdown_content += f" - Day: {days[i]}\n"
                markdown_content += f" - Week: {week[i]}\n"
                markdown_content += f" - Temperature: {temp}\n"
                markdown_content += f" - Weather: {weather[i]}\n"
                markdown_content += f" - Uniform: {uniform[i]}\n\n"
                markdown_content += f" - Description: {descriptions[i]}\n\n"
                
                markdown_content += f" #### Setting:\n"
                
                parts = settings[i].split(". ")

                for subpart in parts:
                    subsubparts = subpart.split(" - ")
                    major_loc = subsubparts[0]
                    markdown_content += f" - {major_loc}\n"
                    for i in range(1, len(subsubparts)):
                        min_locs = subsubparts[i].split(", ")
                        for j in min_locs:
                            pass
                            markdown_content += f"     - {j}\n"
                            
                markdown_content += "\n"
              
            logging.info(f"Chapter {chapter_key}, Scene {scene_number} created.") 
            
            write_markdown(f"Chapter {chapter_key}", output_dir = output_dir, content = markdown_content)              
    except Exception as e:
        logging.error(f"Error: An error occured while parsing Chapter {chapter_key}, Scene {scene_number}: {e}")
        print(f"Error: An error occured while parsing Chapter {chapter_key}, Scene {scene_number}: {e}")
        
def add_metadata(markdown_content, arc, pov, tags):
            markdown_content += f'---\n'
            markdown_content += f'created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n'
            markdown_content += f'generated_by: {os.path.basename(__file__)}\n'
            markdown_content += f'tags: {tags}\n'
            markdown_content += f'POV: {pov}\n'
            markdown_content += f'Arc: {arc}\n'
            markdown_content += f'---\n\n'

            return markdown_content

def write_markdown(file_path, output_dir, content):
    """Writes a .md markdown file"""
    logging.info(f"Writing .md file at '/{output_dir}/{file_path}.md'")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(f"./{output_dir}/{file_path}.md", 'w') as file:
            file.write(content)
        logging.info(f"Markdown file saved successfully: '/{output_dir}/{file_path}.md'")
    except Exception as e:
        logging.error(f"Error: An error occurred while saving the file '/{output_dir}/{file_path}.md': {e}")
        print(f"Error: An error occurred while saving the file '/{output_dir}/{file_path}.md': {e}")
        
def generate_metrics(df, save, output_dir):
    
    days = df["Day"]
    
    # Count the occurrences of each unique string
    counter = Counter(days)
    labels, counts = zip(*counter.items())

    # Bar Chart
    plt.figure(figsize=(10, 5))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Count')
    plt.title('Days of the Week')

    if save == True:
        if not os.path.exists(f"{output_dir}/images/"):
            os.makedirs(f"{output_dir}/images/")
        else:
            pass
        plt.savefig(f"{output_dir}/images/days.png")
        plt.show()

def parse_items(value):
    """For argparser to process comma-separated string."""
    return [item.strip() for item in value.split(',')]
    
def main():
    parser = argparse.ArgumentParser(description="Convert excel planning sheet into .md for Obsidian")
    parser.add_argument('input_file', type=str, help="Path to the input Excel file.")
    parser.add_argument('output_dir', type=str, help="Path to the output directory.")
    parser.add_argument('-s', '--sheet', type=str, default=0, help="Sheet name or index to read from the Excel file (default: 0).")
    parser.add_argument('-l', '--log_file', type=str, default='log.log', help="Path to the log file (default: log.log).")
    parser.add_argument('-am','--add_metadata', type = bool, default = False, help = "Add metadata to file header? (default: False, requires --tags).")
    parser.add_argument('-t', '--tags', type = parse_items, help = "Tags to add to file header. (default: "")")
    parser.add_argument('-g', '--generate_metrics', type = bool, default = False, help = "Generate descriptive statistics and metrics? (default: False, requires matplotlib).")
    parser.add_argument('-S', '--save', type = bool, default = False, help = "Save generated metrics? (default: False, requires -g to be True, does nothing otherwise).")
    
    args = parser.parse_args()
    
    setup_logging(f"logs/{args.log_file}")
    
    logging.info("Script started")
    print("Script started.")

    df = read_excel_file(args.input_file, args.sheet)

    num_rows = get_number_of_rows(args.input_file, args.sheet)

    chapters = parse_scenes(df, num_rows = num_rows)

    generate_markdown_content(chapters, tags = args.tags, am = args.add_metadata, output_dir = args.output_dir)

    if args.generate_metrics == True:
        generate_metrics(df, args.save, args.output_dir)
    else:
        pass
    
    logging.info(f"Script complete. Excel file: '{args.input_file}' converted to {len(chapters)} .md files.")
    print(f"Script complete. Excel file: '{args.input_file}' converted to {len(chapters)} .md files.")
    
if __name__ == "__main__":
    main()
