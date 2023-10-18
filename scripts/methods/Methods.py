#write your functions here
#we will use the name in the setup module to call the functions



def test(args):

    #print(args)
    print(f'test function called with {args[0]} variable and {args[1]} avriable')


if __name__=='__main__':

    import Methods
    test = getattr(Methods, 'test')

    f = lambda  :test('heoll')
    f()
