from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess
import re
import csv

def isZombie(param):
    # Checks the activity of a GitHub repository based on its pull request history
    if param == -1:
        return -1

    # Extract the repository name from the GitHub URL
    pattern = r"(?<=https:\/\/github\.com\/).*"
    repo = re.search(pattern, param).group(0)

    # Add your GitHub token here
    token = "your_personal_access_token"

    # Command to call Bodega with repository details
    command = "bodegha " + repo + " --verbose --csv --only-predicted --start-date 01-01-2024 --key " + token

    try:
        # Execute the Bodega command and capture output
        results = subprocess.run(args=command, shell=True, check=True, capture_output=True, text=True, encoding="utf-8")
        result = results.stdout.split("\r\n")
        print(results.stdout)
    except subprocess.CalledProcessError as e:
        # Handle repositories with no pull request history
        print(param, " This repository has no pull request history.")
        with open("repos.csv", "a", encoding="utf-8") as toWrite:
            beg_writer = csv.writer(toWrite, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            beg_writer.writerow(["No pull request history in Repo: " + repo])
        return 1

    # Save results to the output file
    with open("repos.csv", "a", encoding="utf-8") as toWrite:
        beg_writer = csv.writer(toWrite, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        beg_writer.writerow(result)

    # Check if the repository is marked "Human" (indicating activity)
    if results.stdout.find("Human") == -1:
        return 1
    return 0


def main():
    # Variables to track the status of mods
    num_alive = 0
    num_dead = 0
    num_zombie = 0
    total_versions = 0

    # Create the output CSV file for mod details
    with open("mods.csv", "w", encoding="utf-8") as toWrite:
        beg_writer = csv.writer(toWrite, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        beg_writer.writerow(["File Beginning: "])

    # Iterate through the first 5 pages of most downloaded mods
    for x in range(1, 6):
        # Setup Selenium WebDriver
        driver = webdriver.Chrome()
        tempurl = "https://www.curseforge.com/minecraft/search?page=" + str(x) + "&pageSize=20&sortBy=total+downloads&class=mc-mods"
        driver.get(tempurl)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Store mod details for the current page
        listings = []

        # Extract information from mod cards
        for rows in soup.find_all("div", class_="project-card"):
            name = rows.find("a", class_="name").get_text()
            downloads = rows.find("ul", class_="details-list").find("li", class_="detail-downloads").get_text()
            latestRelease = rows.find("ul", class_="details-list").find("li", class_="detail-updated").get_text()
            num_version = 0

            # Open the mod's homepage to count the number of versions
            driver2 = webdriver.Chrome()
            tempURL = "https://www.curseforge.com"
            tempURL += rows.find('a', attrs={'href': re.compile("^/minecraft/mc-mods/")}).get('href')
            driver2.get(tempURL)
            potatSoup = BeautifulSoup(driver2.page_source, "html.parser")

            # Count versions listed on the mod's homepage
            for version in potatSoup.find_all("li", attrs={"id": "version-item"}):
                num_version += 1
            version_count = potatSoup.find("li", class_="extra").get_text()
            num_version += int(re.search(r"[\d]+", version_count).group(0))

            # Check if the latest release was in 2024
            if latestRelease.find("2024") > 0:
                try:
                    # Look for GitHub repositories linked on the mod page
                    zombies = potatSoup.find_all("a", attrs={"href": re.compile("^https://github.com/")})
                    for zombie in zombies:
                        zombie_url = zombie.get("href")
                        # Ignore irrelevant links (e.g., sponsors or issues)
                        if zombie_url.find("sponsor") == -1 and zombie_url.find("issues") == -1:
                            repo_stat = isZombie(zombie_url)
                            if repo_stat == 1:
                                # Increment zombie count
                                num_zombie += 1
                                break
                            elif repo_stat == 0:
                                # Increment alive count
                                num_alive += 1
                                break
                except AttributeError:
                    break
                finally:
                    driver2.close()
            else:
                # Increment dead count
                num_dead += 1

            total_versions += num_version
            listings.append([name, downloads, latestRelease, num_version])
            print("Number of Minecraft Versions: ", num_version)

        # Write mod details to the CSV file
        with open("mods.csv", "a", encoding="utf-8") as toWrite:
            writer = csv.writer(toWrite, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerows(listings)

    # Print summary statistics
    print("Alive: ", num_alive)
    print("Dead: ", num_dead)
    print("Zombie: ", num_zombie)
    print("Average Num Versions: ", total_versions / 100.0)

main()
