import os
import re
from pprint import pprint

import requests
from fastapi import FastAPI
from jwt import JWT
from requests_oauthlib import OAuth2Session
import webbrowser

def get_token():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Open a web-browser for OAuth Login to Microsoft Online
    oauth = OAuth2Session(
        client_id="b36b1432-1a1c-4c82-9b76-24de1cab42f2",
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
    )

    authorization_url, state = oauth.authorization_url(
        url="https://login.microsoftonline.com/common/oauth2/authorize",
        resource="https://meeservices.minecraft.net",
    )

    webbrowser.open(authorization_url)

    print("Your browser will open to log into the system. Once done it will then try to open an invalid URL beginning with:")
    print("  urn:ietf:wg:oauth:2.0:oob?code=")
    print("Please copy and paste that entire URL below. In Chrome you should right click the message box and choose 'copy full text")
    print("which will grab all the text. You can use this as well as we will ignore the message text")
    print("\n\n")

    while True:
        authorization_response = re.search("urn[^ ]+", input('Enter the full url (or text):  ')).group(0)

        if ".." in authorization_response:
            print("You have provided a shortened response. Try right clicking the message box and choosing 'copy full text' ")
            continue

        break

    token = oauth.fetch_token(
        token_url="https://login.microsoftonline.com/common/oauth2/token",
        authorization_response=authorization_response,
        include_client_id=True,
    )

    # Get Tenant ID from access_token
    access = JWT().decode(token["access_token"], do_verify=False, do_time_check=False)
    return access["tid"], token["refresh_token"]


if __name__ == "__main__":
    tenant, token = get_token()

    print("\n\nAdd the following line to 'tokens.yml'\n")
    print("{}: \"{}\"".format(tenant, token))
