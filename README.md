#Weather bot

Telegram bot to receive weather.
#Start

Clone the repository `git clone https://github.com/s1mple-prog/WeatherBot.git`

Install requirements:

```
$ pip install -r requirements.txt  
```
Create database:
```
$ touch server.db
```

Get a token from @BotFather and create environment variable with name "**BOT**" [Guide how to create enviromental variable](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).

In this project I used the weatherbit API to get weather data you should get [API KEY](https://www.weatherbit.io/).

Create environment variable with name "**WEATHER**" with the key value that you received on the weather bit.

That's all, run in the terminal ` python3 bot.py `