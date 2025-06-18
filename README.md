# WebCrawlerForCS399

This tool is part of a paper written as a requirement for the final project `Collateral Evolution Within Video Game Modding Communities` for the course CS399- Software Ecosystems. 

## Overview
This project contains a web crawler designed to scrape information about Minecraft mods from [CurseForge](https://www.curseforge.com). The script collects data such as mod name, download count, latest release date, and the number of versions available. It also analyzes linked GitHub repositories to classify mods into three categories:
- **Alive**: Actively maintained projects.
- **Zombie**: Projects with some activity but no significant human contribution.
- **Dead**: Projects without any recent updates.

The gathered data is stored in CSV files for further analysis.

## Features
- **Automated Web Scraping**: Crawls the most downloaded Minecraft mods from CurseForge.
- **GitHub Repository Analysis**: Classifies repositories linked to the mods as *Alive*, *Zombie*, or *Dead*.
- **CSV Output**: Exports mod details and repository activity to CSV files.


## Prerequisites
### Python Packages
This script requires the following Python libraries:
- `beautifulsoup4`
- `selenium`
- `csv`
- `subprocess`
- `re`

Install them using:
`pip install beautifulsoup4 selenium csv subprocess re`

## Additional Requirements
- **Selenium WebDriver**:  
  Selenium requires a WebDriver to interact with browsers. Download and install ChromeDriver. Ensure the version matches your installed Chrome browser version.  
  - [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)

- **Bodega Tool**:  
  Bodega is used for analyzing GitHub repositories. Ensure Bodega is installed and configured correctly, and use a valid GitHub personal access token for authentication.  
  - [Bodega Repository](https://github.com/mehdigolzadeh/BoDeGHa)


## Usage
1. Clone the repository:\
   `git clone https://github.com/diamondhero1/WebCrawlerForCS399.git`\
   `cd WebCrawlerForCS399`

2. Install the required Python libraries

3. Download and install ChromeDriver. Ensure it matches your installed Chrome version and is added to your system's PATH.\
   `Download ChromeDriver`

4. Update the isZombie function in webcrawler.py with your GitHub personal access token.


## Ouput 

The output results into csv files:
- `mods.csv`: Contains mod details.
- `repos.csv`: Contains GitHub repository activity data.

