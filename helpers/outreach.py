import requests, os, json
from dotenv import load_dotenv

load_dotenv()


class Outreach:
    """
        the Outreach object is used to access the Outreach API.
    """
    def __auth(self):
        """
            __auth() is accessible only to Outreach class methods.
            This method simply builds the session object so that
            future methods can securely access the Outreach API.
        """
        response = requests.post(
            "https://api.outreach.io/oauth/token",
            {
                "client_id": os.getenv("OUTREACH_ID"),
                "client_secret": os.getenv("OUTREACH_SECRET"),
                "grant_type": "refresh_token",
                "refresh_token": os.getenv("REFRESH_TOKEN"),
            },
        )
        # Update session headers with access token for subsequent calls
        session = requests.Session()
        session.headers.update(
            {"Authorization": "Bearer " + response.json().get("access_token")}
        )
        return session

    def fetch_all_mailboxes(self):
        """
            fetch_all_mailboxes queries the Outreach API for all
            active user mailboxes that exist in our account.
        """
        mailboxes = []
        url = "https://api.outreach.io/api/v2/mailboxes"
        session = self.__auth()

        response = session.get(url).json(
        while response.get("links").get("next"):
            url = response.get("links").get("next")
            response = session.get(url).json()
            mailboxes += response.get("data")
        return mailboxes

    def disable_send(self, id):
        """
            disable_send sets the mailbox attribute 'sendDisabled' to True.
            :param id: the user's id which needs to have their sendDisabled attr set.
        """
        session = self.__auth()
        payload = {
            "data": {
                "type": "mailbox",
                "id": id,
                "attributes": {"sendDisabled": True},
            }
        }
        url = f"https://api.outreach.io/api/v2/mailboxes/{id}"
        response = session.patch(url, data=json.dumps(payload))
        return response.status_code
