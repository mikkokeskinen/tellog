Tellog
======

A simple Telegram message logger bot.

Included components
===================

| Directory | Description |
| --- | --- |
| server | A Django project which implements a Telegram webhook and provides a JSON endpoint for reading the saved messages. |
| client | A simple React javascript app that you can use to search the messages. |

Installation
============

Clone the repository

    git clone git@github.com:mikkokeskinen/tellog.git

Change to the directory, create a Python virtualenv and activate it.

    cd tellog
    pyvenv venv
    . ./venv/bin/active

Install server dependencies

    pip install -r server/requirements.txt

Create PostgreSQL user and database

    CREATE USER tellog_server WITH PASSWORD 'changethis';
    ALTER ROLE tellog_server SET client_encoding TO 'utf8';
    ALTER ROLE tellog_server SET timezone TO 'UTC';

    CREATE DATABASE tellog_server;
    ALTER DATABASE tellog_server OWNER TO tellog_server;
    GRANT ALL PRIVILEGES ON DATABASE tellog_server TO tellog_server;

Also, allow the user to create new databases if you would like to run the
supplied tests.

    ALTER USER tellog_server CREATEDB;

Copy `server/tellog/settings/local.py.sample` to
`server/tellog/settings/local.py` and edit the database settings to match
the values used in the database.

    cp server/tellog/settings/local.py.sample server/tellog/settings/local.py
    vim server/tellog/settings/local.py

Run migrations to create the database tables

    ./server/manage.py migrate

Create a new bot into Telegram by messaging @BotFather.
See [the guide](https://core.telegram.org/bots#6-botfather).

Enter the supplied token into the setting `TELEGRAM_BOT_TOKEN` in the file
`server/tellog/settings/local.py`.

Telegram requires the bot webhook to be an SSL endpoint. I used ngrok to expose
my development machine to the web.

    ngrok http 8080

See [the ngrok docs](https://ngrok.com/docs#expose).

When you have the ngrok forwaring domain (e.g. 156eaffb.ngrok.io) use the
`set_webhook_url` command to set the bots webhook URL in Telegram:

    ./server/manage.py set_webhook_url "156eaffb.ngrok.io"

Also, add the domain to the `ALLOWED_HOSTS` setting in the
`server/tellog/settings/local.py` settings file.

Now you can start the development server. (The script runs `manage.py
runserver address 0.0.0.0:8080`)

    ./start_dev.sh

The server should now receive and save messages from Telegram.

## Tests

The few test included can be run by running:

    ./server/manage.py test server

Client
======

The client is a simple React application created using
[create-react-app](https://github.com/facebookincubator/create-react-app).

The built client is included in the repository already and is viewable at the
root of the Django project. (e.g. http://localhost:8080/)

The client development can be started by first installing the javascript
dependencies.

    cd client
    yarn install

And running

    yarnpkg start

The command will compile the app, start the development server and open
a browser at http://localhost:3000/.

The production build can be built by running

    yarnpkg run build

Search endpoint
===============

The message search endpoint is a simple Django view which returns the messages
as a list. For example making a GET request to
`http://localhost:8080/transcript/message/search` could return:

    {
        "success": true,
        "messages": [
            {
                message_id: 15,
                id: 2,
                date: "2017-03-01T18:14:41Z",
                text: "Testi",
                edit_date: null,
                obsolete: false,
                chat_name: "@kesoil",
                update_id: 178961178,
                chat_id: 338211185,
                chat_type: "private",
                from_username: "kesoil"
            }
        ]
    }

The message list can be filtered with three GET parameters:

Parameter | Description
----------|------------
q         | Includes only messages where text field contains that match the supplied value. (Using the Django [Full-text search functionality](https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/search/).
username  | Includes only messages where the from_username field is the same as the supplied value.
date      | Includes only messages that are sent on the date supplied. (Format is yyyy-mm-dd) Time of day is ignored in the query.

If the search parameters are invalid (e.g. the date is not a real date) the
endpoint will return JSON object where success is false and the errors-key contains
a list of error messages. e.g.:

    {
        "success": false,
        "errors": ["Enter a valid date."]
    }
