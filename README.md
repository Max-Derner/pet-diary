

# *__WELCOME__*
Hi, I'm Max Derner and I created this application.  

This project is intended to serve as a pet diary of sorts.  
Using this application you can create records against a DynamoDB table that: 

* Contain details about your pets such as name, microchip number, colour, date of birth
* records a vet appointment
* records vaccinations and medications administered and when they are next due
* records any observations you may have had about them that could be useful in diagnosing health conditions (e.g. stopped eating on x date, vomited on x day, etc)  

There are also scheduled lambda functions which will query the database and check if you have any upcoming appointments or need to administer any medication soon. One lambda will then e-mail you with anything you need to be aware of up to 2 weeks in advance. The other lambda will send you an SMS text message on the day.

You will also be able to generate summary reports on your pets. These can then be sent to your vets, so they are aware of your records, and can more easily diagnose any health issues your pet may have.

Please follow the links below to navigate to the rest of the READMEs  

* [Set up](./README_DIR/SET_UP_README.md)
* [Project structure](./README_DIR/PROJECT_STRUCTURE_README.md)
* [Cost Breakdown](./README_DIR/COSTS_README.md)
* [My TODO list](./README_DIR/TODO_README.md)

