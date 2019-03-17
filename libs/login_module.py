def register(username,password):        
    try:
        
        file = open("res/accountfile.txt","a")
        file.write(username)
        file.write(" ")
        file.write(password)
        file.write("\n")
        file.close()
        return True
        
    except:
        return True
    
def login(username,password):
    with open("res/accountfile.txt","r") as input_file:
        for line in input_file:# Read the lines
            login_info = line.split() # Split on the space, and store the results in a list of two strings
            if username == login_info[0] and password == login_info[1]:     
                return True
    return False
