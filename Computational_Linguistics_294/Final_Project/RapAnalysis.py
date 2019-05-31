import nltk
import bs4
import urllib.request
import random
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

SAMPLE_SIZE = 10
total_compound = 0.0
compound_scores = []
total_pos = 0.0
total_neu = 0.0
total_neg = 0.0

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

def runOneSong():
    lyrics = ""
    while lyrics == "":
        try:
            # Get a random range of artists by choosing a random URL
            urlRand = random.choice(urls)

            # Get the artists from the URL
            artists = getArtistsFromURL(urlRand)

            # Get the albums from a random choice of the artist URLS
            albums = getAlbumsFromArtist(random.choice(artists))

            # Get the songs from a random choice of the album URLs
            songs = getSongsFromAlbum(random.choice(albums))
            song = random.choice(songs)

            # Get the lyrics from the song
            lyrics = getLyricsFromSong(song)
        except:
            lyrics = ""
    return lyrics

def get_adj(tagged_lyrics):
    adjectives = []
    for word in tagged_lyrics:
        if word[1] == 'JJ':
            adjectives.append(word[0])
    return adjectives

def sentAnalysis(lyrics):
    global total_compound
    global total_pos
    global total_neu
    global total_neg
    global compound_scores
    lines_list = nltk.tokenize.line_tokenize(lyrics)
    sid = SentimentIntensityAnalyzer()
    for sentence in lines_list:
        ss = sid.polarity_scores(sentence)
        total_compound += ss['compound']
        compound_scores.append(ss['compound'])
        total_pos += ss['pos']
        total_neu += ss['neu']
        total_neg += ss['neg']

        # for k in sorted(ss):
        #     #print('{0}: {1}, '.format(k, ss[k]), end='')
        #     print(k,ss[k])


def main():
    global total_compound
    all_lyrics = ""
    for i in range(SAMPLE_SIZE):
        percent = str(round(((i + 1) / SAMPLE_SIZE) * 100, 2))
        print_string =str(i+1)+"/"+str(SAMPLE_SIZE)+"........"+percent+"%"
        print('\r'+print_string, end="")
        lyrics = runOneSong()
        all_lyrics+="\n"+lyrics
    print("\nnumber of words:",len(re.split(" ",all_lyrics)))
    print("number of lines:", len(re.split("\n", all_lyrics)))
    sentAnalysis(all_lyrics)
    text_file = open("Output.txt", "w")
    text_file.write(str(SAMPLE_SIZE)+"|"+str(all_lyrics.encode(errors='replace')))
    text_file.close()

main()

print("FINAL COMPOUND SCORE USING",SAMPLE_SIZE,"SAMPLES:",total_compound)
print("AVERAGE COMPOUND SCORE:", sum(compound_scores) / float(len(compound_scores)))
print("FINAL POSITIVE SCORE:", total_pos)
print("FINAL NEUTRAL SCORE:", total_neu)
print("FINAL NEGATIVE SCORE:", total_neg)