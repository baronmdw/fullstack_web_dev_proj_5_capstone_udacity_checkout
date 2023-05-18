# Foodplanner App
Welcome to the Foodplanner App which serves as my Capstone project for the Udacity Fullstack developer nanodegree!

## Goals of the Project
Longterm I am planning to make this an app my parents can use to plan their weekly meals and generate a grocery list from it. I already did some market research, currently there are already many apps offering this but they do have a monthly fee so I will make this free to use for my parents. So in future the app will be able to add, edit and read receipes, add them to a weekplan and automatically generate the grocery list.

## Current state
At this state of the project the app is capable of managing the receipes and their ingredients. That means, that the users will be able to add, edit and delete receipes as well as reading the receipes. It could for example be used in a professional kitchen where the head chef edits receipes and the chefs that prepare the food can only access the receipes for reading. Therefore there are two user groups: the ones that are allowed to read, add, delete and change receipes and the ones that are only allowed to read the receipes. In order to be able to generate the grocery list in future, the groceries need to be in a different table than the receipes list.

## Access the project
The project can be accessed on [this](https://foodplanner-frontend.onrender.com) Links. For testing the Backend, it is hosted [here](https://foodplanner-backend.onrender.com). For the review of this project I created two dummy-users which will be deleted after the review has been done. One user es equipped with all rights, the other one with only read access, feel free to use them to log into the live-app. Their tokens should be used to test the enpdoints as well:

### Full-rights user
Username: foodplanner_role@thismaildoesnotexist.com
Password: iAmFoodplanner!
JWT: tbd

### Read-only user
Username: reader_role@thismaildoesnotexist.com
Password: iAmReceipeReader!
JWT: tbd

## Run the project locally
To run the project locally you will need to setup a Flask backend and an Angular frontend, the instructions for those are described in the respective readmes:
[Backend Readme](/backend/README.md), [Frontend Readme](/foodplanner-frontend/README.md)

## Endpoint Description
The endpoints for the API are described in a separate [file](7backend/Endpoints.md).

This Git-Repository has been forked from the one that I am keeping on working in and will also be deleted once the review is finished.