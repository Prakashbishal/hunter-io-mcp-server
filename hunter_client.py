
import httpx
import os
from dotenv import load_dotenv

url = "https://api.hunter.io/v2/domain-search"

load_dotenv()
apikey = os.getenv("HUNTER_API_KEY")

if not apikey:
    raise ValueError("HUNTER_API_KEY is missing. Check your .env file.")


# Reusable helper for Hunter.io API requests
def hunter_get(url: str, params: dict, timeout: int = 10) -> dict:

    try:
        response = httpx.get(url, params=params, timeout=timeout)
        response.raise_for_status()

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 401:
            raise ValueError("Hunter.io authentication failed") from None

        elif status_code == 429:
            raise ValueError("Hunter.io rate limit exceeded") from None

        else:
            raise ValueError(f"Hunter.io API error: {status_code}") from None

    except httpx.RequestError:
        raise ValueError("Unable to connect to Hunter.io") from None

    return response.json()


def search_domain(domain: str) -> dict:

    params = {
        "domain": domain,
        "api_key": apikey
    }

    result = hunter_get(url, params)

    org = result["data"]["organization"]
    res = result["meta"]["results"]
    emails = [email["value"] for email in result["data"]["emails"]]

    return {
        "organization": org,
        "total_results": res,
        "emails": emails
    }


def find_person_email(first_name: str, last_name: str, domain: str) -> dict:

    url = "https://api.hunter.io/v2/email-finder"

    params = {
        "domain": domain,
        "api_key": apikey,
        "first_name": first_name,
        "last_name": last_name
    }

    response = httpx.get(url, params=params, timeout=10)
    response.raise_for_status()

    result = response.json()
    data = result["data"]

    firstname = data.get("first_name")
    lastname = data.get("last_name")
    email = data.get("email")
    con = data.get("score")

    return {
        "first_name": firstname,
        "last_name": lastname,
        "emails": email,
        "confidence": con
    }


def verify_email(email: str) -> dict:

    url = "https://api.hunter.io/v2/email-verifier"

    params = {
        "email": email,
        "api_key": apikey
    }

    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()

    result = response.json()
    data = result["data"]

    email = data.get("email")
    status = data.get("status")
    score = data.get("score")

    return {
        "email": email,
        "status": status,
        "score": score
    }


if __name__ == "__main__":
    print(search_domain("stripe.com"))
