[Welcome Page](../README.md)  
[App README](./APP_README.md)  

## __contents__
* [exceptions.py](#exceptionspy)
* [file_interactors.py](#file_interactorspy)
* [logger.py](#loggerpy)
* [misc.py](#miscpy)
* [record_skeletons/](#record_skeletons)

#### __exceptions.py__
This file contains custom exceptions, that's all. It's not a fancy thing.
* [exceptions.py](../app/supporting_cast/exceptions.py)

#### __file_interactors.py__
This file simply does file interactions, such as creating a directory or list of directories, and pinching the AWS region out of your .pdt-config
* [file_interactors.py](../app/supporting_cast/file_interactors.py)

#### __logger.py__
This file contains the code to set up our logger. It uses the logging library, and can be used to get certain loggers.  
There are a variety of functions available and plenty of links for further reading. There are functions to set up different types of formatters, functions to set up different stream handlers, and functions to slap it all together into a cohesive logger.  
The function `get_partial_logger()` gives a logger which only outputs messages at level `INFO` and above and it sends these logs to console output only.  
The function `get_full_logger()` gives a logger which outputs any logs of level `INFO` or above to the console output and writes a copy of the output to file. In addition to that, it also outputs more detailed information to yet another file, this file captures all logs, including logs at the `DEBUG` level. This file will show what function has produced the log, at what time, from which file, and from which line in the file too.
* [logger.py](../app/supporting_cast/logger.py)

#### __misc.py__
This file just contains the on function at the minute. I suppose it's just a file for function which I couldn't decide where they should live. It currently holds `utc_timestamp_now()`, which does what it says on the tin. The reason this simple functionality is abstracted into it's own function is that I can now patch that function and control time during tests.
* [misc.py](../app/supporting_cast/misc.py)

#### __record_skeletons/__
This directory holds all the details you need for creating and validating records.  
Firstly, we have [`pet_table_models.py`](../app/supporting_cast/record_skeletons/pet_table_models.py), this file defines the pet-table DynamoDB table in a comment at the top. It then goes on to describe the fields involved in each form of record. These are Pydantic models and are used for validation, though we do not use them directly.  
Instead we use 'record factories', each record factory inherits from `AbstractRecordFactory` in the [`abstract_record.py`](../app/supporting_cast/record_skeletons/abstract_record.py) module. Now, this class is not an abstract factory, it's an abstract class which when inherited from, provides the structure for a factory.  
The abstract factory provides methods for validation and coercing records into a valid state. It is then up to each individual record factory to implement the methods:
* `__init__()` Which simply needs to assign one of the models to `self.model`.
* `_convert_model_to_record()` This method is exclusively used by the method `coerce_record_to_valid_state()`, which uses `self.model.model_validate()` (the method provided by Pydantic BaseModel), however, this method returns a model not a dictionary. So our `_convert_model_to_record()` method needs to take in a model and spit out a dictionary, this is typically done via the `produce_record()` method.
* `produce_record()` This should take in all the values for your record and simply give you a dictionary representation of the record. Nice and easy, except that most records use a timestamp in their sort-keys in order to best keep them unique amongst each other, so you generally have to come up with a way of keeping that timestamp the same if you need to but without allowing anyone to completely overwrite what the sort_key is, as the sort key defines the type of record.  

See [observation_record.py](../app/supporting_cast/record_skeletons/observation_record.py) for some ideas on how to implement those methods.  
* [record_skeletons/](../app/supporting_cast/record_skeletons/)


