# Writer's Corner

This repository is home to a collection of scripts and tools I have and will develop to assist with the book-writing process.

## Table of Contents

- [Introduction](#Introduction)
- [Getting Started](#getting-started)
- [Scripts and Tools](#scripts-and-tools)

## Introduction - UNDER CONSTRUCTION

## Getting Started

### Prerequisites

Most of the tools and scripts are developed in Python, the latest release of which can be found [here](https://www.python.org/downloads/).

For completeness, each script is accompanied by it's own metadata, which details specific requirements. If required, a requirements.txt will be provided as well for ease of use. I would recommend using a virtual environment with these scripts.

### Installation

 1. Clone the repository to your local machine:

```sh
git clone https://github.com/Numberedlemon/writers-corner
```

 2. Navigate to the repository directory:

```sh
cd writers-corner
```

 3. Install requirements as per script header.

```sh
pip install -r requirements.txt
```

## Scripts and Tools

### Excel-to-Markdown Converter

A tool for converting a tabulated scene-by-scene plan of a novel or story into a markdown-based chapter-by-chapter plan. For more information on this script, it's intended use, see the header of ```excel_to_markdown.py```

### Common Words Tool

This simple script extracts the 100 most common words in your text, supplied by .csv summary files which can provided by an editor such as TeXstudio. It can also display a bar chart for visualisation of this data.

### Word Count Dashboard

This tool allows for tracking of scene counts within chapters, their associated word counts, and predicted word counts at scene number milestones. 

This tool will eventually be linked to another tool which will act as a kind of database management script.

