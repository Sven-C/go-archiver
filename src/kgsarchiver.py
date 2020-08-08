#!env/bin/python3

import sys
import os
import requests
import zipfile
import argparse
import bs4

from timestamp import Timestamp

def downloadZip(url, downloadDirectory, outputDirectory):
    def getZipFilename(url):
        return url.split("/")[-1]
    print("Downloading zipfile from", url)
    req = requests.get(url)
    if req.status_code != 200:
        return

    tmpFilename = os.path.join(downloadDirectory, getZipFilename(url))
    with open(tmpFilename, "wb") as f:
        f.write(req.content)
    unpackZip(tmpFilename, outputDirectory)
    os.remove(tmpFilename)

def unpackZip(zipFileName, directory):
    print("Unpacking zipfile", zipFileName, "to", directory)
    with zipfile.ZipFile(zipFileName) as zf:
        for fileInfo in zf.infolist():
            filename = os.path.normpath(os.path.join(directory, fileInfo.filename))
            if os.path.commonpath((filename, directory)) == directory:
                print("Extracting file", fileInfo)
                try:
                    os.makedirs(os.path.dirname(filename))
                except FileExistsError:
                    pass
                with open(filename, 'wb') as fh:
                    fh.write(zf.open(fileInfo.filename, "r").read())

def extractBeginAndEndData(name):
    def html():
        HOST = "https://www.gokgs.com/gameArchives.jsp"
        params = {
                "oldAccounts":"y",
                "user":name
                }
        req = requests.get(HOST, params=params)
        return req.text
    htmlDoc = html()
    earliestTimestamp = None
    latestTimestamp = None

    soup = bs4.BeautifulSoup(htmlDoc, "html.parser")
    allLinks = map(lambda a: a.get('href'), soup.find_all('a'))

    for link in allLinks:
        if "month" in link and "year" in link:
            parts = link.split("&")
            month = [int(x.split("=")[1]) for x in parts if "month" in x][0]
            year = [int(x.split("=")[1]) for x in parts if "year" in x][0]
            timestamp = Timestamp(month, year)
            
            if earliestTimestamp == None or timestamp < earliestTimestamp:
                earliestTimestamp = timestamp
            if latestTimestamp == None or latestTimestamp < timestamp:
                latestTimestamp = timestamp

    # Adjust latest timestamp, because the current page does not have an href
    # The page we download shows by default the games played in the current month
    latestTimestamp = Timestamp.next(latestTimestamp)
    return earliestTimestamp, latestTimestamp

def dlGamesTimestamp(name, downloadDirectory, outputDirectory, timestamp):
    url = "https://www.gokgs.com/servlet/archives/en_US/{}-all-{}-{}.zip".format(name, timestamp.year, timestamp.month)
    downloadZip(url, downloadDirectory, outputDirectory)

def dlGames(name, outputDirectory, start, end):
    print("Downloading games of player {} to {}".format(name, outputDirectory))
    try:
        os.makedirs(outputDirectory)
    except FileExistsError as err:
        pass
    TMP_DIR = "/tmp/kgsarchiver"
    if not os.path.isdir(TMP_DIR):
        os.makedirs(TMP_DIR)
    earliestTimestamp, latestTimestamp = extractBeginAndEndData(name)

    start = earliestTimestamp if start < earliestTimestamp else start
    end = end if end < latestTimestamp else latestTimestamp

    for timestamp in Timestamp.range(start, end):
        dlGamesTimestamp(name, TMP_DIR, outputDirectory, timestamp)
    
def parseArgs():
    parser = argparse.ArgumentParser(description="Download game archives from KGS.")
    parser.add_argument("nickname", help="The nickname of the player whose archive you want to download.")
    parser.add_argument("-o", "--output", default=None, help="Directory where the games get stored. Defaults to nickname.")
    parser.add_argument("--start", default="01/1900", help="Download games played since the start date. Format: MM/YYYY.")
    parser.add_argument("--end", default="01/9999", help="Download games played up to the end date. Format: MM/YYYY.")

    return parser.parse_args()

def main():
    INCORRECT_USAGE = 1
    args = parseArgs()

    if args.output == None:
        args.output = args.nickname
    start = Timestamp.parse(args.start)
    end = Timestamp.parse(args.end)
    if (start > end):
        print("End date should be after start date.")
        exit(INCORRECT_USAGE)
    outputDirectory = os.path.abspath(args.output)
    dlGames(args.nickname, outputDirectory, start, end)

if __name__ == "__main__":
    main()
