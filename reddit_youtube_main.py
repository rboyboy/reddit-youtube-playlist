#!/usr/bin/python

import json
import sys, getopt
from reddit_youtube import create_youtube_playlist

def main(argv):

  actual_reddit = "music"
  limit = 25

  helper="Usage : \"python " + sys.argv[0] + " [-h] [--subreddit ...] [-l ...]\nOptions and arguments :\n-h          : Display helper\n--subreddit : The name of the subreddit (Default : \"music\")\n-l          : Maximum number of posts parsed by the script (default : 25, min 0, max 100)"
  # Get parameters
  try:
    opts, args = getopt.getopt(argv, "hl:", ["subreddit="])
  except getopt.GetoptError:
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
 
  print "Playlist written in " + output_filename



if __name__ == "__main__":
  main(sys.argv[1:])
