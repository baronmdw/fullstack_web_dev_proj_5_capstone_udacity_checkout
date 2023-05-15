export const environment = {
  production: true,
  auth0: {
    url: process.env["url"], // the auth0 domain prefix
    audience: process.env["audience"], // the audience set for the auth0 app
    clientId: process.env["clientId"], // the client id generated for the auth0 app
    callbackURL: process.env["callbackURL"], // the base url of the running ionic application. 
  },
  apiServerUrl: process.env["apiServerUrl"]
};
