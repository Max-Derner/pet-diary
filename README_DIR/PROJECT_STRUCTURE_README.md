[Welcome Page](../README.md)

## __contents__
* [Makefile](#makefile)
* [template.yaml](#templateyaml)
* [requirements.txt](#requirementstxt)
* [.gitignore](#gitignore)

#### __Makefile__
This file currently only allows the user to run checks against the SAM template nice and quickly.  
* [Makefile README](./MAKEFILES_README.md)  
* [Makefile](../Makefile)

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
