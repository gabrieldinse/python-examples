def except_function():
    raise Exception('exception')


print('teste 1')

# sem try o programa simplesmente terminaria
try:
    except_function()
except:
    pass
print('teste 2')
