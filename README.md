# WebCrawlerForCS399

This tool is part of a paper written as a requirement for the final project `Collateral Evolution Within Video Game Modding Communities` for the course CS399- Software Ecosystems. 

## Overview
This project contains a web crawler designed to scrape information about Minecraft mods from [CurseForge](https://www.curseforge.com). The script collects data such as mod name, download count, latest release date, and the number of versions available. It also analyzes linked GitHub repositories to classify mods into three categories:
- **Alive**: Actively maintained projects.
- **Zombie**: Projects with some activity but no significant human contribution.
- **Dead**: Projects without any recent updates.

The gathered data is stored in CSV files for further analysis.

---

## Features
- **Automated Web Scraping**: Crawls the most downloaded Minecraft mods from CurseForge.
- **GitHub Repository Analysis**: Classifies repositories linked to the mods as *Alive*, *Zombie*, or *Dead*.
- **CSV Output**: Exports mod details and repository activity to CSV files.

---
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

---

## File Descriptions
### `webcrawler.py`
The script performs the following tasks:
1. Scrapes the first five pages of the most downloaded Minecraft mods from [CurseForge](https://www.curseforge.com).
2. Extracts mod information:
   - Name
   - Download count
   - Latest release date
   - Number of versions available
3. Analyzes linked GitHub repositories to classify the mods into:
   - Alive
   - Zombie
   - Dead
4. Outputs results into CSV files:
   - `mods.csv`: Contains mod details.
   - `repos.csv`: Contains GitHub repository activity data.
