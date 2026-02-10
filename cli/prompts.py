#Prompt used as Main Menu
MAIN_PROMPT = """

Welcome to EZ Youtube Downloader!

To get started, choose among the options below:

1. Single Download
2. Batch Download
3. Playlist Download


Note: You can type "exit" anytime to close the program :)

"""

#Prompt for getting user input on type
TYPE_PROMPT = """
What format do you want to download?

1. Video
2. Audio only

"""

#Prompt for getting user input on URL
URL_PROMPT = """
Please enter Youtube URL (copy-paste it below)

"""

#Prompt for getting user input of Filepath
PATH_PROMPT = """
Do you want to save your download to a specific folder?


If yes, please enter the filepath with double backslashes
or forward slash
    ex. C:\\\\Users\\\\Name\\\\Videos\\\\
        C:/Users/Name/Videos/

        
Enter "no" or leave blank to save in the current directory

"""

#Prompt for user's final decision
FINAL_DECISION = """

{mode} DOWNLOAD

Title: {title}
Type: {file_type}
Path: {filepath}


"""