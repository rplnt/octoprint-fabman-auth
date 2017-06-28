# octoprint-fabman-auth
Authenticate [OctoPrint](http://octoprint.org/) users using [Fabman](https://fabman.io/) service.

## Installation
1. Copy `fabman.py` to `/src/octoprint` in your OctoPrint installation.
2. Adjust `config.yaml` to use it, see section **Config**

## Config

    accessControl:
    
      # Change userManager to point to our FabmanUserManager class
      userManager: octoprint.fabman.FabmanUserManager
      
      # Config section specific to our FabmanUserManager.
      fabman:
        
        # Allow login for local users (tried first before talking to Fabman).
        # default: false
        allowLocalUsers: true
        
        # When disabled no attempt to login through Fabman API is made.
        # default: false
        enabled: true
        
        # Url of the Fabman API.
        # default: https://fabman.io/api/v1/
        url: https://fabman.io/api/v1/

## Notes
Tested on OctoPrint version 1.3, provided as-is without any guarantee.
