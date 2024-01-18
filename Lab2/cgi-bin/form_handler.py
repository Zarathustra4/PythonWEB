import cgi
import http.cookies
import html
import os
import datetime

LOGIN = "max"
PASSWORD = "max"

def get_success_page(login: str, personal_info: dict, occupation: str, cookies: dict) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Form hanling</title>
        </head>
        <body>
            <h1> Hi, {login} </h1>
            <h2> Personal info: {personal_info} </h2>
            <h2> I am a {occupation} </h2>
            <h3> {os.environ["HTTP_COOKIE"]=} </h3>
            <h3> From cookie: {cookies["login"]=} {cookies["password"]=} {cookies["count"]=}</h3>
        </body>
        </html>
    """

def get_error_page(err_message: str) -> str:
    return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error page</title>
            </head>
            <body>
                <h1 style="color:red">{err_message}</h1>
            </body>
            </html>
        """

def main() -> None:
    form = cgi.FieldStorage()

    login = form.getfirst("login", "")
    password = form.getfirst("password", "")

    login = html.escape(login)
    password = html.escape(password)

    info_checkboxes = ["pnu", "ipz", "group"]
    personal_info = {}
    for info_item in info_checkboxes:
        choice = form.getvalue(info_item, "off")
        if choice != "off":
            personal_info[info_item] = choice

    occupation = form.getvalue("occupation")

    if login != LOGIN or password != PASSWORD:
        message = "Wrong password or login"
        print(get_error_page(message))
        return

    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))

    count = 1
    if "count" in cookie:
        count = int(cookie.get("count").value.strip()) + 1


    print(f"Set-cookie: login={login};")
    print(f"Set-cookie: password={password};")
    print(f"Set-cookie: count={count};")


    cookies = {"login": cookie.get("login").value,
               "password": cookie.get("password").value,
               "count": cookie.get("count").value}


    print(
        get_success_page(login, personal_info, occupation, cookies)
    )


if __name__ == "__main__":
    main()