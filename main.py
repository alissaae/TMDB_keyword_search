from flask import Flask, render_template, request

import urllib.parse, urllib.request, urllib.error, json, tmdb_api



from flask import Flask, render_template
import logging

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
        	print("The server couldn't fulfill the request.")
        	print("Error code: ", e.code)
        elif hasattr(e,'reason'):
        	print("We failed to reach a server")
        	print("Reason: ", e.reason)
        return None

#getting the keyword ids



def obtain_keywords(baseurl='https://api.themoviedb.org/3/search/keyword',
        api_key = tmdb_api.key,
        format = 'json',
        query = "happy",
        params = {},
        printurl = False
        ):
    #params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    params["query"] = query
    if format == "json":
        params['nojsoncallback'] = True
    url = baseurl+ "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safeGet(url)

#obtaining the data from the json file, have all the values of the keywords
def keyword_list(url):
    readable = url.read()
    getreadytoprint = json.loads(readable)
    id_list = []
    for each_id in getreadytoprint["results"]:
        for key in each_id:
            if key == "id":
                if len(id_list) == 0:
                    id_list = [each_id[key]]
               # else:
                   # id_list.append(each_id[key])
    return id_list[0]

#keywords are stored here to pass into



# primary_release_year = choice,

def TMDB_REST(baseurl='https://api.themoviedb.org/3/discover/movie/',
        api_key = "deafc5d037262e305f40d056e578cfb9",
        format = 'json',
        language = "en-US",
        sort_by = "popularity.desc",
        include_adult = False,
        params = {},
        printurl = True
        ):
    params['api_key'] = api_key
    params['format'] = format
    params["language"] = language
    params["sort_by"] = sort_by
    #params["primary_release_year"] = primary_release_year
    params["include_adult"] = include_adult

    if format == "json":
        params['nojsoncallback'] = True
    url = baseurl+ "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safeGet(url)

def printinfo(url):
    readable = url.read()
    getreadytoprint = json.loads(readable)
    return getreadytoprint



class Movie():
    """where we will access all our movie info"""
    def __init__(self, dict):
        starter = dict["results"]
        self.title= starter[0]["title"]
        self.popularity = starter[0]["popularity"]
        self.overview = starter[0]["overview"]
       # self.release_date = starter[0]["original_releasae_date"]

# need to get the tags, then get a dictionary of information with the movies of those tags
# process the info into a printable form
# read in the parts of the photo info you want to see





#FLASK CODE

@app.route('/')
def main_handler():
    app.logger.info("InMainHandler")
    return render_template("openingpagetemplate.html", page_title= "Find Movies")

@app.route("/gresponse")
def greet_response_handler():
    name =request.args.get('keyword')
    app.logger.info(name)
    if name:
        # if form filled in, greet them using this data
    # this returns one keyword that can be used using the query
        word_find = keyword_list(obtain_keywords(query = name))
        #tmdb rest needs to take that one word in as with_keywords and returns a dictionary
        movie_search = Movie(printinfo(TMDB_REST(params={'with_keywords': word_find})))

        return render_template('responsepage.html',name=name,page_title="Search Response for %s"%name, film_title=movie_search.title, popularity= movie_search.popularity, film_overview= movie_search.overview)

    else:
    #if not, then show the form again with a correction to the user
        return render_template('responsepage.html',page_title="Search Results -Error")

if __name__ == "__main__":
    # Used when running locally only.
	# When deploying to Google AppEngine, a webserver process
	# will serve your app.
    app.run(host="localhost", port=8080, debug=True)

