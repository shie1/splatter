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
        opts, args = getopt.getopt(sys.argv[1:], "t:h:u:", [
                                   "threads=", "headless", "userlist=", "skip="])
    except getopt.GetoptError as err:
        print(str(err).capitalize() + "!")
        sys.exit(2)

    # Default Options
    options = {
        "threads": 1,
        "audio": False,
        "headless": False,
        "userlist": False,
        "skip": False,
        "playlist": ""
    }

    for o, a in opts:
        if o in ("-t", "--threads"):
            if(a.isnumeric() == False):
                print(f"Option {o} must be an integer!")
                sys.exit(2)
            options["threads"] = int(a)
        elif o in ("-h", "--headless"):
            options["headless"] = True
        elif o in ("-u", "--userlist"):
            if(os.path.exists(a) == False):
                print("Userlist path invalid!")
                sys.exit(2)

            if(("text/plain" in mimetypes.guess_type(a)) == False):
                print("Userlist must be plain text!")
                sys.exit(2)

            options["userlist"] = list(nonblank_lines(open(a, "r")))
        else:
            assert False, "unhandled option"

    if(options["userlist"] == False):
        print("Please provide a userlist! -u")
        sys.exit(2)

    try:
        if(len(options["userlist"]) < options["threads"]):
            print(
                f"Can't start {options['threads']} threads with {len(options['userlist'])} user(s)!")
            sys.exit(2)
    except KeyError:
        ""

    spotify.start(options, spotify.testlogin)


if __name__ == "__main__":
    main()
