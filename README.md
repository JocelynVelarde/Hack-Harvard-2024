# TheftWatch

## What is TheftWatch?
Shoplifting is not fun. As one of our group members has worked in retail before, it's a terrible experience for the victim. We want to give shop owners the control and the assurance that their business is secure by giving insights into shop lifting and dangerous customers, resulting in an increase in shop owner wellbeing and letting shop owners know what to watch out for.

## How does it work?
We will leverage Computer vision and classification machine learning to scan the several customers that enter a user's store, classifying customers into safe, suspicious, and dangerous based on their movements inside the store. Once they are detected to be dangerous, three things happen. We will send a Whatsapp notification to the shop owner, notifyig them of the unusual behvaior in their store.  We will also run object recognition and facial recognition to determine what was stolen and who did. After all of these are finished, we display to the user a report providing further details about the situation. We also have several other features as part of our intricate dashboard, including a heatmap of the "hot zones" where shoplifting is most common. 



## Installation

To install all of the dependencies, you'll need to first make a virtual environment like so :
```bash
py -m venv .venv
```
Next, you'll want to activate the venv like so:
```bash
.venv/Scripts/activate
```
Now navigate to the `backend` directory.
Then, you'll want to install all backend dependencies:
```bash
pip install -r requirements.txt
```

Also, please note that this is a project built on top of Streamlit, and so you'll need a `.streamlit` folder with a `secrets.toml` file with all of your streamlit api keys.

