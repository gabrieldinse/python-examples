# 1:
# chama na ordem: First -> Third -> Fourth
# nao chama Second

# class First:
# def __init__(self):

#print ("first")


# class Second:
# def __init__(self):
# super().__init__()
#print ("second")


# class Third(First):
# def __init__(self):
# super().__init__()
#print ("third")


# class Fourth(Third, Second):
# def __init__(self):
# super().__init__()
#print ("that's it")


# 2:
# Chama todos, na ordem: First -> Third -> Second -> Fourth
class First:
    def __init__(self):
        print("first")


class Second:
    def __init__(self):
        super().__init__()
        print("second")


class Third(First):
    def __init__(self):
        super().__init__()
        print("third")


class Fourth(Second, Third):
    def __init__(self):
        super().__init__()
        print("that's it")
