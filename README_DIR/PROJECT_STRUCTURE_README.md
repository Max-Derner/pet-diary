[Welcome Page](../README.md)

## __contents__
* [template.yaml](#templateyaml)
* [requirements.txt](#requirementstxt)
* [.gitignore](#gitignore)
* [pdt](#pdt)
* [tooling.sh](#toolingsh)
* [.env](#env)
* [app/](#app)
* [tests/](#tests)


#### __template.yaml__
This file is the AWS SAM template. SAM stands for Serverless Application Model, and it describes the cloud infrastructure.  
Why is it a `.yaml` and not a `.json`? Well, most people do it in yaml, meaning that there's more support readily available in things like stackoverflow. YAML also support comments, so you can comment out the bits that add additional costs if you fancy it, and i can leave comments telling you where to do that.  
I did give consideration to using `.json` as there is native Python support for parsing JSON files, and I figured it would be nice to be able to parse the file for things like table names. I may just produce a make command that attempts to report on that stuff for you though.  
* [template.yaml](../template.yaml)

#### __requirements.txt__
This file details the Python requirements and should be installed after setting up the Python virtual environment, as detailed in the setup README.
* [setup README](./SET_UP_README.md)
* [requirements.txt](../requirements.txt)

#### __.gitignore__
This file tells git what files and directories should not be considered as part of the project. This allows us not include things like the venv as it is large and you should set up your own which will then be specific to your machine.
* [.gitignore](../.gitignore)

#### __pdt__
`pdt` stands for pet-diary tooling.  
It constitutes a few helpful bash functions that make life easy on a developer.  
If you're new to the project, I suggest you run the following commands in order, making sure to pay attention to the output.  

* `source ./pdt`  
* `pdt configure-venv`  
* `pdt configure-vars`  

That will ensure you have your Python virtual environment set up correctly.  
You will also be able to make use of all of the functions available in pdt.  
If you ever need a reminder of what functions are available to you simply give the command `pdt`.  
`pdt` will become available to you anytime you activate your virtual environment provided you have used `pdt` to configure your virtual environment with the `pdt configure-venv` command.
* [pdt](../pdt)

#### __tooling.sh__
`tooling.sh` contains all of the functions used by `pdt`.
* [tooling.sh](../tooling.sh)


#### __.env__
The `.env` file is simply there to be appended to your virtual environments activate script. It just fixes the Python path and sources the pdt script.
* [.env](../.env)

#### __app/__
You may be surprised to find out that all of the application's code is housed within the `app/` directory
* [app/](../app/)
* [app README](./APP_README.md)

#### __tests/__
You may also be surprised to find out that the `tests/` directory contains all of the tests for the files that are found in the `app/` directory.
* [tests/](../tests/)
