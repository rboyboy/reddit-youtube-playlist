import requests
import json

subreddit_music = "music"
subreddit_rock = "rock"
actual_reddit = subreddit_rock

def get_json_data_from_request(url, custom_headers):
  r = requests.get(url, headers=custom_headers)
  if r.status_code!=200:
    print "status_code: " + `r.status_code`
    exit()
  else:
    print("Data got from " + url)
    json_music = r.json()
    with open(actual_reddit + '.json', 'w') as fp:
      json.dump(json_music, fp)
    print("Data written in file " + actual_reddit + ".json")
  return json_music


def get_json_from_file(filename):
  with open(filename) as json_file:
    json_data = json.load(json_file)
  print("Data got from " + filename)
  return json_data


def json_data_to_youtube_list(json_music):
  children = json_music["data"]["children"]
  f = open("playlist_r_" + actual_reddit + ".txt", "w")
  f.write("Youtube playlist : \n\n")
  for child in children:
    data_child = child["data"]
    if (data_child["domain"]=="youtube.com") |  (data_child["domain"]=="youtu.be"):
      f.write(data_child["url"])
      f.write('\n')
  f.close()


# MAIN

#url = "http://www.reddit.com/r/" + actual_reddit + ".json"
#custom_headers = {'user-agent': 'reddit music player v0.1, by /u/rboyboy'}
#json_music = get_json_data_from_request(url, custom_headers)

filename = actual_reddit + ".json"
json_music = get_json_from_file(filename)

json_data_to_youtube_list(json_music)

