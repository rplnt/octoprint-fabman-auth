# octoprint-fabman-auth
Authenticate [OctoPrint](http://octoprint.org/) users using [Fabman](https://fabman.io/) service.

## Installation
1. Clone this repository into `plugins` directory inside your OctoPrint *install* folder
    ```
    cd {OctoPrint}/src/octoprint/plugins
    git clone https://github.com/rplnt/octoprint-fabman-auth
    ```
2. Adjust `config.yaml`, see section **Config**

## Config

```YAML
accessControl:

  # Change userManager to point to our FabmanUserManager class
  # default: OctoPrint's default manager using local users.yaml file
  userManager: octoprint.plugins.octoprint-fabman-auth.FabmanUserManager
  
  # Config section specific to our FabmanUserManager.
  fabman:
    
    # Allow login for local users (tried first before talking to FM).
    # default: false
    allowLocalUsers: true
    
    # When disabled no attempt to login through Fabman API is made.
    # default: false
    enabled: true
    
    # Url of the Fabman API.
    # default: https://fabman.io/api/v1/
    url: https://fabman.io/api/v1/

    # Only give rights to users who have resource with id specified in resourceIds
    # default: false
    restrictAccess: true

    # List of Fabman resource ids this instance handles
    # Only users with permission to *any* of these ids will get 'user' role when restrictAccess is enabled
    # default: []
    resourceIds: [1, 2, 3]
```

## Issues
* UI doesn't distinguish between regular or Fabman users - change pass and other forms are present and non-functional
* Only first "member" of Fabman user is used for permission management
* Local users can't (shouldn't have) same usernames as Fabman users

## Notes
Tested on OctoPrint version 1.3, provided as-is without any guarantee.
