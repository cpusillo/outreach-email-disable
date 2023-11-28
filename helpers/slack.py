import os
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()


class Slack:
    """
        The Slack object is used to access the Slack API, specifically to send messages.
    """
    def send_slack_message(message):
        """
            send_slack_message sends a list of users who had their send disabled to a channel of your choice.
            :param message: the generated message for each user who had their send disabled.
            :type message: str
        """
        app = App(token=os.environ.get("SLACK_TOKEN"))
        app.client.chat_postMessage(channel=os.environ.get("CHANNEL_ID"), text=message)
