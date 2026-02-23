# Prompt used as Main Menu
MAIN_PROMPT_1 = """
Welcome to EZ YOUTUBE DOWNLOADER!
--Powered by yt-dlp and ffmpeg

To get started, choose among the options below:
"""

# Prompt used as Main Menu
MAIN_PROMPT_2 = """
1. Single Download

2. Batch Download


Note: You can type "exit" anytime to close the program :)

"""

# Prompt for getting user input on type
TYPE_PROMPT_1 = """
What format do you want to download?
"""

# Prompt for getting user input on type
TYPE_PROMPT_2 = """
1. Video

2. Audio only

"""

# Prompt for getting user input on URL
URL_PROMPT = """
Please enter Youtube URL (copy-paste it below)

"""


# Prompt for user's final decision
FINAL_DECISION_PROMPT = """

{mode} DOWNLOAD

Title: {title}
Type: {file_type}
Path: {filepath}

"""

# Prompt for getting txt file for batch download
GET_URL_LIST_PROMPT_1 = """
Please enter the name of the text file (with .txt) that contains all URL for download
(This must be in the directory where you ran the program)
"""

# Prompt for getting txt file for batch download
GET_URL_LIST_PROMPT_2 = """
Important Notes:
1. Text file must have ONLY one URL per line
2. You can also enter the full filepath if the text file is not in current directory

ex. C:\\\\Users\\\\Name\\\\sample.txt
    C:/Users/Name/sample.txt

"""

# Prompt if ffmpeg is not detected in system
MISSING_DEPENDENCY_PROMPT = """
Oops! ffmpeg is not detected in your system!

Would you like to download it now? y/n

"""

# Message if user does not want to download ffmpeg
DEPENDENCY_MESSAGE = """
Sorry, ffmpeg is required to run this program.
        
You can read about it here: https://www.gyan.dev/ffmpeg/builds/"
        
Note:
- ffmpeg needs to be placed in the proper directory for the program to work. If you are not
  comfortable with paths, it can be a bit confusing to do this on your own.

- Enter "y" the next time you run the program so it can do it for you :)
        
"""
