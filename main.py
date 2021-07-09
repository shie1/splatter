import sys, getopt, os, mimetypes

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:", ["threads="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err).capitalize() + "!")
        sys.exit(2)
    threads = 1
    for o, a in opts:
        if o in ("-t", "--threads"):
            if(a.isnumeric() == False):
                print("Option -t must be an integer!")
                sys.exit(2)
            threads = int(a)
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
    

if __name__ == "__main__":
    main()