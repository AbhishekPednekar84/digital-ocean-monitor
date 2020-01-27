# DigitalOcean Droplet Monitor
The script checks the status of a website hosted on a DigitalOcean droplet using `requests.get`. If the returned HTTP status code is not `200`, then the script proceeds to reboot the droplet. Notifications are sent to a configured Slack channel.

## Steps to run the script
1. Create and activate a virtual environment. Ex: `python -m venv venv`
2. Install the requirements - `pip install -r requirements.txt`
3. Create a .env file and set the following environment variables -
   - AUTHORIZATION_KEY (from DigitalOcean)</b >
   - SLACK_AUTH_TOKEN (from Slack)</b >
   - SLACK_CHANNEL_ID</b > 
   - DROPLET_NAME (to be rebooted)</b >
   - WEBSITE_URL (to be monitored)
4. Run the script using the command - `python -m do_monitor.monitor`

#### Sample notification to Slack:

![slack](https://github.com/AbhishekPednekar84/digital-ocean-monitor/blob/master/do_monitor/notifications/images/slack.jpg)
