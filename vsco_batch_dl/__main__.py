import os
import requests
import argparse
from typing import List
from tqdm import tqdm
import re

def loadFile(filepath: str) -> List[str]:
    return [line for line in open(filepath, "r").read().strip().split("\n") if line != ""]

def userExists(user: str) -> bool:
    return requests.get(f"https://vsco.co/{user}/gallery").status_code != 404

def loadAllUserPosts(user: str) -> List[str]:
    user_page = requests.get(f"https://vsco.co/{user}/gallery").text

    content_urls = re.findall(r"\/i\/([0-9a-f]*)", user_page)

    return [f"https://vsco.co/{user}/media/{url}" for url in content_urls]

def parseCDNURL(url: str) -> str:
    page = requests.get(url).text

    cdn_url = re.findall(r'"responsiveUrl":"(.+?(?="))"', page)
    return cdn_url[0]

def main():
    ap = argparse.ArgumentParser(prog="vsco-batch-dl", description="A script for downloading a batch of images from VSCO")
    ap.add_argument("-u", "--user", help="User account to download from")
    ap.add_argument("-f", "--file", help="File containing urls to download from")
    ap.add_argument("-o", "--out", help="Output directory")
    args = ap.parse_args()

    if not args.user and not args.file:
        print("One of --user or --file must be specified")
        exit(1)

    if args.user and args.file:
        print("Only one of --user and --file can be specified at a time")
        exit(1)

    urls = []
    if args.file:
        
        if not os.path.exists(args.file):
            print(f"{args.file} is not a valid filepath")
            exit(1)

        urls = loadFile(args.file)

    else:
        print("Notice: User scraping currently will only grab the \"front page\" of a user. Not all posts")
        if not userExists(args.user):
            print(f"User {args.user} does not exist")
            exit(1)

        urls = loadAllUserPosts(args.user)

    cdn_urls = []

    for url in tqdm(urls, desc="Parsing CDN URLs"):
        cdn_urls.append(parseCDNURL(url))

    outpath = "./"
    if args.out:
        outpath = args.out

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for i, url in tqdm(enumerate(cdn_urls), desc="Downloading"):
        
        body = requests.get(f"https://{url}").content

        with open(f"{outpath}/{i}.png", "wb") as fp:
            fp.write(body)
            fp.close()


if __name__ == "__main__":
    main()
    exit(0)