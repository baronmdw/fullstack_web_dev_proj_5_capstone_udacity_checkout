# Endpoint description
Currently there are two endpoints that are linked to receipes, one with general access and one with access to a specific receipe.

## Receipes
This is the endpoint to address receipes in general.
### GET
The get endpoint is accessible with both user-groups, it needs the "get:receipes" permission and returns a JSON object, containing a success-status and the receipes without ingredients as objects within a list. The Authentication does need to be included in a Bearer token header, ideally it is tested with postman, set the JWT in the Bearer Token point in the Authorization tab. For local testing replace the backend address by your localhost address.
```
GET https://foodplanner-backend.onrender.com/receipes
```
A successful request will look like this:
```JSON
{
    "receipes": [
        {
            "description": "Abenteuer dazu ",
            "id": 2,
            "name": "Spannendes leben"
        },
        {
            "description": "Auflösen und stehen lassen bis es schwarz ist",
            "id": 3,
            "name": "Coca cola"
        }
    ],
    "success": true
}
```

### POST
The post endpoint is only accessible for a user with the "foodplanner" role, it needs the "post:receipes" permission and returns the id of a freshly created object as well as a success status within a JSON object. To address it the requests needs a Bearer token in the Authorization header and needs to contain following JSON object in the body:
```
POST https://foodplanner-backend.onrender.com/receipes
```
```JSON
{
    "name": "Test Receipe",
    "receipe": "This has been inserted with Postman",
    "ingredients": [{"name": "Test ingredient", "unit": "no unit", "amount": 1}]
}
```
Successful creation wil result in this response:
```JSON
{
    "id": 4,
    "success": true
}
```

## Receipes/id
This endpoint serves the interaction with a specific receipe.

### GET
This endpoint is accessible for all roles, it needs the "get:receipes" permission and returns a JSON object containing the receipe object and a list of ingredients objects. TO address it the request needs a Bearer token in the Authorization header and a valid id.
```
GET https://foodplanner-backend.onrender.com/receipes/4
```
Successful request will result in a response similar to this:
```JSON
{
    "ingredients": [
        {
            "amount": 1.0,
            "id": 6,
            "name": "Test ingredient",
            "unit": "no unit"
        }
    ],
    "receipe": {
        "description": "This has been inserted with Postman",
        "id": 4,
        "name": "Test Receipe"
    }
}
```

### PATCH
This endpoint is accessible for the foodplaner role and needs the "patch:receipes" permission. The request needs to contain a Bearer token in the Authorization header and a JSON object containing the name of the receipe, the receipe itself and a list of ingredients containing name, unit and amount of each element. It will respond with a success status and the id of the freshly updated element.
```
PATCH https://foodplanner-backend.onrender.com/receipes/4
```
The body should contain a JSON object like this:
```JSON
{
    "name": "Test Receipe",
    "receipe": "This has been updated with Postman",
    "ingredients": [{"name": "Test ingredient", "unit": "no unit", "amount": 1}, {"name": "Second Test Ingredient", "unit": "no unit", "amount": 1.5}]
}
```
A successful request will look like this:
```JSON
{
    "id": 4,
    "success": true
}
```

### DELETE
This endpoint is accessible for the foodplaner role and needs the "delete:receipes" permission as well as a Bearer token in the header and will delete the corresponding receipe and send a success status.
```
DELETE https://foodplanner-backend.onrender.com/receipes/4
```
Successful request will result in this response:
```JSON
{
    "success": true
}
```

## Errorcodes
Experimenting with your own requests, this are the most common error codes that might occur:

400: Means that there was an issue with the request format
401: Means that the authentication did not work correctly, if on the frontend try to log in and out or only use functions you are allowed to use.
404: Means that the element that should be accessed does not exist
422: Means some error occured on the server
500: This should not appear to you but if so there was an uncaught error, I would highly appreciate feedback for that!
