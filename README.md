# slack-rekarma

Slack user karma based on reactions.

## Usage

From a slack channel type `/rekarma`. The full user karma list will be shown inline (visible just to you).

## Integration

1. Go to **Apps and Integrations**.
2. Click on the to right button **Build your own**.
3. Click on **Make a custom integration**
4. Click on **Slash Commands**.
  - Command: `/rekarma`
5. Update the following info:
  - URL: `http://YOUR-DOMAIN/rekarma`
  - Method: `GET`

## Developing

```python
# Install python dependencies
$ pip install -r requirements.txt

# Set environment variables
$ export SREK_SLAK_API_KEY="YOUR-SLACK-API-KEY-HERE"
$ export REDIS_URL="YOUR-REDIS-URL"

# Start the flask web server
$ python runserver.py

# Start the rq worker
$ python worker.py
```

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

 * Remember to set the `SREK_SLAK_API_KEY` environment variable in your heroku app [using the heroku cli](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application).
 * You will also need to install and enable a redis addon, [redistogo](https://devcenter.heroku.com/articles/redistogo) or [heroku-redis](https://devcenter.heroku.com/articles/heroku-redis) should work.
