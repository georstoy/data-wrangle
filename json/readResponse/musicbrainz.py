"""
To experiment with this code freely you will have to run this code locally.
Take a look at the main() function for an example of how to use the code. We
have provided example json output in the other code editor tabs for you to look
at, but you will not be able to run any queries through our UI.
"""
import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"


# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    """
    This is the main function for making queries to the musicbrainz API. The
    query should return a json document.
    """
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print("requesting"+r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    """
    This adds an artist name to the query parameters before making an API call
    to the function above.
    """
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    """
    After we get our output, we can use this function to format it to be more
    readable.
    """
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    quiz = []
    
    #####################################################
    question = 'How many bands named "First Aid Kit"'
    #####################################################
    artistName = "First Aid Kit"
    results = query_by_name(ARTIST_URL, query_type["simple"], artistName)
    
    artistCount = 0
    for artist in results["artists"]:
        if artist["name"]==artistName:
            artistCount += 1
    
    quiz.append({
        question: str(artistCount)
    })

    ##########################################
    question = 'Begin-area name for Queen?'
    ##########################################
    artistName = "Queen"
    results = query_by_name(ARTIST_URL, query_type["releases"], artistName)
    
    artistCount = 0
    artists = []
    for someArtist in results['artists']:
        if someArtist['name']==artistName and someArtist['area']['name']=='United Kingdom':
            artist = someArtist
            break
    
    quiz.append({
        question: artist['begin-area']['name']
    })

    ##########################################
    question = 'Spanish alias for Beatles?'
    ##########################################
    artistName = "The Beatles"
    results = query_by_name(ARTIST_URL, query_type['aliases'], artistName)

    artistCount = 0
    artists = []
    for someArtist in results['artists']:    
        if someArtist['name']==artistName:
            artists.append(someArtist)
    
    artist = artists[0]
    for alias in artist['aliases']:
        if alias['locale']=='es':
            answer = alias['name']
            break

    quiz.append({
        question: answer
    })
    
    ###########################################
    question = 'Nirvana disambiguation?\n'
    ###########################################
    artistName = "Nirvana"
    results = query_by_name(ARTIST_URL, query_type['atr'], artistName)

    artistCount = 0
    artists = []
    for someArtist in results['artists']:    
        if someArtist['name']==artistName and someArtist:
            artists.append(someArtist)
    
    quiz.append({
        question: artists[0]['disambiguation']
    })

    ###########################################
    question = 'When was "One Direction formed"?'
    ###########################################
    artistName = "One Direction"
    results = query_by_name(ARTIST_URL, query_type['atr'], artistName)

    artistCount = 0
    artists = []
    for someArtist in results['artists']:    
        if someArtist['name']==artistName:
            artists.append(someArtist)

    quiz.append({
        question: artists[0]['life-span']['begin']
    })
    
    pretty_print(quiz)
    
if __name__ == '__main__':
    main()