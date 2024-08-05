import requests

bibkeys = ["ISBN:9780747532699", "ISBN:0201558025"]

params = {"format": "json", "jscmd": "data", "bibkeys": ",".join(bibkeys)}

url = f"https://openlibrary.org/api/books"

# These should be your actual username 
username = input("Usename:")
password = input("Password:")

response = requests.get(url, params=params).json()
for b in bibkeys:
    print(response[b]["title"])


### Log into FOLIO
def get_token():
    headers = {"Content-Type": "application/json", "x-okapi-tenant": "diku"}
    url = "https://folio-orchid-okapi.dev.folio.org/authn/login"
    body = {"username": username, "password": password}

    print("logging in to FOLIO")
    response = requests.request("POST", url, headers=headers, json=body).json()
    return response["okapiToken"]

# Make a request

headers = {
    "Content-Type": "application/json",
    "x-okapi-tenant": "diku",
    "x-okapi-token": get_token()
    }

url = f"https://folio-orchid-okapi.dev.folio.org/users?username={username}"

response = requests.request("GET", url, headers=headers).json()
print(response)
