# grep.py
#
# A very simple coroutine

def grep(pattern):
    print("Looking for %s" % pattern)
    while True:
        print("Pre 'yield' keyword")
        line = (yield)
        print("Post 'yield' keyword")
        if pattern in line:
            print(line)

# Example use
if __name__ == '__main__':
    print('\nCREATES A COROUTINE:')
    g = grep("python")
    print('\nUSES NEXT IN COROUTINE:')
    next(g)
    print('\nSENDS TO COROUTINE:')
    g.send("Yeah, but no, but yeah, but no")
    print('\nSENDS TO COROUTINE:')
    g.send("A series of tubes")
    print('\nSENDS TO COROUTINE:')
    g.send("python generators rock!")