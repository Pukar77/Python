#In python, we normally use 4 keywords to handle errors, 
#they are as follows:

# try : write the code that might throwe error
# except : if error occurs then this block gets executed (same as catch in other languages)
# else : runs if no error occurs
# finally : alawys gets executed


try:
    num = int("20")
except Exception as e :
    print("Some error occured ", e)
else:
    print("if no error occurs, then this block also gets executed after try block")
finally:
    print("This block alawys gets executed")


