def register(username,password):
    try:
        with open("res/accountfile.txt","r") as input_file:
            for line in input_file:# Read the lines
                login_info = line.split()
                print(login_info)
                if username == login_info[0] or password == login_info[1]:     
                    return 201       
        file = open("res/accountfile.txt","a")
        file.write(username)
        file.write(" ")
        file.write(password)
        file.write("\n")
        file.close()
        return 200
        
    except:
        return 404
    
def login(username,password):
    try:
        with open("res/accountfile.txt","r") as input_file:
            for line in input_file:# Read the lines
                login_info = line.split()
                print(login_info)
                if username == login_info[0] and password == login_info[1]:     
                    return 200
        return 201
    except:
        return 404