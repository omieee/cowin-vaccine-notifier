# Cowin Vaccine Notifier

## Get the vaccine for a given age group in a given district. Runs 1 requests per 3 second

### STEPS (TO RUN FROM SOURCE CODE)
- Python 3.6 + required
- Take the git pull, if you wish you can create a virtualenv
- Install requirements
```sh
pip install -r requirements.txt
```
- run the python script
```sh
 #This will run for age group 18+ and district with id 294 (Bangalore BBMP district)
python runner.py 18 294
```

## Executable file
- You can find the executable file under dist folder which can be directly executed (ONLY on WINDOWS). You might need VC++ redistributable

## Disclaimer

- Data is based on COWIN's API at (https://apisetu.gov.in/public/marketplace/api/cowin)
- Data could be stale
- This application has no mechanism for registration use Government approved app only for registration
- Author doesn't take responsibility for datamismath and negative impact caused by it whatsoever.
- Use this only for information purpose to check status
