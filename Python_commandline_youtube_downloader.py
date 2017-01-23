"""
Commandline_youtube_downloader (For osdows)
============================================
Coded By: Jackson Kamya
Email: jacksonkamya48@yahoo.com

This script downloads Music from youtube

Pre-Requirements:
=====================
Python 2.7
BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/download/
pytube: https://pypi.python.org/pypi/pytube/ | https://sourceforge.net/projects/pytube/

Features:
=========
1. Download videos one by one as searched at a prompt
2. Download a list of songs as read line by line from file todownload.txt

You are free to copy and modify this script for your own requirements.

"""

import os
import time
from urllib2 import urlopen
import sys

try:
    from bs4 import BeautifulSoup as bs
    from pytube import YouTube
except:
    print('Please install BeautifulSoup and pytube to run this script')
    # exit is mean to work with intrepter must use sys.exit
    sys.exit(0)

# creating download folder
# output_folder = 'D:/py_jack_downloads'
base_dir = os.path.expanduser("~")
output_folder = os.path.join(base_dir, "Videos", "py_jack_downloads")

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# it's better to ask from the user to provide the path
input_file = "D:/todownload.txt"

# Selecting mode of operation
while True:
    print("A >>> Search songs from the prompt")
    print("B >>> Download songs in the todownload file")

    mode = raw_input('Select Mode: A or B > ').lower()
    if len(mode) > 1 or not (mode.startswith('a') or mode.startswith("b")):
        print('Invalid mode, please try again')
        continue
    break


# Getting youtube search term
def get_search_term():
    while True:
        inpt = raw_input('Enter search term >> ').lower()
        if not inpt:
            print('You didn\'t give us a thing, please try again')
            continue
        srch_terms = inpt.split(' ')
        search = '+'.join(srch_terms)
        break
    return search


# downloading the file
def download(url):
    accepted_resolutions = ['480p', '720p', '360p']
    for resol in accepted_resolutions:
        try:
            vid = YouTube(url).get('mp4', resol)
            # what is the point of breaking this here ?
            # taking the first resol which is 480p and exit ?
            break
        except Exception:
            # what is the point of this check ?
            if resol not in accepted_resolutions:
                print('No video matching any of the qualities required')
                return False
    vid.download(output_folder)
    return True


# Selecting a file from the list
def select_video(soup):
    video_list = []
    for anchor in soup.findAll('a', href=True, title=True):
        link = anchor['href']
        title = anchor['title']
        if(link[:6] == "/watch"):
            video_list.append((link, title))

    print('=' * 30)
    print('Search Results')
    print('=' * 30)

    if not video_list:
        print('No results found')
        return main(mode)
    count = 0
    for l, t in video_list:
        count += 1
        print(str(count) + " >>> " + t)
    while True:
        try:
            # fix pep 8 E501
            selection = int(raw_input('Select from the above list or enter 0 to return to main menu >' )) 
            if(selection > count or selection < 0):
                raise ValueError
            elif(selection == 0):
                return main(mode)
            else:
                return video_list[selection - 1]
        except ValueError:
            # fix pep 8 E501
            print('Input must be a number in between 1-{}, please try again'.format(len(video_list)))


# Getting the file
def get_video(soup):
        File = select_video(soup)
        title = File[1]
        link = File[0]
        vid_url = 'https://www.youtube.com' + link
        print('Downloading ' + title)
        try:
            start_time = time.time()
            if download(vid_url):
                end_time = time.time()
                mins = (end_time - start_time) / 60
                secs = (end_time - start_time) % 60
                # avoid '+' use string formatting instead
                # fix pep 8 E501
                dur = str(round(mins)) + " minutes, " + str(round(secs)) + " seconds"
                print("Downloaded {0} in {1}".format(title, dur))
            else:
                print("Could not download the video")
        except Exception as e:
            print(e)
        return


def downloader(term):
    # Openning youtube search page
        try:
            url = 'https://www.youtube.com/results?search_query=' + term
            html = urlopen(url).read()
        except Exception as e:
            print(e)
            return

        # Obtaining page's soup
        try:
            soup = bs(html, "html.parser")
        except Exception as e:
            print(e)
            return

        # Getting the video
        try:
            get_video(soup)
        except Exception as e:
            print(e)
            return


# Main function of the program
def main(mode):
    if(mode == 'a'):
        while True:
            downloader(get_search_term())
    else:
        f = open(input_file, 'r')
        try:
            files = f.read().split('\n')
        except Exception as e:
            print(e)
            return
        for item in files:
            downloader('+'.join(item.split(' ')))


if __name__ == "__main__":
    main(mode)
