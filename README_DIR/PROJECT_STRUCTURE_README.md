[Welcome Page](../README.md)

## __contents__
* [app/](#app)
* [.env](#env)
* [.gitignore](#gitignore)
* [grype-install.sh](#gyrpeinstallsh)
* [lambda_packages/](#lambda_packages)
* [Makefile](#makefile)
* [pdt](#pdt)
* [requirements.txt](#requirementstxt)
* [template.yaml](#templateyaml)
* [tests/](#tests)
* [tooling.sh](#toolingsh)
* [tox.ini](#toxini)


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

That will ensure you have your Python virtual environment set up correctly.  
You will also be able to make use of all of the functions available in pdt.  
If you ever need a reminder of what functions are available to you simply give the command `pdt help`.  

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

#### __Makefile__
Makefiles define what you can "make". This is typically used for compiling large suites of software, the documentation for this can be found [here](https://www.gnu.org/software/make/manual/make.html). Makefiles are well worth understanding if you don't already, so check that link out, you'll not need to read much to get the gist.  

For us, we use the Makefile as a way of packaging our Lambda deployment packages. To learn more about our lambda deployment packages go to the [lambda_packages section](#lambda_packages)

#### __lambda_packages/__
Our Lambdas are packaged up for deployment as ".zip file archives", to learn more about the types of lambda deployment packages checkout [this link](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html).  

They require a very distinct file hierarchy which in turn informs the file hierarchy of our `app/` directory. In the `lambda_packages/` directory, you should be able to find the directories and .zip files which relate to each of our Lambdas and the Lambda layer they use. I opted for a Lambda layer to keep all of the required pip packages in, as this keeps the lambda .zip file archives relatively slim. Keeping the size of the Lambda .zip files down allows you to edit the Lambda code directly in the AWS console. This means that you can easily check something has been deployed correctly, modify Lambdas as a quick way to experiment, etc.  

This directory will not exist yet if you have not made (or attempted to make) your first deployment. If you wish to see this directory without making a deployment you can simply invoke make directly for each of the zip packages(e.g. `make lambda_packages/lambda_libraries_layer.zip`)

#### __tox.ini__
`tox.ini` is a file that contains certain configurations for various tools you may use. I could've configure things like the AWS region in here but things only end up in here by way of a path of least resistance. Hence, at the time of writing, it only configure `flake8`.