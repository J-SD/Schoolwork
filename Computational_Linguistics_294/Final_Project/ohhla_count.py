import nltk
import bs4
import urllib.request
import random
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# A list of all of the pages containing lists of artists
urls = [
    "http://ohhla.com/all.html",
    "http://ohhla.com/all_two.html",
    "http://ohhla.com/all_three.html",
    "http://ohhla.com/all_four.html",
    "http://ohhla.com/all_five.html"]



def getArtistsFromURL(url):
    """Takes in a URL as a string, goes to the URL and parses the HTML for a list of all links to artists on the page"""
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.findAll("a")
    table = table[30:len(table) - 2]
    artistLinks = []
    for entry in table:
        text = str(re.findall("(?:anonymous).*\"", str(entry)))
        text = re.sub("[\]\['\"]","",text)
        if len(re.findall("/",text)) ==2:
            artistLinks.append(text)
    return artistLinks

def getAlbumsFromArtist(artistLink):
    """Takes in a URL as a string, goes to the page and parses the HTML for a list of the links to the artists albums"""
    artistLink = str(artistLink)
    url = "http://www.ohhla.com/"+artistLink
    if artistLink[0:4]=="http:":
        url = artistLink
    try:
        html = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        table = soup.findAll("a")[5:]
        albumLinks = []
        for entry in table:
            text = str(re.findall("\".*\"", str(entry)))
            text = re.sub("[\]\['\"]", "", text)
            link = url + str(text)
            if len(re.findall("(?:http)",link)) == 1:
                albumLinks.append(link)
    except:
        return []
    return albumLinks

def getSongsFromAlbum(albumLink):
    """Takes in a URL as a string and goes to the page and parses the HTML for a list of links to the album's songs"""
    albumLink = str(albumLink)
    try:
        html = urllib.request.urlopen(albumLink).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        table = soup.findAll("a")[5:]
        songLinks = []
        for entry in table:
            text = str(re.findall("\".*\"", str(entry)))
            text = re.sub("[\]\['\"]", "", text)
            link = albumLink + str(text)
            songLinks.append(link)
    except:
        return []
    return songLinks

def getLyricsFromSong(songLink):
    """Takesa a URL as a string then goes to the page and parses the HTML for the string of the song's lyrics"""
    try:
        html = urllib.request.urlopen(songLink).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        soup = soup.find("pre")
        text = soup.contents[0].strip().split("\n")[5:]
    except:
        return ".\n."

    clean_text = ""
    lyrics_list=[]
    for line in text:
        lyrics_list.append(line)
        clean_text += line + "\n"
    return clean_text

def run():
    lyrics = ""
    # Get a random range of artists by choosing a random URL
    artists = []
    for url in urls:
        # Get the artists from the URL
        artists.extend(getArtistsFromURL(url))
    print('artists count:',len(artists))
    albums = []
    while len(albums)==0:
        for artist in artists:
            # Get the albums from a random choice of the artist URLS
            albums.extend(getAlbumsFromArtist(artist))
    print('album count:', len(albums))
    songs = []
    while len(songs) == 0:
        for album in albums:
            # Get the songs from a random choice of the album URLs
            songs.extend(getSongsFromAlbum(album))
    print('songs count:', len(songs))

    for song in songs:
        lyrics += "\n" + getLyricsFromSong(song)

    text_file = open("Output_all.txt", "w")
    text_file.write(str(49322) + "|" + str(lyrics.encode("utf-8")))
    text_file.close()

run()

