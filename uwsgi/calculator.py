import os
import time
from urllib.parse import parse_qs
from html import escape

import psycopg2


def wrapBody(body, title="Blank Title"):

    return (
        "<html>\n"
        f"<head><title>{title}</title></head>\n"
        "<body>\n"
        f"{body}\n"
        "</body>\n"
        "</html>\n"
    )


def showForm():

    body = (
        "<h1>Calculator</h1>\n"
        "<form method='post'>\n"
        "<b>First operand:</b>\n"
        "<input type='text' name='op1'><br>\n"
        "<b>Second operand:</b>\n"
        "<input type='text' name='op2'><br>\n"
        "<select name='operator'>\n"
        "<option value=''>--Choose an operator--</option>\n"
        "<option value='+'>+</option>\n"
        "<option value='-'>-</option>\n"
        "</select><br>\n"
        "<input type='submit' value='Calculate'><br>\n"
    )

    return body


def calculate(op1, op2, operator):
    if operator == "+":
        return op1 + op2
    elif operator == "-":
        return op1 - op2
    else:
        return "Error"


def get_qs_post(env):
    """
    :param env: WSGI environment
    :returns: A tuple (qs, post), containing the query string and post data,
              respectively
    """
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(env.get("CONTENT_LENGTH", 0))
    except (ValueError):
        request_body_size = 0
    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = env["wsgi.input"].read(request_body_size).decode("utf-8")
    post = parse_qs(request_body)
    return parse_qs(env["QUERY_STRING"]), post


def application(env, start_response):
    qs, post = get_qs_post(env)
    body = showForm()
    if ("op1" in post) and ("op2" in post) and ("operator" in post):
        op1 = float(post["op1"][0])
        op2 = float(post["op2"][0])
        operator = post["operator"][0]
        body += (
            f"<b>Result:</b> "
            f"{op1} {operator} {op2} = {calculate(op1, op2, operator)}"
        )
    start_response("200 OK", [("Content-Type", "text/html")])
    return [wrapBody(body, title="Calculator").encode("utf-8")]


if __name__ == "__main__":
    main()
