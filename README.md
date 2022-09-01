# sf_crime_app


An app that allows you to follow the crime in San Francisco

<h1> Purpose </h1>

The purpose of this app is to allow people whoe are living in, moving to, or visiting the City to see what is going on in the areas where they are going to be.

<h1> About </h1>

This app uses DataSf, a site that has a myriad of API's based on the City's data. The particular API that is used for this project is https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783. 

The images for this project were taken from pixabay.

Future updates could possibly include google maps integration and design changes, especially the blockiness of the incedent reports.

Errors or things that are not working at the moment is the update to user pictures. There is a permissions issue where the user can't upload a picture and have it update on the user page. Another issue is when you save a watch the name can be left blank but should be rwuired. 

<h1> Technicals </h1>

To run the app from your own console, make a pull request to your machine. Navigate to the folder in the command lina dand create a virtual environment with python3 -m venv venv on a mac orlinux machine or py -m venv venv on a windows machine.

Install the dependencies in the CLI with pip -r requiremnts.txt.

There will be no database support, you will need to download postgresql and create a database with the appropritae name.

Got to your browser, Google is what I have used, and go to 127.0.0.1:5000.


The app should run in browser.






