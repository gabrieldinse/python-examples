import sys

if int(sys.argv[3]) == 1:
    with open(sys.argv[1]) as infile, open(sys.argv[2], "w") as outfile:
        warnings = (l for l in infile if 'WARNING' in l)
        print(type(warnings))
        for l in warnings:
            outfile.write(l)

if int(sys.argv[3]) == 2:
    with open(sys.argv[1]) as infile, open(sys.argv[2], "w") as outfile:
        # the statement: 'for l in infile' reads a line and stores in 'l'
        for l in infile:
            print(l.strip())
            if 'WARNING' in l:
                outfile.write(l)