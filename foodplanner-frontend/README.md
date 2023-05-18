# FoodplannerFrontend
Welcome to setting up your frontend, before running locally, please understand how the frontend is used:
First of all you have to login to the app with the credentials provided in the [Readme](../README.md).
Afterwards hit update to see all receipes that are listed on the server. To get the details just click on the receipe name, where you then can edit the receipe or delete it. Since it's all mock data, feel free to play around. On the big "plus" button on top of the you can add a new receipe, please add the ingredients first one at a time and hit the add ingredient button after filling in the form. Submit to database will either post a new receipe or patch an existing one.

Curious what receipes you will have to offer for me :)

## Run locally
Please make sure you have Node version 18.16.0 installed and activated. Afterwards being cd-ed into foodplanner-frontend install all packages (this might take a while):
```console
npm install
```

Afterwards you can run a local version with
```console
ng serve --open
```

## Generic Angular information, kept as a service
This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 14.2.3.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
