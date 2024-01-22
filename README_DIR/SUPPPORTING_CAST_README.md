[Welcome Page](../README.md)  
[App README](./APP_README.md)  

## __contents__
* [common/logger.py](#commonloggerpy)
* [common/misc.py](#commonmiscpy)
* [data_access_layer/](#data_access_layer)
* [records/](#data_access_layerrecords)
* [find_reminders.py](#find_reminderspy)
* [notifications.py](#notificationspy)
* [record_formatting.py](#record_formattingpy)

#### __common/logger.py__
This module sets up a logger from the logging library in a very particular way.  
Using the logging library allows us to send out logs at different levels, then for certain purposes we can pay attention only to specific levels depending on how much detail we want. So, anything at level `INFO` or higher will go to the console output, whilst anything at `DEBUG` or higher will go to a much more detailed .log file where it can be reviewed in case of a crash.
* [common/logger.py](../app/support/common/logger.py)

#### __common/misc.py__
This file simply contains a few small functions which don't really warrant their own module. There's time formatting, file manipulation, and a JSON encoder in here. If this file ever gets above 100 lines, I'll split it out.
* [common/misc.py](../app/support/misc.py)

#### __data_access_layer/records/__
This directory holds all the details you need for creating and validating records.  
Firstly, we have [`pet_table_models.py`](../app/support/data_access_layer/records/pet_table_models.py), this file defines the pet-table DynamoDB table in a comment at the top. It then goes on to describe the fields involved in each form of record. These are Pydantic models and are used for validation, though we do not use them directly.  
Instead we use 'record factories', each record factory inherits from `AbstractRecordFactory` in the [`abstract_record.py`](../app/support/data_access_layer/records/abstract_record.py) module. Now, this class is not an abstract factory, it's an abstract class which when inherited from, provides the structure for a factory.  
The abstract factory provides methods for validation and coercing records into a valid state. It is then up to each individual record factory to implement the following methods:
* `__init__()` Which simply needs to assign one of the models to `self.model`.
* `produce_record()` This should take in all the values for your record and simply give you a dictionary representation of the record. Nice and easy, the only thing to bare in mind is that each record form it's sort key according to specific rules such that it can be found more easily later on, so that needs to be respected and the user should not be able to alter the sort-key at all.  

You may also optionally implement the `_extra_record_validation()` method, which is automatically run by the `validate_record()` method after it has been approved by the Pydantic model. By default, it simply accepts a dictionary and returns true (see [abstract_record.py](../app/support/records/abstract_record.py)), so it is necessary that you also accept the following args and kwargs `(self, record: Dict)`. You may feel free to implement any supplemental validation you choose.

See [medication_record.py](../app/support/records/medication_record.py) for some ideas on how to implement those methods.  
* [records/](../app/support/records/)

#### __data_access_layer/__
This directory holds everything database related. The record factories and every way of interacting with the database, except for getting the initial AWS boto3 resources and clients (that's done in [common/aws_resources.py](../app/support/common/aws_resources.py)).  

There's the [put_records.py](../app/support/data_access_layer/put_records.py) module.  
Which simply contains functions to place records into DynamoDB. After passing in all the record details, these functions will; fetch a DynamoDB resource, create a RecordFactory, produce a record of the correct form, try validating the record, if the record did not validate try coercing the record into it's correct form, and then finally place that record into DynamoDB.  

There's the [get_records.py](../app/support/data_access_layer/put_records.py) module.  
Which has lots of functions which provide ways of querying the data in DynamoDB.


* [data_access_layer/](../app/support/data_access_layer/)

#### __find_reminders.py__
This is a nice and simple module.  
All it does is find records for which you should get a reminder out of the lambdas.
* [find_reminders.py](../app/support/find_reminders.py)

#### __notifications.py__
This module is all about sending notifications and formatting those notifications.
* [notifications.py](../app/support/notifications.py)

#### __record_formatting.py__
This module houses the RecordFormatter class.  
This class is responsible for all record formatting. You can format into a style which suits emails or SMS messages. You can dictate certain aspects of the formatting style by setting variables in the class.
* [record_formatting.py](../app/support/record_formatting.py)
