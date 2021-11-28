import requests

get_url = 'http://0.0.0.0:5000/result/'
post_url = 'http://0.0.0.0:5000/vote/'
json_load = [{'candidate_id': 2},
             {'candidate_id': 2, 'opinion': 'test'},
             {'opinion': 'test'}]

for load in json_load:
    post_response = requests.post(post_url, json=load)
    print(post_response.text)

get_response = requests.get(get_url)
print(get_response.text)


