import os
import time
from urllib.parse import parse_qs
from html import escape

import psycopg2


def wrapBody(body, title="Blank Title"):
    return (
        "<html>\n"
        "<head>\n"
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"{body}\n"
        "<hr>\n"
        f"<p>This page was generated at {time.ctime()}.</p>\n"
        "</body>\n"
        "</html>\n"
    )


def showAllProfiles(conn):
    cursor = conn.cursor()

    sql = """
    SELECT id, lastname, firstName, email, activities
    FROM profiles
    """

    cursor.execute(sql)

    ## create an HTML table for output:
    body = """
    <h2>Profile List</h2>
    <p>
    <table border=1>
      <tr>
        <td><font size=+1"><b>lastname</b></font></td>
        <td><font size=+1"><b>firstname</b></font></td>
        <td><font size=+1"><b>email</b></font></td>
        <td><font size=+1"><b>activities</b></font></td>
        <td><font size=+1"><b>delete</b></font></td>
      </tr>
    """

    count = 0
    # each iteration of this loop creates on row of output:
    for idNum, lastname, firstName, email, activities in cursor:
        body += (
            "<tr>"
            f"<td><a href='?idNum={idNum}'>{lastname}</a></td>"
            f"<td><a href='?idNum={idNum}'>{firstName}</a></td>"
            f"<td>{email}</td>"
            f"<td>{activities}</td>"
            "<td><form method='post' action='miniFacebook.py'>"
            f"<input type='hidden' NAME='idNum' VALUE='{idNum}'>"
            '<input type="submit" name="deleteProfile" value="Delete">'
            "</form></td>"
            "</tr>\n"
        )
        count += 1

    body += "</table>" f"<p>Found {count} profiles.</p>"

    return body


def showProfilePage(conn, idNum):
    body = """
    <a href="./miniFacebook.py">Return to main page.</a>
    """

    cursor = conn.cursor()

    sql = """
    SELECT *
    FROM profiles
    WHERE id=%s
    """
    cursor.execute(sql, (int(idNum),))

    data = cursor.fetchall()

    # show profile information
    (idNum, lastname, firstName, email, activities) = data[0]

    body += """
    <h2>%s %s's Profile Page</h2>
    <p>
    <table border=1>
        <tr>
            <td>Email</td>
            <td>%s</td>
        </tr>
        <tr>
            <td>Activities</td>
            <td>%s</td>
        </tr>
    </table>
    """ % (
        firstName,
        lastname,
        email,
        activities,
    )

    # provide an update button:
    body += (
        """
    <FORM METHOD="POST" action="miniFacebook.py">
    <INPUT TYPE="HIDDEN" NAME="idNum" VALUE="%s">
    <INPUT TYPE="SUBMIT" NAME="showUpdateProfileForm" VALUE="Update Profile">
    </FORM>
    """
        % idNum
    )

    # Get and display all status message for this person
    sql = """
    SELECT DateTime, Message
    FROM status
    WHERE profile_id=%s
    """

    cursor.execute(sql, (int(idNum),))

    data = cursor.fetchall()

    body += """
    <h2>Status Updates</h2>
    <p>
    <table border=1>
        <tr>
          <td>DateTime</td>
          <td>Message</td>
        </tr>
    """

    for row in data:

        body += (
            """
        <tr>
          <td>%s</td>
          <td>%s</td>
        </tr>
        """
            % row
        )

    body += """
    </table>
    """

    # Add form to let user update their status message
    body += (
        """
    <FORM METHOD="POST" action="miniFacebook.py">
    <INPUT TYPE="HIDDEN" NAME="idNum" VALUE="%s">
	<input type="text" name="message" value="Enter a new status...">
    <INPUT TYPE="SUBMIT" NAME="processStatusUpdate" VALUE="Update Status">
    </FORM>
    """
        % idNum
    )
    return body


def showAddProfileForm():
    return """
    <h2>Add A Profile</h2>
    <p>
    <FORM METHOD="POST">
    <table>
        <tr>
            <td>Last Name</td>
            <td><INPUT TYPE="TEXT" NAME="lastname" VALUE=""></td>
        </tr>
        <tr>
            <td>First Name</td>
            <td><INPUT TYPE="TEXT" NAME="firstname" VALUE=""></td>
        </tr>
        <tr>
            <td>Email</td>
            <td><INPUT TYPE="TEXT" NAME="email" VALUE=""></td>
        </tr>
        <tr>
            <td>Activities</td>
            <td><TEXTAREA COLS=60 NAME="activities"></TEXTAREA></td>
        </tr>
        <tr>
            <td></td>
            <td>
            <input type="submit" name="addProfile" value="Add!">
            </td>
        </tr>
    </table>
    </FORM>
    """


def getUpdateProfileForm(conn, idNum):
    # First, get current data for this profile
    cursor = conn.cursor()

    sql = """
    SELECT *
    FROM profiles
    WHERE id=%s
    """
    cursor.execute(sql, (idNum,))

    data = cursor.fetchall()

    # Create a form to update this profile
    (idNum, lastname, firstName, email, activities) = data[0]

    return """
    <h2>Update Your Profile Page</h2>
    <p>
    <FORM METHOD="POST">
    <table>
        <tr>
            <td>Last Name</td>
            <td><INPUT TYPE="TEXT" NAME="lastname" VALUE="%s"></td>
        </tr>
        <tr>
            <td>First Name</td>
            <td><INPUT TYPE="TEXT" NAME="firstname" VALUE="%s"></td>
        </tr>
        <tr>
            <td>Email</td>
            <td><INPUT TYPE="TEXT" NAME="email" VALUE="%s"></td>
        </tr>
        <tr>
            <td>Activities</td>
            <td><TEXTAREA COLS=60 NAME="activities">%s</TEXTAREA></td>
        </tr>
        <tr>
            <td></td>
            <td>
            <input type="hidden" name="idNum" value="%s">
            <input type="submit" name="completeUpdate" value="Update!">
            </td>
        </tr>
    </table>
    </FORM>
    """ % (
        lastname,
        firstName,
        email,
        activities,
        idNum,
    )


def addProfile(conn, lastName, firstName, email, activities):
    cursor = conn.cursor()

    sql = "SELECT max(ID) FROM profiles"
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        nextID = int(data[0]) + 1
    except:
        nextID = 1

    sql = "INSERT INTO profiles VALUES (%s,%s,%s,%s,%s)"
    params = (nextID, lastName, firstName, email, activities)

    cursor.execute(sql, params)
    conn.commit()

    body = ""
    if cursor.rowcount > 0:
        body = "Add Profile Succeeded."
    else:
        body = "Add Profile Failed."

    return body, nextID


def updateStatusMessage(conn, idNum, message):
    cursor = conn.cursor()

    tm = time.localtime()
    nowtime = "%04d-%02d-%02d %02d:%02d:%02d" % tm[0:6]

    sql = "INSERT INTO status(profile_id, message, dateTime) VALUES (%s,%s,%s)"
    params = (idNum, message, nowtime)
    cursor.execute(sql, params)
    conn.commit()

    if cursor.rowcount > 0:
        return "Succeeded."
    else:
        return "Failed."


def processProfileUpdate(conn, idNum, lastname, firstname, email, activities):
    cursor = conn.cursor()

    sql = "UPDATE profiles SET lastname=%s, firstname=%s, email=%s, activities=%s WHERE id = %s"
    params = (lastname, firstname, email, activities, idNum)

    cursor.execute(sql, params)
    conn.commit()

    if cursor.rowcount > 0:
        return "Update Profile Succeeded."
    else:
        return "Update Profile Failed."


def deleteProfile(conn, idNum):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = %s", (idNum,))
    conn.commit()
    if cursor.rowcount > 0:
        return "Delete Profile Succeeded."
    else:
        return "Delete Profile Failed."


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

    body = ""
    try:
        conn = psycopg2.connect(
            host="postgres",
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
    except psycopg2.Warning as e:
        print(f"Database warning: {e}")
        body += "Check logs for DB warning"
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        body += "Check logs for DB error"

    idNum = None
    if "idNum" in post:
        idNum = post["idNum"][0]
        # handle case of starting to do an update -- show the form
        if "showUpdateProfileForm" in post and "idNum" in post:
            body += getUpdateProfileForm(conn, post["idNum"][0])
        ## handle case of completing an update
        elif "completeUpdate" in post:
            body += processProfileUpdate(
                conn,
                idNum,
                post["lastname"][0],
                post["firstname"][0],
                post["email"][0],
                post["activities"][0],
            )
        # handle case of showing a profile page
        elif "processStatusUpdate" in post:
            messages = post["message"][0]
            body += updateStatusMessage(conn, idNum, messages)
        elif "deleteProfile" in post:
            body += deleteProfile(conn, idNum)
            idNum = None
    # handle case of adding a profile page:
    elif "addProfile" in post:
        b, idNum = addProfile(
            conn,
            post["lastname"][0],
            post["firstname"][0],
            post["email"][0],
            post["activities"][0],
        )
        body += b
    elif "idNum" in qs:
        idNum = qs.get("idNum")[0]
    if idNum:
        # Finish by showing the profile page
        body += showProfilePage(conn, idNum)
    # default case: show all profiles
    else:
        body += showAllProfiles(conn)
        body += showAddProfileForm()

    start_response("200 OK", [("Content-Type", "text/html")])
    return [wrapBody(body, title="Mini Facebook").encode("utf-8")]


if __name__ == "__main__":
    main()
