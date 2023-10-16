import cgi
import html
import http.cookies
import os


form = cgi.FieldStorage() 

try:
    username = form.getfirst("username")