import requests
import json
import re
import sys, getopt

DEBUG = False


def get_json_data_from_request(subreddit, custom_headers, limit):
  url = "http://www.reddit.com/r/" + subreddit + ".json?limit=" + `limit`
  r = requests.get(url, headers=custom_headers)
  if r.status_code!=200:
    print "Error when calling " + url + " : status_code: " + `r.status_code`
    sys.exit(2)
  else:
    print("Data got from " + url)
    json_music = r.json()
    if DEBUG:
      with open(subreddit + '.json', 'w') as fp:
        json.dump(json_music, fp)
      print("JSON data written in file " + subreddit + ".json") 
  return json_music


#def get_json_from_file(filename):
#  with open(filename) as json_file:
#    json_data = json.load(json_file)
#  print("Data got from " + filename)
#  return json_data


def json_data_to_youtube_list(json_music, output_filename):
  children = json_music["data"]["children"]
  f = open(output_filename, "w")
  for child in children:
    data_child = child["data"]
    if (data_child["domain"]=="youtube.com") |  (data_child["domain"]=="youtu.be"):
      url = data_child["url"]
      #Check that the link is not a playlist
      m = re.compile("https?://www.youtube.com/playlist.*").match(url)
      if m is None:
        if DEBUG:
          f.write(url + "   ===>   " + get_youtube_id(url))
        else:
          try:
            f.write(get_youtube_id(url))
          except ValueError as err:
            print (err.args[0])
        f.write('\n')
  f.close()
  print("Youtube ids written in file : " + output_filename)


def get_youtube_id(youtube_link):
  m = re.compile("https?://www.youtube.com/.*v=(.{11,11})").match(youtube_link)
  if m:
    return m.group(1)
  m = re.compile("https?://youtu.be/(.{11,11})").match(youtube_link)
  if m:
    return m.group(1)
  else:
    raise ValueError("Error : can't find youtube video id for link " + youtube_link)



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


  custom_headers = {'user-agent': 'reddit music player v0.1, by /u/rboyboy'}
  json_music = get_json_data_from_request(actual_reddit, custom_headers, limit)
  
  #filename = actual_reddit + ".json"
  #json_music = get_json_from_file(filename)
  
  # Write result in file name
  output_filename = "playlist_" + actual_reddit + ".txt"
  json_data_to_youtube_list(json_music, output_filename)

if __name__ == "__main__":
  main(sys.argv[1:])
