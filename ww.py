from generat import *

xmldoc = open('My.xmi', 'r')
instance = CreateFromDocument(xmldoc.read())


# for item in dir(instace):
# 	print(item)

print("\nLOADING SUCCESSFUL!\n")

print('Type of instance: ', type(instance))
print('CurrentHeadPosition: ', instance.HeadPosition)



if __name__ == '__main__':
    xmldoc.close()
    from pdb import set_trace
    set_trace()