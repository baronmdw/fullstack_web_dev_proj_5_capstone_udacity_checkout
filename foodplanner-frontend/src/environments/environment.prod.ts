export const environment = {
  production: true,
  auth0: {
    url: "${url}", // the auth0 domain prefix
    audience: "${audience}", // the audience set for the auth0 app
    clientId: "${clientId}", // the client id generated for the auth0 app
    callbackURL: "${callbackURL}", // the base url of the running ionic application. 
  },
  apiServerUrl: "${apiServerUrl}"
};
