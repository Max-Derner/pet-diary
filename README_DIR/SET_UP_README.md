[Welcome Page](../README.md)

# Contents
* [Setting up AWS](#setting-up-aws)
* [Setting up Python virtual environment](#setting-up-python-virtual-environment)
* [Getting the app deployed](#getting-the-app-deployed)

## *__Setting up AWS__*
First, you'll need to go to `aws.amazon.com` and set yourself up an account.  
Now that you have an AWS root account, you should set up MFA.  
Search for `Identity and Access Management (IAM)` in the search bar and set up MFA for your root user.  

Work through the rest of the `AWS-TODO.txt` items found [here](../AWS-TODO.txt).  
There's plenty of documentation available online, anything I write down here will invariably become outdated, and I trust your Googling abilities.  


## *__Setting up Python virtual environment__*
You will of course need Python installed first.  
For Linux users type `which python` or `which python3`  
If nothing comes up for you, you will need o install Python.  
For Linux users you can install it with the following `sudo apt update && sudo apt install python3 -y`  
That command will first update your known packages, and if successful will then install Python 3 and bypass the user input of having to confirm this is the package you want.  

To set up the virtual environment see the [pdt entry in the Project Structure section](./PROJECT_STRUCTURE_README.md#pdt) of the READMEs


## *__Getting the app deployed__*
Well, if everything else has been done correctly, you should just be able to issue the following commands:
```
pdt aws-login
``````
pdt sam-deploy
```
Once the application is fully deployed, you'll want to subscribe yourself to the various topics to start getting notifications. Use 
```
pdt subscribe
```
 to subscribe yourself to the notifications and that's it, you should be all set.
