#write your functions here
#we will use the name in the setup module to call the functions
#all functions will get a lsit as argument or no argument at all
# when passing argument in the setup module sepearte them using space

# func- test arg1 arg2


class Commander:
    def test(self,args):

        #print(args)
        print(f'test function called with {args} variable ')


if __name__=='__main__':

    # import Methods
    # test = getattr(Methods, 'test')
    #
    # f = lambda  :test()
    # f()

    cmd = Commander()
    method_list = [method for method in dir(Commander) if method.startswith('__') is False]
    print(method_list)


