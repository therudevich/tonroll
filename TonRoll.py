import websockets
import functools
import requests
import json
import asyncio

from .queries import queries, socket_queries


class TonRoll:
	API_URL = "https://tonroll.com/api"
	SOCKETS_URI = "wss://tonroll.com/sockets"
	AVAILABLE_CURRENCIES = ['ton', 'demo']
	AVAILABLE_ROLL_CHOICES = ['blue', 'green', 'red']
	OVERALL_GAMES_LOG_TYPES = ['AllGames', 'MyGames', 'HightRollers', 'BigWins', 'DuckFlipGame']
	DUCKFLIP_SIDES = ['MRDUCK', 'MRSDUCK']
	MESSAGE_REACTIONS = {'🤯' : 'shocked_face_with_exploding_head',
						 '🤔' : 'thinking_face', 
						 '👍' : 'thumbsup', 
						 '😱' : 'scream', 
						 '❤️' : 'heart', 
						 '🔥' : 'fire', 
						 '🎉' : 'tada', 
						 '👏' : 'clap', 
						 '🙏' : 'pray', 
						 '💩' : 'shit',
						 '😭' : 'sob'}

	subscriptions = {}

	def __init__(self, token: str | None = None):
		self.headers = None if not token else {
			"Cookie" : "access={};refresh={}".format(token, token)
		}
		self.operationName = None

	def __send_request(self, variables: dict = {}) -> dict:
		responce = requests.post(self.API_URL, headers = self.headers, json = {
				"operationName" : self.operationName,
				"variables" : variables,
				"query" : queries[self.operationName]
			}
		)
		return responce.json()

	def getServerTime(self):
		self.operationName = "GetServerTime"
		return self.__send_request()

	def getMainWalletInfo(self):
		self.operationName = "getMainWalletInfo"
		return self.__send_request()

	def getMe(self):
		self.operationName = "getMe"
		return self.__send_request()

	def getDemoBalance(self):
		self.operationName = "GetDemoBalance"
		return self.__send_request()

	def getMyAuth(self):
		self.operationName = "getMyAuth"
		return self.__send_request()

	def getWalletTransactionList(self):
		self.operationName = "GetWalletTransactionList"
		return self.__send_request()

	def getRollGame(self):
		self.operationName = "getRollGame"
		return self.__send_request()

	def placeRollGameBet(self, amount: int | float, choice: str, currency: str):
		self.operationName = "placeRollGameBet"
		return self.__send_request({'amount': amount, 'choice': choice, 'currency': currency})

	def getRollGamesResultHistory(self):
		self.operationName = "getRollGamesResultHistory"
		return self.__send_request()

	def startMinesGame(self, amount: int | float, minesCount: int, currency: str):
		self.operationName = "startMinesGame"
		return self.__send_request({'betAmount': amount, 'minesCount': minesCount, 'currency': currency})

	def getMinesGame(self):
		self.operationName = "getMinesGame"
		return self.__send_request()

	def checkMinesGameCell(self, cellNumber: int):
		self.operationName = "checkMinesGameCell"
		return self.__send_request({'cellNumber' : cellNumber})

	def endMinesGame(self):
		self.operationName = "endMinesGame"
		return self.__send_request()

	def getMinesGamesFairness(self):
		self.operationName = "GetMinesGamesFairness"
		return self.__send_request()

	def getOverallGamesLog(self, type: str):
		self.operationName = "GetOverallGamesLog"
		return self.__send_request({'type' : type})

	def playDuckFlipGame(self, chosenSide: str, amount: int | float, currency: str):
		self.operationName = "PlayDuckFlipGame"
		return self.__send_request({'chosenSide' : chosenSide, 'amount' : amount, 'currency' : currency})

	def getDuckFlipGame(self, currency: str):
		self.operationName = "GetDuckFlipGame"
		return self.__send_request({'currency' : currency})

	def getDuckFlipGameLastResults(self):
		self.operationName = "GetDuckFlipGameLastResults"
		return self.__send_request()

	def getDuckFlipGameFairness(self):
		self.operationName = "GetDuckFlipGameFairness"
		return self.__send_request()

	def getChatRoom(self):
		self.operationName = "GetChatRoom"
		return self.__send_request()

	def sendMessageToChatRoom(self, content: str):
		self.operationName = "sendMessageToChatRoom"
		return self.__send_request({'content' : content})

	def reactToMessageInChatRoom(self, messageId: str, content: str):
		self.operationName = "ReactToMessageInChatRoom"
		return self.__send_request({'messageId' : messageId, 'content' : content})

	def activatePromocode(self, code: str):
		self.operationName = "activatePromocode"
		return self.__send_request({'code' : code})


	@classmethod
	def rollGameStartHandler(cls):
		def decorator(func):
			event_id = "677214fe-d27f-4ba3-9176-11b0387c314b"
			query = socket_queries['onRollGameUpdate']
			variables = {}
			extensions = {}
			operationName = "onRollGameUpdate"
			subscription_exists = True
			if event_id not in cls.subscriptions:
				cls.subscriptions[event_id] = []
				subscription_exists = False

			cls.subscriptions[event_id].append({
				'func' : func, 
				'query' : query, 
				'variables' : variables, 
				'extensions' : extensions, 
				'operationName' : operationName, 
				'subscription_exists' : subscription_exists,
				'path' : ['payload', 'data', 'game', '__typename'], 
				'typename' : 'RollGameStart',
				'type' : 'subscribe'
			})

			@functools.wraps(func)
			async def wrapper(*args, **kwargs):
				return await func(*args, **kwargs)
			return wrapper
		return decorator


	@classmethod
	def rollNewGameHadler(cls):
		def decorator(func):
			event_id = "677214fe-d27f-4ba3-9176-11b0387c314b"
			query = socket_queries['onRollGameUpdate']
			variables = {}
			extensions = {}
			operationName = "onRollGameUpdate"
			subscription_exists = True
			if event_id not in cls.subscriptions:
				subscription_exists = False
				cls.subscriptions[event_id] = []

			cls.subscriptions[event_id].append({
				'func' : func, 
				'query' : query, 
				'variables' : variables, 
				'extensions' : extensions, 
				'operationName' : operationName, 
				'subscription_exists' : subscription_exists,
				'path' : ['payload', 'data', 'game', '__typename'], 
				'typename' : 'RollGameNewGame',
				'type' : 'subscribe'
			})

			@functools.wraps(func)
			async def wrapper(*args, **kwargs):
				return await func(*args, **kwargs)
			return wrapper
		return decorator

	@classmethod
	def rollGamesResultHistoryHandler(cls):
		def decorator(func):
			event_id = "5bce8c9f-de59-4458-ae09-551a9997ac8a"
			query = socket_queries['onRollGamesResultHistoryUpdate']
			variables = {}
			extensions = {}
			subscription_exists = True
			operationName = "onRollGamesResultHistoryUpdate"
			if event_id not in cls.subscriptions:
				subscription_exists = False
				cls.subscriptions[event_id] = []

			cls.subscriptions[event_id].append({
				'func' : func, 
				'query' : query, 
				'variables' : variables, 
				'extensions' : extensions, 
				'operationName' : operationName, 
				'subscription_exists' : subscription_exists,
				'path' : ['payload', 'data', 'resultHistory', '__typename'], 
				'typename' : 'RollGamesResultHistory',
				'type' : 'subscribe'
			})

			@functools.wraps(func)
			async def wrapper(*args, **kwargs):
				return await func(*args, **kwargs)
			return wrapper
		return decorator

	@classmethod
	def chatNewMessageHandler(cls):
		def decorator(func):
			event_id = "a848b99d-3e47-4618-9409-216bdbcd82ac"
			query = socket_queries['OnEventInChatRoom']
			variables = {}
			extensions = {}
			subscription_exists = True
			operationName = "OnEventInChatRoom"
			if event_id not in cls.subscriptions:
				subscription_exists = False
				cls.subscriptions[event_id] = []

			cls.subscriptions[event_id].append({
				'func' : func,
				'query' : query,
				'variables' : variables,
				'extensions' : extensions,
				'operationName' : operationName,
				'subscription_exists' : subscription_exists,
				'path' : ['payload', 'data', 'chat', 'name'],
				'typename' : 'newMessage',
				'type' : 'subscribe'
			})

			@functools.wraps(func)
			async def wrapper(*args, **kwargs):
				return await func(*args, **kwargs)
			return wrapper
		return decorator

	@classmethod
	def onlineChangedHandler(cls):
		def decorator(func):
			event_id = "a848b99d-3e47-4618-9409-216bdbcd82ac"
			query = socket_queries['OnEventInChatRoom']
			variables = {}
			extensions = {}
			subscription_exists = True
			operationName = "OnEventInChatRoom"
			if event_id not in cls.subscriptions:
				subscription_exists = False
				cls.subscriptions[event_id] = []

			cls.subscriptions[event_id].append({
				'func' : func,
				'query' : query,
				'variables' : variables,
				'extensions' : extensions,
				'operationName' : operationName,
				'subscription_exists' : subscription_exists,
				'path' : ['payload', 'data', 'chat', 'name'],
				'typename' : 'onlineChanged',
				'type' : 'subscribe'
			})

			@functools.wraps(func)
			async def wrapper(*args, **kwargs):
				return await func(*args, **kwargs)
			return wrapper
		return decorator


	async def __run_connection(self):
		async with websockets.connect(self.SOCKETS_URI, subprotocols=['graphql-transport-ws'], extra_headers=self.headers) as websocket:
			await websocket.send(json.dumps({"type": "connection_init"}))
			await asyncio.sleep(1)
			for _id in self.subscriptions.keys():
				request_data_list = self.subscriptions[_id]
				for request_data in request_data_list:
					if not request_data['subscription_exists']:
						message = {
							"id" : _id, 
							"payload" : {
								"variables" : request_data['variables'],
								"extensions" : request_data['extensions'],
								"query" : request_data['query'],
								"operationName" : request_data['operationName']
							},
							"type" : request_data['type']
						}

						await websocket.send(json.dumps(message))

			async for message in websocket:
				data = json.loads(message)
				_id = data.get('id')
				subscriptions = self.subscriptions.get(_id)
				typename = data
				if subscriptions:
					for subscription in subscriptions:
						for path in subscription['path']:
							typename = typename[path]
						if typename == subscription['typename']:
							subscription['func'](data['payload']['data'])
						typename = data


	def run(self):
		while True:
			try:
				asyncio.run(self.__run_connection())
			except:
				pass
