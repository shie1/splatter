import sys, getopt, os

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

if __name__ == "__main__":
    main()