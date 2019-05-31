import bs4
import urllib.request
import re


def getArtistsFromURL(url):
    """Takes in a URL as a string, goes to the URL and parses the HTML for a list of all links to artists on the page"""
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.findAll("a") # Links in the table are marked with the tag 'a'
    table = table[30:len(table) - 2]    # the actual artists are the 30th link onwards up until the last two
    artistLinks = [] # a list of all the links to pages with albums
    for entry in table:
        text = str(re.findall("(?:anonymous).*\"", str(entry))) # links are in the table with the string 'anonymous'
        text = re.sub("[\]\['\"]","",text)                      # remove the list notation and quotes
        if len(re.findall("/",text)) ==2:                       # make sure the link is valid
            artistLinks.append(text)                            # add the link to the list
    return artistLinks


def getAlbumsFromArtist(artistLink):
    """Takes in a URL as a string, goes to the page and parses the HTML for a list of the links to the artists albums"""
    artistLink = str(artistLink)
    url = "http://www.ohhla.com/"+artistLink  # the url is the homepage appended with the name of the artist
    if artistLink[0:4]=="http:":
        url = artistLink                      # if the artist link is a full URL already, don't append the homepage
    try:
        html = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        table = soup.findAll("a")[5:]                   # links are within the tag <a href="">
        albumLinks = []                                 # a list to be filled with links to albums
        for entry in table:
            text = str(re.findall("\".*\"", str(entry)))        # find the text between quotes, this is the link
            text = re.sub("[\]\['\"]", "", text)                # remove list notation and quotes
            link = url + str(text)                              # the full url is the running url plus the new addition
            if len(re.findall('(?:http)', link)) == 1:           # make sure the link is valid
                albumLinks.append(link)                         # add it to the list
    except:
        return []                                               # if there is an error, just return an empty list
    return albumLinks


def getSongsFromAlbum(albumLink):
    """Takes in a URL as a string and goes to the page and parses the HTML for a list of links to the album's songs"""
    albumLink = str(albumLink)
    try:                                                       # this function behaves the same as get albums
        html = urllib.request.urlopen(albumLink).read()             # a better design would be to have one function
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
    """Takes a a URL as a string then goes to the page and parses the HTML for the string of the song's lyrics"""
    try:
        html = urllib.request.urlopen(songLink).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        soup = soup.find("pre")
        text_split = soup.contents[0].strip().split("\n")[5:]
    except:
        return ".\n."           # if there is an error going to the URL, use a trash string to prevent further issues
    text_joined = ""
    for line in text_split:
        text_joined += line + "\n"       # turn the list of lines into one string
    return text_joined


def run():
    lyrics = ""                 # empty string to be filled with all lyrics
    artist_group_urls = [           # A list of all of the pages containing lists of artists
        "http://ohhla.com/all.html",        # A-E and numbers/symbols
        "http://ohhla.com/all_two.html",    # F-J
        "http://ohhla.com/all_three.html",  # K-O
        "http://ohhla.com/all_four.html",   # P-T
        "http://ohhla.com/all_five.html"]   # U-Z

    artists = []
    for url in artist_group_urls:                   # For every group of artists:
        artists.extend(getArtistsFromURL(url))          # Get the artists from the URL
    print('artists count:',len(artists))

    albums = []
    for artist in artists:
        albums.extend(getAlbumsFromArtist(artist))      # Get the albums from a random choice of the artist URLS
    print('album count:', len(albums))

    songs = []                                          # An empty list to be filled with song links
    for album in albums:
        songs.extend(getSongsFromAlbum(album))          # Get the songs from a random choice of the album URLs
    print('songs count:', len(songs))

    for song in songs:
        lyrics += "\n" + getLyricsFromSong(song)        # Build a string of all the lyrics

    text_file = open("Output_all.txt", "w")
    text_file.write(str(49322) +"|" + str(lyrics.encode("utf-8"))) # Write all of the lyrics to a text file for analysis
    text_file.close()

run()

