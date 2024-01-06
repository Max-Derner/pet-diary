[Welcome Page](../README.md)  
[App README](./APP_README.md)  

# Well out of date!
## My apologies, this needs seriously updating

## __contents__
* [data_access_layer/](#data_access_layer)
* [file_interactors.py](#file_interactorspy)
* [logger.py](#loggerpy)
* [misc.py](#miscpy)
* [records/](#records)
#### __file_interactors.py__
This file simply does file interactions, such as creating a directory or list of directories, and pinching the AWS region out of your .pdt-config
* [file_interactors.py](../app/support/file_interactors.py)

#### __logger.py__
This file contains the code to set up our logger. It uses the logging library, and can be used to get certain loggers.  
There are a variety of functions available and plenty of links for further reading. There are functions to set up different types of formatters, functions to set up different stream handlers, and functions to slap it all together into a cohesive logger.  
The function `get_partial_logger()` gives a logger which only outputs messages at level `INFO` and above and it sends these logs to console output only.  
The function `get_full_logger()` gives a logger which outputs any logs of level `INFO` or above to the console output and writes a copy of the output to file. In addition to that, it also outputs more detailed information to yet another file, this file captures all logs, including logs at the `DEBUG` level. This file will show what function has produced the log, at what time, from which file, and from which line in the file too.
* [logger.py](../app/support/logger.py)

#### __misc.py__
This file just contains the one function at the minute. I suppose it's just a file for function which I couldn't decide where they should live. It currently holds `utc_timestamp_now()`, which does what it says on the tin. The reason this simple functionality is abstracted into it's own function is that I can now patch that function and control time during tests.
* [misc.py](../app/support/misc.py)

#### __records/__
This directory holds all the details you need for creating and validating records.  
Firstly, we have [`pet_table_models.py`](../app/support/records/pet_table_models.py), this file defines the pet-table DynamoDB table in a comment at the top. It then goes on to describe the fields involved in each form of record. These are Pydantic models and are used for validation, though we do not use them directly.  
Instead we use 'record factories', each record factory inherits from `AbstractRecordFactory` in the [`abstract_record.py`](../app/support/records/abstract_record.py) module. Now, this class is not an abstract factory, it's an abstract class which when inherited from, provides the structure for a factory.  
The abstract factory provides methods for validation and coercing records into a valid state. It is then up to each individual record factory to implement the following methods:
* `__init__()` Which simply needs to assign one of the models to `self.model`.
* `produce_record()` This should take in all the values for your record and simply give you a dictionary representation of the record. Nice and easy, the only thing to bare in mind is that each record form it's sort key according to specific rules such that it can be found more easily later on, so that needs to be respected and the user should not be able to alter the sort-key at all.  

You may also optionally implement the `_extra_record_validation()` method, which is automatically run by the `validate_record()` method after it has been approved by the Pydantic model. By default, it simply accepts a dictionary and returns true (see [abstract_record.py](../app/support/records/abstract_record.py)), so it is necessary that you also accept the following args and kwargs `(self, record: Dict)`. You may feel free to implement any supplemental validation you choose.

See [medication_record.py](../app/support/records/medication_record.py) for some ideas on how to implement those methods.  
* [records/](../app/support/records/)

#### __data_access_layer/__
This directory holds things which would be considered an abstraction over the `records/` directory.  

There's the [put_records.py](../app/support/data_access_layer/put_records.py) module.  
Which simply contains functions to place records into DynamoDB. After passing in all the record details, these functions will; fetch a DynamoDB resource, create a RecordFactory, produce a record of the correct form, try validating the record, if the record did not validate try coercing the record into it's correct form, and then finally placing that record into DynamoDB.  

There's the [helpers.py](../app/support/data_access_layer/helpers.py) module.  
This just keeps things which will get used across various modules in the `data_access_layer` package. Things like providing a DynamoDB resource, things of that nature.

* [data_access_layer/](../app/support/data_access_layer/)
