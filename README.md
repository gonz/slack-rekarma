# slack-rekarma

Slack user karma based on reactions.

## Usage

From a slack channel type `/rekarma`. The full user karma list will be shown inline (visible just to you).

## Integration

1. Go to your channel
2. Click on **Configure Integrations**.
3. Scroll all the way down to **DIY Integrations & Customizations section**.
4. Click on **Add** next to **Slash Commands**.
  - Command: `/rekarma`
  - URL: `http://YOUR-DOMAIN/rekarma`
  - Method: `GET`

## Developing

```python
# Install python dependencies
$ pip install -r requirements.txt

# Set environment variables
$ export SREK_SLAK_API_KEY="YOUR-SLACK-API-KEY-HERE"

# Start the server
$ python app.py
```

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Remember to set the `SREK_SLAK_API_KEY` environment variable in your heroku app [using the heroku cli](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application).
