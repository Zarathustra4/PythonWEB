import http.cookies
import html

def main():
    print(f"Set-cookie: login=;")
    print(f"Set-cookie: password=;")
    print(f"Set-cookie: count=;")

    print("""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error page</title>
            </head>
            <body>
                <h1 style="color:blue">Cookies are cleaned</h1>
            </body>
            </html>
    """)

if __name__ == "__main__":
    main()