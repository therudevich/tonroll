import requests
from .queries import queries

class TonRoll:
	API_URL = "https://tonroll.com/api"
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

	def __init__(self, token: str | None = None):
		self.headers = {
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

	def getWalletTransactionList(self):
		self.operationName = "GetWalletTransactionList"
		return self.__send_request()

	def getRollGame(self):
		self.operationName = "getRollGame"
		return self.__send_request()

	def placeRollGameBet(self, amount: int | float, choice: str, currency: str):
		self.operationName = "placeRollGameBet"
		return self.__send_request({'amount': amount, 'choice': choice, 'currency': currency})

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



