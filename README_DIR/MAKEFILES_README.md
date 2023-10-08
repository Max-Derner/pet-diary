[Welcome Page](../README.md)

## *__What Makefiles do we have?__*
* [cloud_report](#cloud_report)

### __cloud_report__
The command `make cloud_report` uses a phony target and will not create a file for you.  
Instead, this will validate the SAM template at `pet-diary/template.json`, and then run checkov against the same file for find security flaws.