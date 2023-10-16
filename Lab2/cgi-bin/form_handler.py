import cgi
import http.cookies
import html
import os
import datetime

LOGIN = "max"
PASSWORD = "max"

def set_cookie(key, value, path="/", expires=False):
    cookie = http.cookies.SimpleCookie()
    cookie[key] = value
    cookie[key]["path"] = path
    if expires:
        expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        cookie[key]["expires"] = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")

def get_cookie(name):
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        for cookie in cookies:
            try:
                (_name, _value) = cookie.split('=')
                if name.lower() == _name.lower():
                    return _value
            except:
                return ''
    return ''

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

    cookie["login"] = login
    cookie["password"] = password

    cookies = {"login": cookie.get("login").value,
               "password": cookie.get("password").value,
               "count": cookie.get("count").value}

    print(
        get_success_page(login, personal_info, occupation, cookies)
    )


if __name__ == "__main__":
    print("Content-type:text/html\r\n\r\n")
    main()