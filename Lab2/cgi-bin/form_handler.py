import cgi
import html
import os

LOGIN = "max"
PASSWORD = "max"


def get_success_page(login: str, personal_info: dict, occupation: str):
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
            
        </body>
        </html>
    """

def get_error_page(err_message: str):
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

# <h3> From cookie: {name_cookie=} {password_cookie=} </h3>


def main():
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
        exit(1)

    print(get_success_page(login, personal_info, occupation))


if __name__ == "__main__":
    main()