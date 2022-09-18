# Linkedin_2nd_connection

## Configuration

Version 1 for Win10, google chrome webdriver 15

Make sure your default chrome version matches the driver you wanna use!

### Helpful sources

Your default chrome version can be checked by tips here: https://www.digitalcitizen.life/version-google-chrome/

Driver can be download here: https://chromedriver.chromium.org/downloads

## Run the code
Download the necessary packages by:
```bash shell
pip install -r requirements.txt
```

To run the program, please edit the cfg.yaml and add your username, password to LinkedIn. The school name is used for filtering your alumni.
```yaml cfg.yaml
username: user@email.com
password: pwd
school: ABC University
```

Then it can be started by: 
```bash shell
python run.py
```

The whole flow can be prsented by demo_processed.mp4

https://user-images.githubusercontent.com/66770967/190921368-45709366-1bed-422c-8c74-01225fdcdcff.mp4

## Warnings

LinkedIn official may ask you to check the unusual activities caused by a great amout of user profiles viewing. Use this program rationally.
<img src="https://user-images.githubusercontent.com/66770967/190923752-10d738f1-c683-4276-9a6a-fd959e655e9f.png" width="600" height="400">
