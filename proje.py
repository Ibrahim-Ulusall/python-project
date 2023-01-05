import os,sys,time,json,random,smtplib

class membershipSystem:

    #region init
    def __init__(self) -> None:
        self.__users = {}
        self.email = ''
        self.__activationCode = ''
    #endregion

    #region menu
    def menu(self):
        _m = """
            Delta Software Panel

            1 - Sign Up
            2 - Login
            3 - Forgot Password
            4 - Quit
        """
        try:
            print(_m)
            choice = int(input('Please enter the number of the transaction you want to do: '))

            while choice < 0 or choice > 4:
                print('Please enter a value between 1 and 4 : ')
                choice = int(input('Choice : '))
            if choice == 1:
                self.signUp()
            elif choice == 2:
                self.login()
            elif choice == 3:
                self.forgotPassword()
            else:
                self.__program()
                sys.exit()
        except ValueError:
            print('Cannot contain textual expressions and spaces!')
            time.sleep(1)
            self.__program()
            self.menu()
    #endregion

    #region CreateActivationCode
    def _createActivationCode(self) -> str: #Aktivasyon Kodu üret
        
        charSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','o','p','r','s','t','u','v','y','z','w','x',1,2,3,4,5,6,7,8,9,'@','!','^','$','%','&','?']
        for i in range(10):
            self.__activationCode += str(random.choice(charSet))
        return self.__activationCode
    #endregion

    #region SendActivationCode
    def _sendActivationCode(self) -> None: #Aktivasyon Kodu gönder
        smtpServerName = 'smtp.gmail.com'
        smtpServerPort = 587
        try:
            fromAddress = ''
            password = ''
            smtpServer = smtplib.SMTP(smtpServerName,smtpServerPort)
            smtpServer.ehlo()
            smtpServer.starttls()
            smtpServer.login(fromAddress,password)
            smtpServer.sendmail(fromAddress,self.email,self._createActivationCode())
        except Exception as e:
            print(e)
        finally:
            smtpServer.close()
    #endregion

    #region writerActivationCode
    def writerActivationCode(self):
        with open('activationCode.txt','w',encoding='utf-8') as file:
            file.write(self._createActivationCode())
    #endregion

    #region ForgotPassword
    def forgotPassword(self) -> None: # Şifremi Unuttum
        email = str(input('Email Address : '))
        if email != None:
            if self.emailControl(email):
                self.email = email        
                try:
                    
                    print('1 - Send Mail')
                    print('2 - Write to File')
                    print('3 - Cancel')
                    choice = int(input('Please enter the number of the transaction you want to do: '))

                    while choice < 0 or choice > 3:
                        print('Please enter a value between 1 and 3 : ')
                        choice = int(input('Choice : '))
                    if choice == 1:
                        self._sendActivationCode()
                    elif choice == 2:
                        self.writerActivationCode()
                        print(self.__activationCode)
                        activationCode = str(input('Activation Code : '))
                        if activationCode != None:
                            if self.activationCodeControl(activationCode):
                                self.changePassword()
                            else:
                                print('Incorrect Activation Code')
                    else:
                        self.__program()
                        self.menu()
            
                except ValueError:
                    print('Cannot contain textual expressions and spaces!')
                    time.sleep(1)
                    self.__program()
                    self.forgotPassword()
            else:
                print("Email Address Incorrect")
                time.sleep(1)
                self.__program()
                self.forgotPassword()
    #endregion

    #region changePassword
    def changePassword(self):
        try:
            newPassword = str(input('New Password : '))
            newPasswordAgain = str(input('New Password Again : '))
            while newPassword != newPasswordAgain:
                print('Passwords Do Not Match')
                newPassword = str(input('New Password : '))
                newPasswordAgain = str(input('New Password Again : '))
            with open('users.json','r',encoding='utf-8') as jsonFile:
                users = json.load(jsonFile)
            with open('users.json','w',encoding='utf-8') as file:
                users['users'][0]['password'][self.passwordIndexContol()] = newPassword
                json.dump(users,file)
        except ValueError as e:
            print(e)
            time.sleep(1)
            self.clearTerminal()
            self.changePassword()

    #endregion

    #region Password Index Control 
    def passwordIndexContol(self):
        with open('users.json','r',encoding='utf-8') as jsonFile:
            self.__users = json.load(jsonFile)
            for user in self.__users['users']:
                for email in user['email']:
                    if self.email == email:
                        return user['email'].index(self.email)
            
    #endregion

    #region signUp
    def signUp(self) -> None: # üye Ol
        pass
    #endregion

    #region ActivationCodeControl
    def activationCodeControl(self,code):
        if self.__activationCode != code:
            return False
        return True
    #endregion

    #region EmailControl
    def emailControl(self,mail) -> bool:
        with open('users.json','r',encoding='utf-8') as jsonFile:
            self.__users = json.load(jsonFile)
            for user in self.__users['users']:
                for email in user['email']:
                    if mail == email:
                        return True
        return False
    #endregion
    
    #region Login
    def login(self): #Giriş Yap
        pass
    #endregion

    #region clearTerminal
    def clearTerminal(self) -> None:
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
        else:
            pass
    #endregion

    def __program(self):
        self.clearTerminal()
        for i in range(3,0,-1):
            print('\rThe program will restart after %s seconds'%(i),end='')
            time.sleep(1)
        print() 
user = membershipSystem()
user.menu()