# Healthier Food Choices

## Introduction
The script utilises chromedriver, selenium, and python to automate the process of messaging participants at pre-determined timings. This way, participants may receive messages and pictures according to the various phase according to the phase they are in. From the `names.txt` file, a list of participant IDs tagged by the Day is fed into the program, As the study progresses, the Days increases, the participant ID is updated and stored in a `names_next.txt` file. The cycle completes until the participant exits the cycle of the study or drops off from the study.

## Pre-requisite
1. Chrome Browser (Check the version of your chrome browser)
2. ChromeDriver (Download the corresponding chromedriver based on your chrome browser over [here](https://chromedriver.chromium.org/downloads) and move the binary executable file to this app root folder) (Note: please download the relevant ones depending on your operating system).
3. Python3

## How to Use
1. Clone this github repository into the local computer.
2. Prepare your participant list with the ones included in the [Excel spreadsheet](./Participant_List.xlsx) (Note: the participant id need to be stored as the names and should be able to be found in the Whatsapp mobile application).
3. Copy the Participants' ID and tag from Column F of the [Excel spreadsheet](./Participant_List.xlsx) into the names.txt.
4. Create a virtual environment with Python3 `python3 -m venv ./venv; source ./venv/bin/activate; pip install --upgrade pip; pip install -r requirements.txt`
5. Run the following command `nohup python main.py &`
6. Log in to the Whatsapp Web Browser with your mobile, and the program will send the messages and images at the preset time, which could be set in [main.py Line 202](./main.py)
6. The logs can be monitored via `timelogger.txt`, which is updated on a regular basis.

## References
1. Wan, K.; Choo, B.J.; Chan, K.; Yeo, J.Y.; Tan, C.S.; Quek, B.; Gan, S.K. Fear, Peer Pressure, or Encouragement: Identifying Levers for Nudging Towards Healthier Food Choices in Multi-Cultural Singapore. Preprints 2021, 2021110551 (doi: [10.20944/preprints202111.0551.v1](https://www.preprints.org/manuscript/202111.0551/v1)).
