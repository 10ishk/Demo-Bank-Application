# python_bank

### Below Are The Steps Required To Get The Mock Bank Running Locally:

- 1. Start By Opening 'Windows Powershell' In ADMINISTRATOR Mode (ONLY WINDOWS OS)

- 2. Type the following command in 'Windows Powershell' : 'Set-ExecutionPolicy RemoteSigned'
     (This is MANDATORY) After Typing The Command It Will Show You An Agreement, You Can Simply
     ACCEPT this Agreement By Typing 'y' as in Yes And Pressing Enter. 
     Now 'Windows Powershell' Can Be Closed (ONLY WINDOWS OS)

- 3. Next In Your Preferred Command Line (Terminal, Command Prompt, Powershell, Etc)
     Run The Following Commands:

     - Windows:
          - `> python -m pip install -r requirements.txt`
      
     - Linux/MacOS:
          - `$ pip install -r requirements.txt`

- 4. The Command Above Creates An Virtual Environment That Isolates All The Processes
      This prevents data curroption and allows us to use pre-set versions of packages that we need

- 5. Now We Can Finally Run The Python Server Using The Following Commands:

     - Windows:
          - `> python bank.py`
      
     - Linux/MacOS:
          - `$ python bank.py`

- 6. The Server Should Now Be Running And Can Be Accessed At The Following Urls:

     - a) http://127.0.0.1:42069/
     - b) http://localhost:42069/

- 7. To Stop The Server Simply Press CTRL+C

**NOTE:** Mock Bank Is Also Running ON The Following Urls

   - http://demo.amitoj.net:42069/

> Creds
**Amitoj Singh, Tanishk Bhardwaj, Pranav Vallabhaneni, Rik Mukherji**
