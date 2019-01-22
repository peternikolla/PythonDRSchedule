# Doctor Schedule Project
This project is built using Python/Flask.

**DR Schedule REST server**

### Problem statement

We would like to build a simple service for managing doctors and their schedules. 
Requirements:

* For each doctor we would initially like to store the following:
    * id
	* name
	* locations - represented as a collection of address strings
	* schedule - weekly schedule indicating the hours they are available each day of the week
* CRUD operations for doctors
    * Ability to book an appointment with a doctor (a tuple of (doctor, location, time)) 
    * Ability to get all appointments for a doctor
    * Ability to cancel an appointment with a doctor

Expectations/assumptions:

* The API will be internally-facing and used by other applications/services that we trust
* The API will be single-tenant (it only contains data for a single hospital)
* A doctor is available at any of their locations for any of their available times
* A doctor can only have one appointment at a time
* A doctor can travel instantaneously between locations
* No UI/front-end is expected   

#### Extra questions ####

Below are a few questions which expand the scope of the service. Please pick one and describe your approach.

* What are some real-world constraints to booking appointments that would add complexity to this API and how would they impact the design.  
**This is a simple design, we can add the ability to book more than one block of time, track the patient that booked it, track the patient that canceled an appoint.  All these would require more tables of information and better data validation. Can discuss furthur.**

* How would our design change if this API was opened up to external users?  
**If it was accessed by a user we would have the user log in and use an access token.  If accessed by another system we could use API_KEYS and/or white list IP addresses that could access the APIs**

* What concerns are there with multi-tenant data management and how could we modify the design to increase data security?
**We could have a different database for each tenant or add tenent column to the data (This could lead to leaks if not handled correctly).**

#### Suggestions ####

* Start simple 
* Document your assumptions and their impact on the design
* Stub out areas that are not related to core functionality and describe their expected behavior
* You may choose any means of persistence (ex: database, third-party service, etc.) or choose to exclude it (e.g. in-memory only). We recognize that integrating with a persistence layer may be time-consuming and by omitting it, more time can be allocated to service development.
* You may use any third-party libraries you feel are appropriate

### Who do I talk to? ###
* If you have any questions prior to your interview, please reach out to your designated Kyruus recruiting contact and he/she will get back to you as soon as possible.
* If you have any feedback on the interview question after you're done, let us know, we're always looking into improving the interview process. Thanks!


##Result

An schedule is made up of the following data:

**Schedule spec**  
doctor_id - The doctors Id  
location_id - Location of the Appointment
date - YYYY-MM-DD Date of Appointment   
time - HH:MM Time of Appointment

# REST API Endpoints

### Make Appointment
Appointments are 15 minute  
**Method:** POST  
**URI:** http://localhost:5000/appointment  
**JSON:** {"doctor_id": 1, "location_id": 1,date": "2019-02-01", "time": "11:00"}
### Get all Appointments
**Method:** GET  
**URI:** http://localhost:5000/appointments/{id}

### Cancel Appointment
**Method:** DELETE   
**URI:** http://localhost:5000/appointment   
**JSON:** {"doctor_id": 1, date": "2019-02-01", "time": "11:00"}



