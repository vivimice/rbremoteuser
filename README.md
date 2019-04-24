# RemoteUser Authentication Backend for ReviewBoard

This extension provides support for extracting username from `REMOTE_USER` CGI variable for ReviewBoard, makes it possible to use OpenId Connect along side with ReviewBoard (via `libapache2-mod-openidc`)

## Requirements

`ReviewBoard >= 2.0` and tested under v3.0.14

## Quick Start

First, install this extension:

```sh
git clone https://github.com/vivimice/rbremoteuser.git
cd rbremoteuser
sudo python setup.py install
```

Second, enable `rbremote.RemoteUserMiddleware` in your site's `conf/settings_local.py`：

```py
# RemoteUser Authentication Middleware is required by rbremoteuser.RemoteUserAuthBackend
RB_EXTRA_MIDDLEWARE_CLASSES = ['rbremoteuser.RemoteUserMiddleware']
```

Last, restart your webserver to take effect.

## Use

After proper installation, `RemoteUser` backend will appear on administration - Authentication backends drop list. Select it and save.

## Advanced

If you want to authenticate some account by built-in authentication backend (for web api usage for example), you can put these usernames in `LocalUsers` settings (comma-seperated)

## Limitations

* Logout is not working. (We cannot clear `REMOTE_USER` variable passed by Webserver)
* Registration and password change is not supported. (We don't save user and password information)
