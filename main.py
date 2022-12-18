import sys
import getopt
import os
import mimetypes
import requests
import spotify_spammer as spotify


def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line


def main():
    try:
        requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        print("No internet access!")
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "aht:l:", [
                                   "threads=", "audio", "headless", "login=", "tracking"])
    except getopt.GetoptError as err:
        print(str(err).capitalize() + "!")
        sys.exit(2)

    # Default Options
    options = {
        "threads": 1,
        "audio": False,
        "headless": False,
        "login": False,
        "tracking": False
    }

    for o, a in opts:
        if o in ("-t", "--threads"):
            if(a.isnumeric() == False):
                print("Option -t must be an integer!")
                sys.exit(2)
            options["threads"] = int(a)
        elif o in ("-a", "--audio"):
            options["audio"] = True
        elif o in ("-h", "--headless"):
            options["headless"] = True
        elif o in ("-l", "--login"):
            options["login"] = True

            userlist = a

            if(os.path.exists(userlist) == False):
                print("Userlist path invalid!")
                sys.exit(2)

            if(("text/plain" in mimetypes.guess_type(userlist)) == False):
                print("Userlist must be plain text!")
                sys.exit(2)

            options["userlist"] = list(nonblank_lines(open(userlist, "r")))
        elif o == "--tracking":
            print("NOTE: Tracking is still in development, currently it does nothing!\n")
        else:
            assert False, "unhandled option"

    if(len(args) < 1):
        print("Please provide a Spotify playlist URL!")
        sys.exit(2)

    url = args[0]

    try:
        try:
            req = requests.get(url).text
        except requests.exceptions.MissingSchema:
            req = requests.get("https://" + url).text
        except requests.exceptions.ConnectionError:
            req = ""
    except requests.exceptions.ConnectionError:
        req = ""

    if(("spotify" in req) == False):
        print("Please enter a valid playlist URL!")
        sys.exit(2)

    try:
        if(len(options["userlist"]) < options["threads"]):
            print(
                f"Can't start {options['threads']} threads with {len(options['userlist'])} user(s)!")
            sys.exit(2)
    except KeyError:
        ""

    spotify.start(options, url)


if __name__ == "__main__":
    main()
