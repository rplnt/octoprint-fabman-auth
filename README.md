# octoprint-fabman-auth
Authenticate [OctoPrint](http://octoprint.org/) users using [Fabman](https://fabman.io/) service.

## Installation
1. Copy `fabman.py` to `/src/octoprint` in your OctoPrint installation.
2. Adjust `config.yaml` to use it, see section **Config**

## Config

```YAML
accessControl:

  # Change userManager to point to our FabmanUserManager class
  userManager: octoprint.fabman.FabmanUserManager
  
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

    # List of Fabman resource ids this instance handles; only users with access to *any* of these ids will get 'user' role
    resourceIds: [1, 2, 3]
```

## Issues
* UI doesn't distinguish between regular or Fabman users - change pass and other forms are present and non-functional
* All Fabman users have only user roles in OctoPrint
* Local users can't (shouldn't have) same usernames as Fabman users

## Notes
Tested on OctoPrint version 1.3, provided as-is without any guarantee.
