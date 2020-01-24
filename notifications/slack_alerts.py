import slack


def send_slack_notification(token, channel, message, emoji):
    """
    Function sends a slack notification to the configured channel

    Parameters
    ----------
    1. slack token
    2. slack channel id
    3. message
    4. emoji

    Returns
    -------
    None
    """
    slack_token = token
    client = slack.WebClient(token=slack_token)

    client.chat_postMessage(channel=channel, text=f"{emoji} {message}")
