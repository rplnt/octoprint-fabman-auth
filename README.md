# octoprint-fabman-auth
Authenticate [OctoPrint](http://octoprint.org/) users using [Fabman](https://fabman.io/) service.

This module works only as a "bundled" plugin and unlike regular plugins it has to live inside OctoPrint's install location.

## Installation
1. Clone this repository into `plugins` directory inside your OctoPrint source before running `setup.py install`.
    ```
    cd {OctoPrint}/src/octoprint/plugins
    git clone https://github.com/rplnt/octoprint-fabman-auth
    ```

    If you want to install this plugin without running install, check startup logs to see where are bundled plugins loaded from.

2. Adjust `config.yaml`, see section **Config**

## Config

```YAML
accessControl:

  # Change userManager to point to our FabmanUserManager class
  # default: OctoPrint's default manager using local users.yaml file
  userManager: octoprint.plugins.octoprint-fabman-auth.FabmanUserManager
  
  # Config section specific to our FabmanUserManager.
  fabman:

    # When disabled no attempt to login through Fabman API is made.
    # default: false
    enabled: true
    
    # Allow login for local users (tried first before talking to Fabman).
    # default: false
    allowLocalUsers: true

    # Url of the Fabman API.
    # default: https://fabman.io/api/v1/
    url: https://fabman.io/api/v1/

    # Fabman account ID - which account user's membership belongs to
    # You can get your account ID by either fetching the list of accounts you have access to (https://fabman.io/api/v1/documentation#!/accounts/getAccounts)
    # or by looking at the URL of your Fabman webapp (https://fabman.io/manage/<accountId>/)
    # Used API: "/accounts/{id}"
    # default: None
    accountId: ~

    # Only give rights to users are trained for specific resourceIds
    # Used API: "/members/{id}/trained-resources"
    # default: false
    restrictAccess: true

    # List of Fabman resource ids this instance handles
    # Only users with permission to *any* of these ids will get 'user' role when restrictAccess is enabled
    # default: []
    resourceIds: [1, 2, 3]
```

## Issues
* UI doesn't distinguish between regular or Fabman users - change pass and other forms are present and non-functional
* Local users can't (shouldn't have) same usernames as Fabman users

## Notes
Tested with OctoPrint version 1.3 and Fabman API v1. Provided as-is without any guarantee.
