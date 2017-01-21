"""
Commandline_youtube_downloader (For windows)
============================================
Coded By: Jackson Kamya
Email: jacksonkamya48@yahoo.com

This script downloads Muzic from youtube to a folder 'py_jack_downloads' on local disk D

Minimum requirements:
=====================
Python 2.7

Modules Not included in python standard installation
----------------------------------------------------
1. bs4: https://www.crummy.com/software/BeautifulSoup/bs4/download/
2. pytube: https://pypi.python.org/pypi/pytube/, https://sourceforge.net/projects/pytube/

Features:
=========
1. Download videos one by one as searched at a prompt
2. Download a list of songs as read line by line from a text file (todownload.txt)

You are free to copy and modify this script for your own requirements.
    
"""
import re
import os as win
import time

try:
    import urllib2
    from bs4 import BeautifulSoup as bs
    from pytube import YouTube
except:
    print('Please install bs4 and pytube to run this program')
    exit()

#creating download folder
output_folder = 'D:/py_jack_downloads'
if not win.path.exists(output_folder):
    win.mkdir(output_folder)

input_file = "D:/todownload.txt"
    
#Selecting mode of operation
while True:
    print("A >>> Search songs from the prompt\nB >>> Download songs in the todownload file")
    mode = raw_input('Select Mode: >').lower()
    if not re.findall("^[ab]$",mode):
        print('Invalid mode, please try again\n')
        continue
    break

#Getting youtube search term
def get_search_term():
    while True:
        Input = raw_input('Enter search term >> ').lower()
        if not Input:
            print('You didn\'t give us a thing, please try again')
            continue
        srch_parts = Input.split(' ')
        search = '+'.join(srch_parts)
        break
    return search

#downloading the file
def download(url):
    accepted_resolutions = ['480p','720p','360p']
    for resol in accepted_resolutions:
        try:
            vid = YouTube(url).get('mp4',resol)
            break
        except Exception as e:
            if(accepted_resolutions.index(resol) == (len(accepted_resolutions)-1)):
                print('No video matching any of the qualities required')
                return False
    vid.download(output_folder)
    return True

#Selecting a file from the list
def select_video(soup):
    video_list = []
    for anchor in soup.findAll('a',href=True,title=True):
        link = anchor['href']
        title = anchor['title']
        if(link[:6] == "/watch"):
            video_list.append((link,title))
    count = 0
    print('='*30)
    print('Search Results')
    print('='*30)
    if not video_list:
        print('No results found')
        return main(mode)
    for l,t in video_list:
        count+=1
        print(str(count)+" >>> "+t)
    while True:
        try:
            selection = int(raw_input('Select from the above list or enter 0 to return to main menu >')) 
            if(selection > count or selection < 0):
                raise ValueError
            elif(selection == 0):
                return main(mode)
            else:
                return video_list[selection - 1]
        except ValueError:
            print('Selection must be an integer, please try again')
            
#Getting the file
def get_video(soup):
        File = select_video(soup)
        title = File[1]
        link = File[0]
        vid_url = 'https://www.youtube.com'+link
        print('Downloading '+title)
        try:
            time_at_start = time.time()
            if download(vid_url):
                time_at_end = time.time()
                minz = (time_at_end - time_at_start)/60
                secs = (time_at_end - time_at_start)%60
                dur = str(round(minz))+" minutes, "+str(round(secs))+" seconds"
                print("Downloaded "+title+" in "+dur)
            else:
                print("Could not download the video")
        except Exception as e:
            print(e)
        return

def downloader(File):
    #Openning youtube search page
        try:
            page = urllib2.urlopen('https://www.youtube.com/results?search_query='+File).read()
        except Exception as e:
            print(e)
            return
                
        #Obtaining page's soup
        try:
            soup = bs(page)
        except Exception as e:
            print(e)
            return
                
        #Getting the video
        try:
            get_video(soup)
        except Exception as e:
            print(e)
            return
#Main function of the program
def main(mode):
    if(mode == 'a'):
        while True:
                downloader(get_search_term())
    else:
        f = open(input_file,'r')
        try:
            files = f.read().split('\n')
        except Exception as e:
            print(e)
            return
        for item in files:
            downloader('+'.join(item.split(' ')))
if __name__ == "__main__": main(mode)
