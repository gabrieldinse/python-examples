def foo(lst):
    del lst[0]
    
lst = [1, 2, 3]
foo(lst)
print(lst)