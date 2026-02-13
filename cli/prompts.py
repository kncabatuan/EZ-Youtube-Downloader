# Prompt used as Main Menu
MAIN_PROMPT_1= """

Welcome to EZ Youtube Downloader!

To get started, choose among the options below:
"""

# Prompt used as Main Menu
MAIN_PROMPT_2= """
1. Single Download
2. Batch Download
3. Playlist Download


Note: You can type "exit" anytime to close the program :)

"""

#Prompt for getting user input on type
TYPE_PROMPT_1 = """
What format do you want to download?
"""


#Prompt for getting user input on type
TYPE_PROMPT_2 = """
1. Video
2. Audio only

"""


#Prompt for getting user input on URL
URL_PROMPT = """
Please enter Youtube URL (copy-paste it below)

"""

#Prompt for getting user input of Filepath
PATH_PROMPT_1= """

Do you want to save your download to a specific folder?
"""


#Prompt for getting user input of Filepath
PATH_PROMPT_2= """
If yes, please enter the filepath with double backslashes
or forward slash
    ex. C:\\\\Users\\\\Name\\\\Videos\\\\
        C:/Users/Name/Videos/

        
Enter "no" or leave blank to save in the current directory

"""


#Prompt for user's final decision
FINAL_DECISION_PROMPT = """

{mode} DOWNLOAD

Title: {title}
Type: {file_type}
Path: {filepath}

"""


GET_URL_LIST_PROMPT_1= """

Please enter the name of the text file (with .txt) that contains all URL for download
(This should be located in the directory of this program)
"""


GET_URL_LIST_PROMPT_2= """
Important Notes:
1. Text file must have ONLY one URL per line
2. You can also enter the full filepath if the text file is not in current directory

ex. C:\\\\Users\\\\Name\\\\sample.txt
    C:/Users/Name/sample.txt

"""