# Linkedin_2nd_connection

This project aims to automatically send connection requests to your 2nd connections who are also your alumni judging based on your highlights. To run this code, your python version should be 3.7/8/9/10/11. 
## Set up
Pip install required packages
```bash shell
pip install -r requirements.txt
```

## Edit [LinkedIn account setting and school name](config.yaml)
```yaml config.yaml
username: user@email.com
password: pwd
school: ABC University # We will determine alumni based on the name of school, so be careful of typos
```

## Edit [greeting text](greeting_alumni.txt) if needed
```text greeting_alumni.txt
Hi ?name?
I noticed you are also in the ?school? Alumni networking group here on LinkedIn, and I really hope to have one of your connections. Best regards.
```
`?name?` will be pending connector's First name and `?school?` will be identical to the school name you configurated [here](config.yaml). 

## Run the code
```bash shell
python run.py --headless [bool: False] --config [path: 'config.yaml'] --request-num [int: 20] --greet-txt [path: greeting_alumni.txt]
```
- `--headless`: hide browser while operating
- `--request-num`: the number of requests you want to send

The whole flow can be prsented by demo_processed.mp4

https://github.com/WSpie/Linkedin_2nd_connection/assets/66770967/accad9fb-12b4-404e-9e72-daafe25457fa


## Warnings

- If you are not Premium member, you will only have limited connection requests to send and it will show this image if you reached the limits.

<img src="https://github.com/WSpie/Linkedin_2nd_connection/assets/66770967/c8de26b9-f378-4c0f-83cf-2064bf6275f7"#center width="300" height="250">

- If you are already a Premium member, LinkedIn official may ask you to check the unusual activities caused by a great amount of user profiles viewing. Use this program rationally.

<img src="https://user-images.githubusercontent.com/66770967/190923752-10d738f1-c683-4276-9a6a-fd959e655e9f.png"#center width="600" height="400">

If this warning displayed, just wait as required. I will add more humanlike operations in ver 2.0.
