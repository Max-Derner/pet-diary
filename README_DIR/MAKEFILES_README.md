[Welcome Page](../README.md)

## *__What Makefiles do we have?__*
* [cloud_report](#cloud_report)
* [app](#app)
* [destroy](#destroy)

### __cloud_report__
The command `make cloud_report` uses a phony target and will not create a file for you.  
Instead, this will validate the SAM template at `pet-diary/template.yaml`, and then run checkov against the same file for find security flaws.  
If you are using this project outside the region eu-west-2, then you need to change the Makefile to specify the region you are in.  

### __app__
The command `make app` uses a phoney target again, and deploys the app for me.  
If you are using this project, you would have to have chosen the same profile name as me, and be in the same region as me, sorry about that.  

### __destroy__
The command `make destroy` uses a phoney target again, and deletes the app for me.  
If you are using this project, you would have to have chosen the same profile name as me, and be in the same region as me, sorry about that.  