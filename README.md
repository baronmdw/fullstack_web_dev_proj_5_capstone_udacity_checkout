# Foodplanner App
Welcome to the Foodplanner App which serves as my Capstone project for the Udacity Fullstack developer nanodegree!

## Goals of the Project
Longterm I am planning to make this an app my parents can use to plan their weekly meals and generate a grocery list from it. I already did some market research, currently there are already many apps offering this but they do have a monthly fee so I will make this free to use for my parents. So in future the app will be able to add, edit and read receipes, add them to a weekplan and automatically generate the grocery list.

## Current state
At this state of the project the app is capable of managing the receipes and their ingredients. That means, that the users will be able to add, edit and delete receipes as well as reading the receipes. It could for example be used in a professional kitchen where the head chef edits receipes and the chefs that prepare the food can only access the receipes for reading. Therefore there are two user groups: the ones that are allowed to read, add, delete and change receipes and the ones that are only allowed to read the receipes. In order to be able to generate the grocery list in future, the groceries need to be in a different table than the receipes list.

## Access the project
The Frontend of the project can be accessed on [this](https://foodplanner-frontend.onrender.com) Link. For testing the Backend, it is hosted [here](https://foodplanner-backend.onrender.com). For the review of this project I created two dummy-users which will be deleted after the review has been done. One user es equipped with all rights, the other one with only read access, feel free to use them to log into the live-app. Their tokens should be used to test the enpdoints as well. In case the tokens expire, just log out and in in the live app and copy the updated token from the URL, I kept it in the URL for this.

### Full-rights user
Username: foodplanner_role@thismaildoesnotexist.com

Password: iAmFoodplanner!

JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJqelUxTGFYaG1fNFk5LUNPUnBxaiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWR3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDYzYjhlOTU4NDg0ZWVhOGI2YWE1MjMiLCJhdWQiOiJmb29kcGxhbmVyX2FwaSIsImlhdCI6MTY4NDQxMzczOCwiZXhwIjoxNjg0NTAwMTM4LCJhenAiOiJ3TWdvRHlXRW04U2ZLdGxTVTNSekFwQ2pwYlllTDlEdCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJlY2VpcGVzIiwiZ2V0OnJlY2VpcGVzIiwicGF0Y2g6cmVjZWlwZSIsInBvc3Q6cmVjZWlwZXMiXX0.jwxPwCaLgBRyhCl96z7Zrjp4s51Ue2PfwMSRERwj6VQAC68XdqEKv8NmBPJu858CDH9GRg0BAKA66dpwrgYgg8_lEssLqr77PDYNEW4ka6e4vwiZRTbKVSHl6_0H9JkhGxPKotoO7cC2YD7XK63asZfSxQfXCTSNHL4tdMVkAhzOSrO0kNvuyTD1f1ulurxZquWByO3ozz2j95Y4hif4fYLAUoI9lOg4jMRFpqAxdXNO0BRtk3bhRBY00Ke9NVqdM9K06zB7lT-LyBdO5YmqihQhkDrsUABKoqfQy0vgfyFwiGls71uVY0G0aWSFDDwUcXr9tRkZ2g49gRb6V88wYQ

### Read-only user
Username: reader_role@thismaildoesnotexist.com

Password: iAmReceipeReader!

JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJqelUxTGFYaG1fNFk5LUNPUnBxaiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWR3LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDYzYjk1ZTBjYzM1ZTc1NzEyNzY1OTYiLCJhdWQiOiJmb29kcGxhbmVyX2FwaSIsImlhdCI6MTY4NDQxMzgxOSwiZXhwIjoxNjg0NTAwMjE5LCJhenAiOiJ3TWdvRHlXRW04U2ZLdGxTVTNSekFwQ2pwYlllTDlEdCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnJlY2VpcGVzIl19.0SP2iqM4bGtU8qBpJoZjrX8NjYVvRni0oHBgZxtJR34FkYDVhUdw2VEKN4HI0w9aCaCwQhszr6MZ5RCSOxwEJk--MbyMooiwrzWGI95Idytqnb2IUAxUyy6VKjjQwwRzAGfomBwdsGFNxX9yzrMgv1zMSLHLJpOCVIqSFgQk_zhb3LlRSc2hCpalv04c1e3h7Ybp9B9cwfSc9WGBlzLqV2O6CmMSycH3MkYekANsPq2GfwmgLFUpcTscNzMhjXQACZMZJU9DT4l9eGoywBUs0XVFCGsveP9mTfIMhRH02cmf2JbyIYos9sbw-mfRNz7N-ThYTUANfubVazkRQVMuqw

## Run the project locally
To run the project locally you will need to setup a Flask backend and an Angular frontend, the instructions for those are described in the respective readmes:
[Backend Readme](/backend/README.md), [Frontend Readme](/foodplanner-frontend/README.md)

## Endpoint Description
The endpoints for the API are described in a separate [file](7backend/Endpoints.md).

This Git-Repository has been forked from the one that I am keeping on working in and will also be deleted once the review is finished. Therefore there is only the main branch, for developping I used a dev-Branch with a high commit-frequency and commited only to main if there were major updates.