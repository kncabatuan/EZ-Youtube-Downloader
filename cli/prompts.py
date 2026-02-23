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
To use the Batch Download feature, do the following steps:
"""

# Prompt for getting txt file for batch download
GET_URL_LIST_PROMPT_2 = """
-----Step 1-----

Open Notepad or any text file editor

-----Step 2----- (IMPORTANT!)

Copy-paste the URLs of the videos into the text file.
Ensure that there is only ONE URL per line

-----Step 3----- (IMPORTANT!)

Save the text file on your DESKTOP with file name "ez"

-----Step 4-----

Enter "proceed" once you are ready!


"""

# Prompt if ffmpeg is not detected in system
MISSING_DEPENDENCY_PROMPT = """
Oops! ffmpeg is not detected in your system!

This program uses ffmpeg and cannot run without it.

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


Closing the program . . .
"""
