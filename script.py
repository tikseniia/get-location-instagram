import requests
import time
import json

# STEP 1: Scrap posts for a tag
arr = []

end_cursor = '' # empty for the 1st page
tag = 'moscow' # your tag
page_count = 3 # desired number of pages

for i in range(0, page_count):
    url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
    r = requests.get(url)
    data = json.loads(r.text)
    
    end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] # value for the next page
    edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
    
    for item in edges:
       arr.append(item['node'])
       
    time.sleep(2) # insurence to not reach a time limit
    
print(end_cursor) # save this to restart parsing with the next page

with open('posts.json', 'w') as outfile:
    json.dump(arr, outfile) # save to json
    
# Step 2: Get locations for posts
with open('posts.json', 'r') as f:
    arr = json.loads(f.read()) # load json data from previous step
    
locations = []
for item in arr:
    shortcode = item['shortcode']
    url = "https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
    
    r = requests.get(url)
    try:
        data = json.loads(r.text)
        try:
            location = data['graphql']['shortcode_media']['location']['name'] # get location for a post
        except:
             location = '' # if location is NULL
        locations.append({'shortcode': shortcode, 'location': location})
    except:
        location = ''
        
with open('locations.json', 'w') as outfile:
    json.dump(locations, outfile) # save to json
