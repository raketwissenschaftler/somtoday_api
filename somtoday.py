import json
import urllib2
import hashlib
import base64
class Somtoday:
	"""
	An interface with the somtoday site. Made using the mobile app.
	The schoolname and brin-code can be found on http://servers.somtoday.nl

	"""
	leerlingId=None
	name=""

	def __init__(self, username, password, schoolname, brin):
		"""
		

		"""
		password=hashlib.sha1(password).digest()
		password=self.toHex(base64.encodestring(password))
		username=base64.b64encode(username)
		loginUrl="http://somtoday.nl/"+schoolname+"/services/mobile/v10/Login/CheckMultiLoginB64/"+username+"/"+password+"/"+brin
		try:
			response=json.loads(urllib2.urlopen(loginUrl).read())
		except ValueError:
			raise Exception("School not found")

		if response["error"]=="SUCCESS":
			self.leerlingId=response["leerlingen"][0]["leerlingId"]
			self.name=response["leerlingen"][0]["fullName"]
		elif response["error"]=="FEATURE_NOT_ACTIVATED":
			raise notActivated("Your school doesn't support the somtoday app, wich was used to create this api.")
		elif response["error"]=="FAILED_AUTHENTICATION":
			raise invalidDetails("Invalid login details")
		elif response["error"]=="FAILED_OTHER_TYPE":
			raise invalidAccount("Your account isn't supported")
		else:
			raise Exception("Unknown error occured")


	def toHex(self,convertString):
		output=""
		hexChars="0123456789abcdef"
		symbols=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
		for char in convertString:
			asciiValue=ord(char)
			index1=asciiValue % 16
			index2=(asciiValue-index1)/16
			output+=hexChars[index2]
			output+=hexChars[index1]
		return output[:-2]

	def getName(self):
		return self.name

class notActivated(Exception):
	pass

class invalidDetails(Exception):
	pass
class invalidAccount(Exception):
	pass

