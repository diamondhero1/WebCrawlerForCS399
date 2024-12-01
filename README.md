# WebCrawlerForCS399

This tool is part of a paper written as a requirement for the final project `"Collateral Evolution Within Video Game Modding Communities"` for the course CS399- Software Ecosystems. 

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
```bash
pip install beautifulsoup4 selenium
