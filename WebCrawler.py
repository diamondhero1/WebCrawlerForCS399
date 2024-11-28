from bs4 import BeautifulSoup
import requests
import os, os.path, csv

from selenium import webdriver
import subprocess
import re

def isZombie(param):
    if param == -1:
        return -1
    pattern = r"(?<=https:\/\/github\.com\/).*"
    repo = re.search(pattern, param)
    repo = repo.group(0)
    token = #add your own token here
    command = "bodegha " + repo + " --verbose --csv --only-predicted --start-date 01-01-2024 --key " + token
    try:
        results = subprocess.run(args=command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
        result = results.stdout.split("\r\n")
        print(results.stdout)
    except subprocess.CalledProcessError as e:
        print(param, " This repository has no thing I think")
        with open("repos.csv", 'a', encoding = 'utf-8') as toWrite:
            beg_writer = csv.writer(toWrite, delimiter =",", quoting=csv.QUOTE_MINIMAL)
            beg_writer.writerow(list("No pull request history in Repo: " + repo))
        return 1
    with open("repos.csv", 'a', encoding = 'utf-8') as toWrite:
        beg_writer = csv.writer(toWrite, delimiter =",", quoting=csv.QUOTE_MINIMAL)
        beg_writer.writerow(list(result))
    if results.stdout.find("Human") == -1:
        return 1
    return 0
    pass


def main():
    #These four variables keep track of number of alive, dead, and zombie projects as well as the total number of versions of all projects
    num_alive = 0
    num_dead = 0
    num_zombie = 0
    total_versions = 0

    with open("mods.csv", 'w', encoding = 'utf-8') as toWrite:
        beg_writer = csv.writer(toWrite, delimiter =",",quoting=csv.QUOTE_MINIMAL)
        beg_writer.writerow(list("File Beginning: "))
    for x in range (1, 6):

        #This allows us to scrape each mod on the first 5 pages of the most downloaded mods
        driver = webdriver.Chrome()
        tempurl = "https://www.curseforge.com/minecraft/search?page=" + str(x) + "&pageSize=20&sortBy=total+downloads&class=mc-mods"
        driver.get(tempurl)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        #Listings is used to keep track of datapoints about individual mods
        listings = []

        for rows in soup.find_all("div", class_="project-card"):
            #We decided to collected the name, downloads, latest release, and number of releases of each mod
            name = rows.find("a", class_= "name").get_text()
            downloads = rows.find("ul", class_= "details-list").find("li", class_="detail-downloads").get_text()
            latestRelease = rows.find("ul", class_= "details-list").find("li", class_="detail-updated").get_text()
            num_version = 0

            #This opens up the mods homepage on curseforge in order to get num_version
            driver2 = webdriver.Chrome()
            tempURL = "https://www.curseforge.com"
            tempURL += rows.find('a', attrs={'href': re.compile("^/minecraft/mc-mods/")}).get('href')
            driver2.get(tempURL)
            potatSoup = BeautifulSoup(driver2.page_source, "html.parser")
            for version in potatSoup.find_all("li", attrs={'id':"version-item"}):
                num_version += 1
            version_count = potatSoup.find("li", class_="extra").get_text()
            num_version += int(re.search("[\d]+", version_count).group(0))

            #If the latest release was in 2024 then we must determine if it is a zombie or if it is alive
            if(latestRelease.find("2024")>0):
                try:
                    zombies = potatSoup.find_all("a", attrs={'href': re.compile("^https://github.com/")})
                    for zombie in zombies:
                        zombie_url = zombie.get('href')
                        if zombie_url.find("sponsor") == -1 & zombie_url.find("issues") == -1:
                            repo_stat = isZombie(zombie_url)
                            if(repo_stat == 1):
                                # If Repo Stat == 1 then the isZombie() function determined it to be a zombie
                                num_zombie +=1
                                break
                            elif repo_stat == 0:
                                num_alive += 1
                                break
                except AttributeError:
                    break
                driver2.close()
            else:
                num_dead = num_dead + 1
            total_versions = total_versions + num_version
            listings.append([name, downloads, latestRelease, num_version])
            print("Number of Minecraft Versions: ", num_version)


        with open("mods.csv", 'a', encoding = 'utf-8') as toWrite:
            writer = csv.writer(toWrite, delimiter =",",quoting=csv.QUOTE_MINIMAL)
            for row in listings:
                writer.writerow(row)
    print("Alive: ", num_alive)
    print("Dead: ", num_dead)
    print("Zombie: ", num_zombie)
    print("Average Num Versions: ", total_versions / 100.0)


main()