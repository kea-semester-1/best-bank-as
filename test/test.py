import requests

with requests.Session() as session:
    # Step 1: GET request to fetch CSRF token
    login_url = "http://localhost/accounts/login/"
    initial_response = session.get(login_url)
    initial_response.raise_for_status()

    # Extract CSRF token from cookies
    csrf_token = session.cookies.get("csrftoken")
    print("token!!!!!!!!!!!!!!!", csrf_token)
    print("Cookies after GET request:", session.cookies.get_dict())

    if not csrf_token:
        raise ValueError("CSRF token not found in initial response")

    # Step 2: POST request with CSRF token and credentials
    credentials = {
        "username": "Mo",
        "password": "123",
        "csrfmiddlewaretoken": csrf_token,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": login_url,  # Adding the Referer header
        "X-CSRFToken": csrf_token,
    }

    login_response = session.post(
        url=login_url, data=credentials, headers=headers, allow_redirects=False
    )
    print(login_response.__dict__)

    login_response.raise_for_status()
