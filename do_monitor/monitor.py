import requests
import os
import time
from dotenv import load_dotenv
from do_monitor.notifications.slack_alerts import send_slack_notification

# Load the environment variables
load_dotenv(".env")

do_auth_key = f"Bearer {os.getenv('AUTHORIZATION_KEY')}"
slack_token = os.getenv("SLACK_AUTH_TOKEN")
slack_channel_id = os.getenv("SLACK_CHANNEL_ID")
droplet_name = os.getenv("DROPLET_NAME")
website_url = os.getenv("WEBSITE_URL")

# List of dict's holding the droplet id and name
droplets = []
droplets_dict = {}

# Request headers
headers = {"Authorization": do_auth_key}

# Body for the post request
data = {"type": "reboot"}


def get_droplet_info():
    """
    Function gathers information about the droplet via an api call
    - https://developers.digitalocean.com/documentation/v2/#list-all-droplets

    Returns
    -------
    droplet_id
    """

    # Call the digital ocean API to get the droplet id
    r = requests.get("https://api.digitalocean.com/v2/droplets", headers=headers)

    result = r.json()["droplets"]

    for i in range(len(result)):
        droplets_dict["id"] = result[i]["id"]
        droplets_dict["name"] = result[i]["name"]
        droplets.append(droplets_dict)

    # Droplet name read from the .env file
    id = (item["id"] for item in droplets if droplet_name in item["name"])
    return next(id)


def check_site_status():
    """
    Function to check the status of https://www.abhishekpednekar.com/contact

    Returns
    -------
    None
    """

    # Get droplet id
    droplet_id = get_droplet_info()

    # Check the status of the website being monitored. The website name is being read from the .env file
    r = requests.get(website_url)

    if r.status_code == 200:
        reboot_droplet(droplet_id)


def reboot_droplet(droplet_id):
    """
    Function reboots a droplet based on the id passed to it. The reboot is handled via a call to
    a DigitalOcean droplet actions api - https://developers.digitalocean.com/documentation/v2/#reboot-a-droplet.
    Upon initiating a reboot, the function sleeps for 10 seconds before querying for the reboot status via
    another api call - https://developers.digitalocean.com/documentation/v2/#list-actions-for-a-droplet

    Parameters
    ----------
    droplet_id

    Returns
    -------
    None
    """
    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}/actions"

    # Send a warning prior to the reboot
    send_slack_notification(
        slack_token,
        slack_channel_id,
        "Your droplet is about to be rebooted",
        ":warning:",
    )

    # Call the DigitalOcean api to reboot the droplet
    requests.post(url=url, data=data, headers=headers)

    time.sleep(10)

    # Get the latest status of the reboot and send the appropriate notification
    actions = requests.get(url=url, headers=headers)
    actions_json = actions.json()
    action_status = actions_json["actions"][0]["status"]
    action_start_time = actions_json["actions"][0]["started_at"]
    action_end_time = actions_json["actions"][0]["completed_at"]

    if action_status == "in-progress":
        send_slack_notification(
            slack_token,
            slack_channel_id,
            f"The reboot was started at {action_start_time} and will complete shortly",
            ":warning:",
        )
    elif action_status == "completed":
        send_slack_notification(
            slack_token,
            slack_channel_id,
            f"The reboot was completed at {action_end_time}",
            ":heavy_check_mark:",
        )
    else:
        send_slack_notification(
            slack_token,
            slack_channel_id,
            f"There was an error while restarting the droplet",
            ":skull_and_crossbones:",
        )


if __name__ == "__main__":
    check_site_status()

