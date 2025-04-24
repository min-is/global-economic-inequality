import os
import json
import opendatasets as od

def setup_kaggle_credentials():
    kaggle_username = input("Enter your Kaggle username: ")
    kaggle_key = input("Enter your Kaggle API key: ")
    
    kaggle_json = {"username": kaggle_username, "key": kaggle_key}
    kaggle_dir = os.path.expanduser('~/.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
        json.dump(kaggle_json, f)
    
    os.chmod(os.path.join(kaggle_dir, 'kaggle.json'), 0o600)
    
    print("Kaggle API credentials configured successfully!")

if __name__ == "__main__":
    setup_kaggle_credentials()