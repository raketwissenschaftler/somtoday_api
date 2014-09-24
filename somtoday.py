import json
import urllib2
import hashlib
import base64
import time


class Somtoday:
    """
    An interface with the somtoday site. Made using the mobile app.
    The schoolName and brin-code can be found on http://servers.somtoday.nl

    Attributes:
     leerlingId(str): The identifier somtoday uses to identify students.

     name(str): The full name of the student, returned by som.

     username(str): The username used to log in.

     schoolName(str): The abbreveation of the school used by somtoday.

     password(str): The password used to log in to somtoday.

     brin(str): The brin-code, a unique code per school.
    """
    leerlingId = None
    name = ""

    def __init__(self, username, password, schoolname, brin):
        """
        Creates a new Somtoday object
        Args:
         username(str): The somtoday username you use logging in.

         password(str): Your somtoday password, also the one you use logging in.

         schoolName(str): The name of your school, as found on http://servers.somtoday.nl.

         brin(str): The brin-code of your school, an unique identifier.

        Raises:
         notActivated: Gets raised if the selected school doesn't support the somtoday app.

         invalidDetails: If the credentials used to login are invalid.

         invalidAccount: If the used account isn't a student account.

         Exception: for all other errors.


        """
        password = hashlib.sha1(password).digest()
        password = self.tohex(base64.encodestring(password))
        username = base64.b64encode(username)
        loginurl = "http://somtoday.nl/" + schoolname + "/services/mobile/v10/Login/CheckMultiLoginB64/" + \
                   username + "/" + password + "/" + brin
        response = self.getJSON(loginurl)

        if response["error"] == "SUCCESS":
            self.leerlingId = str(response["leerlingen"][0]["leerlingId"])
            self.name = response["leerlingen"][0]["fullName"]
            self.username = username
            self.schoolName = schoolname
            self.password = password
            self.brin = brin
            self.baseurl = "https://somtoday.nl/" + schoolname + "/services/mobile/v10/"
        elif response["error"] == "FEATURE_NOT_ACTIVATED":
            raise notActivated("Your school doesn't support the somtoday app, wich was used to create this api.")
        elif response["error"] == "FAILED_AUTHENTICATION":
            raise invalidDetails("Invalid login details")
        elif response["error"] == "FAILED_OTHER_TYPE":
            raise invalidAccount("Your account isn't supported")
        else:
            raise Exception("Unknown error occured")

    def getgrades(self):
        """
        Returns the recent grades from the user.

        Returns:
         A JSON object with the most recent grades, ordered by age.

        """

        gradesurl = self.baseurl + "Cijfers/GetMultiCijfersRecentB64/" + self.username + "/" + self.password + "/" + \
                    self.brin + "/" + self.leerlingId
        gradesJSON = self.getJSON(gradesurl)["data"]
        return gradesJSON

    def gethomework(self, daysahead=14):
        """
        Returns all homework for the amount of days specified in daysAhead

        Parameters:
         daysahead(int): the amount of days ahead the homework has to be displayed.

        Returns:
         A JSON object with all homework until the amount of days ahead.
        """

        huiswerkurl = self.baseurl + "Agenda/GetMultiStudentAgendaHuiswerkMetMaxB64/" + self.username + "/" + \
                      self.password + "/" + self.brin + "/" + str(daysahead) + "/" + self.leerlingId
        homeworkJSON = self.getJSON(huiswerkurl)["data"]
        return homeworkJSON

    def getschedule(self, daysahead=0):
        """
        Returns all classes for the current day, or a specified amount of days ahead.

        Parameters:
         daysahead(float): a number that indicates the amount of days ahead it has to fetch the schedule for. Default=0

        Returns:
         A JSON object with the schedule for the current day in it.
         This JSON object contains an array of dictionaries, that contain the following elements:
          huiswerk:The homework for that class, markup done with html.
          vak: The subject. Format depends on the format your school uses.
          begin: The timestamp when this subject starts.(Milliseconds since epoch)
          titel: The name given on the app, bascially a short summary of the period.
          afspraakid: I don't know this one yet, if anyone figures something out: let me hear.
          af: False if there wasn't any homework or if you didn't finish it, true if you finished it.
          docenten: I guess it should indicate the teacher(s) you have that period, but for me it says none. Testing needed.
          onderwijsproduct: I don't have a clue. My school doesn't use this.
          huiswerkid: Should contain the homework for that hour. Doesn't work that well(in my case at least)
          eind: The timestamp when this period ends(milliseconds since epoch)
          type: The type of appointment. Most cases this will be ROOSTER.
          lesuur: The period of this class. Should be parsed to int if used as a number.
          locatie: The classroom/place in general where this appointment is.
          afkorting: No idea. Needs testing.
          omschrijving: Not indicated most of the time, but i guess it is for additional remarks.
        """
        date = int(time.time() + (daysahead * 86400)) * 1000
        roosterUrl = self.baseurl + "Agenda/GetMultiStudentAgendaB64/" + self.username + "/" + self.password + "/" + \
                     self.brin + "/" + str(date) + "/" + self.leerlingId
        scheduleJSON = self.getJSON(roosterUrl)["data"]
        return scheduleJSON

    def tohex(self, convertString):
        """
        An obscure function topicus forced me to use. It works.

        """
        output = ""
        hexChars = "0123456789abcdef"
        symbols = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        for char in convertString:
            asciiValue = ord(char)
            index1 = asciiValue % 16
            index2 = (asciiValue - index1) / 16
            output += hexChars[index2]
            output += hexChars[index1]
        return output[:-2]

    @staticmethod
    def getJSON(url):
        try:
            response = json.loads(urllib2.urlopen(url).read())
        except ValueError:
            raise invalidResponse("Could not parse this response")
        except urllib2.HTTPError:
            raise invalidResponse("Page not found.")
        return response


class notActivated(Exception):
    pass


class invalidDetails(Exception):
    pass


class invalidAccount(Exception):
    pass


class invalidResponse(Exception):
    pass

