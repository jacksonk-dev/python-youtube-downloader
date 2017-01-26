"""
Commandline_youtube_downloader
============================================
Coded By: Jackson Kamya
Email: jacksonkamya48@yahoo.com
This script downloads Music from youtube
Pre-Requirements:
=====================
Python 2.7
BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/download/
pytube: www.pypi.python.org/pypi/pytube/ | www.sourceforge.net/projects/pytube/
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
import re

try:
    from bs4 import BeautifulSoup as bs
    from pytube import YouTube
except:
    print('Please install BeautifulSoup and pytube to run this script')
    sys.exit(0)

# creating download folder
base_dir = os.path.expanduser("~")
output_folder = os.path.join(base_dir, "Downloads", "py_cmd_utube_downloads")

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

downloaded_resol = ''
# Getting youtube search term
def get_search_term():
    while True:
        inpt = raw_input('Enter search term\nor press <<Enter>> to change mode: > ').lower()
        if not inpt:
            return main('b')
        srch_terms = inpt.split(' ')
        search = '+'.join(srch_terms)
        break
    return search

def selected_resol_format(u_obj):
    files = u_obj.videos
    file_list = []
    for f in files:
        ext = f.extension
        resol = f.resolution
        file_list.append((ext,resol))
    count = 0
    print('='*50)
    print('Available file formats and resolutions')
    print('='*50)
    for item in file_list:
        count+=1
        print("{} >>> {}-{}".format(count,item[0],item[1]))

    while True:
        try:
            choice = int(raw_input("Select from the choices above or enter 0 to exit selection: >"))
            if(choice == 0):
                return main('a')
            elif(choice > count or choice < 1):
                print('Invalid choice, input must be a number in the range 1-{} please try again\n'.format(count))
                continue
            else:
                break
        except Exception as e:
            print('Input must be a number in the range 0-{}, please try again'.format(count))          
    return file_list[choice-1]
    
# downloading the file
def download(url):
    v = YouTube(url)
    selection = selected_resol_format(v)
    vid = v.get(selection[0], selection[1])
    print('Downloading the video, you will be informed when its done, please hold on')
    vid.download(output_folder)
    global downloaded_resol
    downloaded_resol = selection[1]
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
            selection = int(raw_input('Select from the above list or enter 0 to return to main program >'))
            if(selection > count):
                raise ValueError
            elif(selection == 0):
                return main(mode)
            else:
                return video_list[selection - 1]
        except ValueError:
            # fix pep 8 E501
            print('Input must be a number in the range 1-{}, please try again'.format(count))


# Getting the file
def get_video(soup):
        File = select_video(soup)
        title = File[1]
        link = File[0]
        vid_url = 'https://www.youtube.com' + link
        print('\n\nSelected: ' + title)
        print('Gathering available file formats and resolutions, please wait...')
        try:
            start_time = time.time()
            if download(vid_url):
                end_time = time.time()
                mins = (end_time - start_time) / 60
                secs = (end_time - start_time) % 60
                # avoid '+' use string formatting instead
                # fix pep 8 E501
                dur = str(round(mins)) + " minutes, " + str(round(secs)) + " seconds"
                print("Downloaded %s(Resolution: %s) in %.0f minutes, %.0f seconds" % (title,str(downloaded_resol),mins,secs))
            else:
                print("Could not download the video")
        except Exception as e:
            print(e)
        return


def downloader(term):
    # Openning youtube search page
        print("Searching youtube, please wait..")
        try:
            #An error was resulting from the changes you made here
            url = 'https://www.youtube.com/results?search_query='+term
            r = urlopen(url)
            html = r.read()
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
        
# Selecting mode of operation
def select_mode():
    while True:
        print("A >>> Search songs from the prompt")
        print("B >>> Download songs in the todownload file")

        mode = raw_input('Select Mode: A or B > ').lower()
        if len(mode) > 1 or not (mode.startswith('a') or mode.startswith("b")):
            print('Invalid mode, please try again')
            continue
        break
    return mode

# Main function of the program
def main(m=None):
    if not m:
        mode = select_mode()
    else:
        mode = m
    if(mode == 'a'):
        while True:
            downloader(get_search_term())
    else:
        input_file = raw_input('Provide input file path e.g. D:/input.txt >')
        if not input_file:
            print("No path provided, please try again")
            return main(mode)
        else:
            if not os.path.exists(input_file):
                print("File does not exist")
                while True:
                    print('A >>> switch mode\nB >>> Try again\nC >>> Quit program')
                    choice = raw_input('Select one of the options above >').lower()
                    if choice not in ('a','b','c'):
                          print('Invalid choice, please try again')
                          continue
                    if(choice == "a"):
                        return main('a')
                    elif(choice == 'b'):
                        return main(mode)
                    else:
                        sys.exit(0)
        with open(input_file, 'r') as f:
            try:
                files = f.readlines()
            except Exception as e:
                print(e)
                return
        for item in files:
            downloader('+'.join(item.split(' ')))

if __name__ == "__main__":main()
