export const environment = {
  production: true,
    auth0: {
    url: require("../../auth_config.json").url, // the auth0 domain prefix
    audience: require("../../auth_config.json").audience, // the audience set for the auth0 app
    clientId: require("../../auth_config.json").clientId, // the client id generated for the auth0 app
    callbackURL: "https://foodplanner-frontend.onrender.com", // the base url of the running ionic application. 
  },
  apiServerUrl: "https://foodplanner-backend.onrender.com",
};
