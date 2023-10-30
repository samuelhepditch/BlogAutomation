import requests
import json

# Step 1: Get authentication details to get auth key.
auth_args = {
    'username': 'wellness.wonders.connect@gmail.com',
    'password': 'SamAdAgency550',
    'client_id': '92028',
    'client_secret': 'M0paHrcIreHFPtf6G2IeJp0m10i4tRSXUT42yMlOfLHYKGMxQqYjQiqPa0NnsC2N',
    'grant_type': 'password'
}

def get_access_key(auth_args):
    # Step 2: Get Access Key
    response = requests.post('https://public-api.wordpress.com/oauth2/token', data=auth_args)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

# Step 3: Set post arguments and pass it to create the post.
post_args = {
    'title': 'Test Post with OAuth',
    'content': 'Test post content goes here..',
    'tags': 'tests',
    'post_status': 'draft',
    'categories': 'API'
}

def create_post(access_key, post_args):
    # Step 4 & 5: Create a post with the access key.
    headers = {
        'Authorization': f'Bearer {access_key}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://public-api.wordpress.com/rest/v1/sites/220516987/posts/new/', headers=headers, data=post_args)
    return response.json()

access_key = get_access_key(auth_args)
if access_key:
    response = create_post(access_key, post_args)
    print(response)
else:
    print("Failed to retrieve access key.")


access_key = get_access_key(auth_args)
create_post(access_key, post_args)