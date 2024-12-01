from bs4 import BeautifulSoup
import requests
import os, os.path, csv

from selenium import webdriver
import subprocess
import re
bot_occurances = 0
def isZombie(param):
    global bot_occurances
    if param == -1:
        return -1
    pattern = r"(?<=\/)([a-zA-Z0-9_-]+)\/([a-zA-Z0-9_-]+)"
    repo = re.search(pattern, param)
    repo = repo.group(0)
    print(repo)
    token = "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"#add your own token here
    command = "bodegha " + repo + " --verbose --csv --start-date 01-01-2024 --key " + token
    try:
        results = subprocess.run(args=command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
        result = results.stdout.split("\r\n")
        bot_occurances += results.stdout.count("Bot")
    except subprocess.CalledProcessError as e:
        print("Bodegha Error: ", e)
        print(param, " Repository/Committers are not active enough to determine if they are a bot")
        with open("repos.csv", 'a', encoding = 'utf-8') as toWrite:
            beg_writer = csv.writer(toWrite, delimiter =",", quoting=csv.QUOTE_MINIMAL)
            beg_writer.writerow(list("No pull request history in Repo: " + repo))
        return -1
    with open("repos.csv", 'a', encoding = 'utf-8') as toWrite:
        beg_writer = csv.writer(toWrite, delimiter =",", quoting=csv.QUOTE_MINIMAL)
        beg_writer.writerow(list(result))
    if results.stdout.find("Human") == -1 and results.stdout.find("Bot") != -1:
        return 1
    return 0
    pass


def main():
    #These four variables keep track of number of alive, dead, and zombie projects as well as the total number of versions of all projects
    num_alive = 0
    num_dead = 0
    num_zombie = 0
    num_unsure = 0
    total_versions = 0
    graph_data = []

    with open("mods.csv", 'w', encoding = 'utf-8') as toWrite:
        beg_writer = csv.writer(toWrite, delimiter =",",quoting=csv.QUOTE_MINIMAL)
    for x in range (1, 11):


        #This allows us to scrape each mod on the first 5 pages of the most downloaded mods
        driver = webdriver.Chrome()
        tempurl = "https://www.curseforge.com/minecraft/search?page=" + str(x) + "&pageSize=20&sortBy=total+downloads&class=mc-mods"
        driver.get(tempurl)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        #Listings is used to keep track of datapoints about individual mods
        listings = []
        batch_alive = 0
        batch_dead = 0
        batch_zombie = 0
        batch_unsure = 0

        for rows in soup.find_all("div", class_="project-card"):
            #We decided to collected the name, downloads, latest release, and number of releases of each mod
            name = rows.find("a", class_= "name").get_text()
            downloads = rows.find("ul", class_= "details-list").find("li", class_="detail-downloads").get_text()
            latestRelease = rows.find("ul", class_= "details-list").find("li", class_="detail-updated").get_text()
            creationDate = rows.find("ul", class_= "details-list").find("li", class_="detail-created").get_text()
            num_version = 0

            #This opens up the mods homepage on curseforge in order to get num_version
            driver2 = webdriver.Chrome()
            tempURL = "https://www.curseforge.com"
            tempURL += rows.find('a', attrs={'href': re.compile("^/minecraft/mc-mods/")}).get('href')
            driver2.get(tempURL)
            potatSoup = BeautifulSoup(driver2.page_source, "html.parser")
            for version in potatSoup.find_all("li", attrs={'id':"version-item"}):
                num_version += 1
            try:
                version_count = potatSoup.find("li", class_="extra").get_text()
                num_version += int(re.search("[\d]+", version_count).group(0))
            except AttributeError:
                print("No Extra")

            #If the latest release was in 2024 then we must determine if it is a zombie or if it is alive
            if(latestRelease.find("2024")>0):
                try:
                    zombies = potatSoup.find_all('a')
                    for zombie in zombies:
                        if(zombie.get_text() == "Source"):
                            zombie_url = zombie.get('href')
                            if zombie_url.find("sponsor") == -1:
                                repo_stat = isZombie(zombie_url)
                                if(repo_stat == 1):
                                    # If Repo Stat == 1 then the isZombie() function determined it to be a zombie
                                    num_zombie +=1
                                    batch_zombie += 1
                                    break
                                elif repo_stat == 0:
                                    num_alive += 1
                                    batch_alive += 1
                                    break
                                else:
                                    num_unsure += 1
                                    batch_unsure += 1
                                    print("Not enough data to classify commenters/no comments found")
                                    break
                except AttributeError as e:
                    print("Attribute Error at: ", e)
                    break
                driver2.close()

            else:
                num_dead += 1
                batch_dead += 1
            total_versions = total_versions + num_version
            listings.append([name, downloads, latestRelease, creationDate, num_version])
            print("Number of Minecraft Versions: ", num_version)
        graph_data.append([batch_alive, batch_dead, batch_zombie, batch_unsure])


        with open("mods.csv", 'a', encoding = 'utf-8') as toWrite:
            fieldnames = ['name', 'downloads', 'latest_release', 'creation_date', 'num_versions']
            writer = csv.DictWriter(toWrite, fieldnames=fieldnames)
            for row in listings:
                writer.writerow({'name': row[0], 'downloads': row[1], 'latest_release': row[2], 'creation_date': row[3], 'num_versions': row[4] })
    print("Alive: ", num_alive)
    print("Dead: ", num_dead)
    print("Zombie: ", num_zombie)
    print("Unsure: ", num_unsure)
    print("Average Num Versions: ", total_versions / 200.0)
    print("Graph Data: ", graph_data)
    with open("mods.csv", 'a', encoding = 'utf-8') as toWrite:
        writer = csv.writer(toWrite, delimiter =",", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Number Alive: " + str(num_alive), "Number Dead: " + str(num_dead),
                         "\n Number of Zombies" + str(num_zombie), "Number Unsure: " + str(num_unsure), total_versions])

main()