import sys, getopt, os, mimetypes, requests

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
        opts, args = getopt.getopt(sys.argv[1:], "t:", ["threads=","audio","window"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err).capitalize() + "!")
        sys.exit(2)
    
    # Default Options
    options = {
        "threads": 1,
        "audio": False,
        "window": False
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
        else:
            assert False, "unhandled option"
    
    if(len(args) == 0):
        print("Please provide a userlist path!")
        sys.exit(2)
    
    userlist = args[0]
    
    if(os.path.exists(userlist) == False):
        print("Userlist path invalid!")
        sys.exit(2)

    if(("text/plain" in mimetypes.guess_type(userlist)) == False):
        print("Userlist must be plain text!")
        sys.exit(2)

    userlist = list(nonblank_lines(open(userlist, "r")))
    
    if(len(args) < 2):
        print("Please provide a Spotify playlist URL!")
        sys.exit(2)
    
    url = args[1] 
    
    try:
        try: req = requests.get(url).text
        except requests.exceptions.MissingSchema: req = requests.get("https://" + url).text
        except requests.exceptions.ConnectionError: req = ""
    except requests.exceptions.ConnectionError: req = ""
    
    if(("spotify" in req) == False) or (("playlist" in req) == False):
        print("Please enter a valid playlist URL!")
        sys.exit(2)
        
    if(len(userlist) < options["threads"]):
        print(f"Can't start {options['threads']} threads with {len(userlist)} user(s)!")
        sys.exit(2)

if __name__ == "__main__":
    main()