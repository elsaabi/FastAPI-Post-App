from authentication import utils

def test_add():
    print ('testing add function')
    password = 'MySecretPassword123'
    utils.hash(password)
    # assert add(5,3)
    

from random import randint

for i in range(5):
    print(randint(1,100))