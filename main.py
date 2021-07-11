import sys, getopt, os, mimetypes, requests
import spotify_spammer as spotify

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def main():
    try: requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        print("No internet access!")
        sys.exit(2)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:l:", ["threads=","audio","window","login="])
    except getopt.GetoptError as err:
        print(str(err).capitalize() + "!")
        sys.exit(2)
    
    # Default Options
    options = {
        "threads": 1,
        "audio": False,
        "window": False,
        "login": False
    }
    
    for o, a in opts:
        if o in ("-t", "--threads"):
            if(a.isnumeric() == False):
                print("Option -t must be an integer!")
                sys.exit(2)
            options["threads"] = int(a)
        elif o == "--audio":
            options["audio"] = True
        elif o == "--window":
            options["window"] = True
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
        else:
            assert False, "unhandled option"
    
    if(len(args) < 1):
        print("Please provide a Spotify playlist URL!")
        sys.exit(2)
    
    url = args[0]
    
    try:
        try: req = requests.get(url).text
        except requests.exceptions.MissingSchema: req = requests.get("https://" + url).text
        except requests.exceptions.ConnectionError: req = ""
    except requests.exceptions.ConnectionError: req = ""
    
    if(("spotify" in req) == False) or (("playlist" in req) == False):
        print("Please enter a valid playlist URL!")
        sys.exit(2)
        
    if(len(userlist) < options["threads"]) and (options["login"] == True):
        print(f"Can't start {options['threads']} threads with {len(userlist)} user(s)!")
        sys.exit(2)

    spotify.start(options,url)

if __name__ == "__main__":
    main()