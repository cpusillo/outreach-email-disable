from helpers.outreach import Outreach
from helpers.slack import Slack


def main(event, context):

    mailboxes = Outreach().fetch_all_mailboxes()

    def filter_mailbox_data(mailboxes):
        # Our handler should only work with mailboxes that fit these conditions:
        # - heapanalytics.com email addresses with sending permissions on.
        mailboxes = [
            m
            for m in mailboxes
            if m.get("attributes").get("email").endswith("heapanalytics.com")
            if m.get("attributes").get("sendDisabled") == False
        ]
        return mailboxes

    mailboxes = filter_mailbox_data(mailboxes)

    for m in mailboxes:
        id = m.get("id")
        email = m.get("attributes").get("email")
        message = f"Disabling send for mailbox {email}"
        response = Outreach().disable_send(id)
        if response == 200:
            Slack.send_slack_message(message)
    Slack.send_slack_message("Done!")


if __name__ == "__main__":
    main("", "")
