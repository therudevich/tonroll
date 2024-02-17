<h2>Installing</h2>

```git clone https://github.com/therudevich/tonroll.git```

<h2>Importing</h2>

```from tonroll import TonRoll```

<h2>Initializing</h2>

```tonroll = TonRoll(token)```

You can get your access token on [ tonroll.com](https://tonroll.com) > DevTools > Application > Cookies (https://tonroll.com) > access

<h2>Using examples</h2>
<h3>Getting balances</h3>

```
me = tonroll.getMe()
myBalance = me['data']['me']['balance'] # {'ton' : ..., 'demo' : ...}
  
``` 

<h3>Activating promocode</h3>

```
tonroll.activatePromocode('promocode')

``` 

<h3>Handlers</h3>

```
@tonroll.rollNewGameHadler()    # handler for new roll game
def new_roll_game(msg):
  ...

@tonroll.rollGameStartHandler()    # handler for roll game ends getting bets and starts
def roll_game_starts(msg):
  ...
```

