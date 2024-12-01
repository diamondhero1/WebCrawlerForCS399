# WebCrawlerForCS399

This tool is part of a paper written as a requirement for the final project of CS399- Software Ecosystems. 

## Overview
This project contains a web crawler designed to scrape information about Minecraft mods from [CurseForge](https://www.curseforge.com). The script collects data such as mod name, download count, latest release date, and the number of versions available. It also analyzes linked GitHub repositories to classify mods into three categories:
- **Alive**: Actively maintained projects.
- **Zombie**: Projects with some activity but no significant human contribution.
- **Dead**: Projects without any recent updates.

The gathered data is stored in CSV files for further analysis.
