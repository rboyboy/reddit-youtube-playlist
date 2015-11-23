import requests
import json
import re
import sys, getopt

DEBUG = False


def get_json_data_from_request(subreddit, custom_headers, limit):
  url = "http://www.reddit.com/r/" + subreddit + ".json?limit=" + `limit`
  r = requests.get(url, headers=custom_headers)
  if r.status_code!=200:
    raise StandardError("Error when calling " + url + " : status_code: " + `r.status_code`)
  else:
    json_music = r.json()
    if DEBUG:
      print("Data got from " + url)
      with open(subreddit + '.json', 'w') as fp:
        json.dump(json_music, fp)
      print("JSON data written in file " + subreddit + ".json") 
  return json_music


def json_data_to_youtube_list(json_music):
  children = json_music["data"]["children"]
  playlist = []
  for child in children:
    data_child = child["data"]
    url = data_child["url"]
    try:
      id = get_youtube_id(url)
      playlist.append({"id":id})
    except ValueError:
      pass
  return playlist


def get_youtube_id(youtube_link):
  m = re.compile("https?://www.youtube.com/.*v=(.{11,11})").match(youtube_link)
  if m:
    return m.group(1)
  m = re.compile("https?://youtu.be/(.{11,11})").match(youtube_link)
  if m:
    return m.group(1)
  else:
    raise ValueError("Error : can't find youtube video id for link " + youtube_link)


def create_youtube_playlist(subreddit, limit):
  custom_headers = {'user-agent': 'reddit music player v0.1, by /u/rboyboy'}
  json_music = get_json_data_from_request(subreddit, custom_headers, limit)
  return json_data_to_youtube_list(json_music)
 


# MAIN

def main(argv):

  actual_reddit = "music"
  limit = 25

  helper="Usage : \"python " + sys.argv[0] + " [-h] [--subreddit ...] [-l ...]\nOptions and arguments :\n-h          : Display helper\n--subreddit : The name of the subreddit (Default : \"music\")\n-l          : Maximum number of posts parsed by the script (default : 25, min 0, max 100)"
  # Get parameters
  try:
    opts, args = getopt.getopt(argv, "hl:", ["subreddit="])
  except getopt.GetoptError:
    if DEBUG:
      print "GetoptError"
    print helper
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print helper
      sys.exit()
    if opt == '--subreddit':
      actual_reddit = arg
    if opt == '-l':
      try:
        limit=int(arg)
      except ValueError:
        print "Invalid parameter for -l : " + arg + " ! We need an integer between 0 and 100"
        sys.exit(2)
      if (limit<0) or (limit>100):
        print "Invalid parameter for -l : " + arg + " ! We need an integer between 0 and 100"
        sys.exit(2)

  playlist={}
  try:
    playlist = create_youtube_playlist(actual_reddit, limit);
  except:
    raise

  output_filename = "playlist_" + actual_reddit + ".json"
  with open(output_filename, 'w') as out:
    json.dump(playlist, out)
  
  if DEBUG:
    print "Playlist written in " + output_filename

if __name__ == "__main__":
  main(sys.argv[1:])
