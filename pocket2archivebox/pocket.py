import json
import requests
import time
import os

# Load configs
with open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "r") as f:
    config = json.load(f)

# Lets open the timestamp file which contains timestamp of last run
with open(config["save"]["timestamp_file_path"]) as timestamp:
    # Let's record timestamp of this run
    new_timestamp = int(time.time())

	# Lets load the file as json
    timestamp_json = json.load(timestamp)
    
	# Pocket API endpoint
    url = "https://getpocket.com/v3/get"
    postdata = {
        "consumer_key": config["pocket"]["consumer_key"], # Application id
        "access_token": config["pocket"]["access_token"], # User id
        "state": "all",								      # We want all articles
        "detailType": "complete",						  # This contains tags as well
        "since": timestamp_json["updated"]			      # We only care about updates since last run
    }

    # Lets call the pocket API with our parameters
    response = requests.post(url, data = postdata).content

    # We load the respond as json, note that we only care about "list" array
    response_json = json.loads(response)["list"]

    # Lets loop through pocket response
    for site in response_json:
        # Let loop through the tags and add them to array "tags"
        tags = []
        if("tags" in response_json[site]):
            for tag in response_json[site]["tags"]:
                tags.append('"' + tag + '"')

        # Let's check that "resolved_url" exists
        if "resolved_url" in response_json[site]:
            # Add tags if they exists
            if tags:
                os.system(f"docker exec -i --user archivebox {config['archivebox']['container_name']} archivebox add --tag={','.join(tags)} {response_json[site]['resolved_url']}")
            # Without tags
            else:
                os.system(f"docker exec -i --user archivebox {config['archivebox']['container_name']} archivebox add {response_json[site]['resolved_url']}")

	# Now we can update the timestamp of last run
    timestamp_json["updated"] = new_timestamp

# We want to write the new timestamp to disk
with open(config["save"]["timestamp_file_path"], "w") as timestamp:
	json.dump(timestamp_json, timestamp)