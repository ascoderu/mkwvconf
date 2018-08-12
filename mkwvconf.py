#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

try:
    raw_input
except NameError:
    raw_input = input

try:
    from string import atoi
except ImportError:
    atoi = int


class Mkwvconf:

    #########
    # file paths
    #########

    xmlPath = '/usr/share/mobile-broadband-provider-info/serviceproviders.xml'
    configPath = '/etc/wvdial.conf'

    #########
    # class members
    #########

    introMessage = """
mkwvconf automatically generates a dialer section for use in wvdial.conf based on mobile-broadband-provider-info.

If a provider is missing from the list, add a bug at http://bugzilla.gnome.org/enter_bug.cgi?product=NetworkManager (include your provider name, your country, your plans marketing name if you know it, and of course the APN you're using for data). For more information about the mobile broadband provider database, see http://blogs.gnome.org/dcbw/2009/06/22/mobile-broadband-assistant-makes-it-easy/ .

The configuration generated by mkwvconf overwrites CID 1 with your provider info ('Init2=AT+CGDCONT=1,...') which is then called by dialing *99***1# (the digit before the trailing '#' specifies which CID to use).

Further reading on APNs can be found here: http://mail.gnome.org/archives/networkmanager-list/2008-August/msg00191.html. Thanks goes to Antti Kaijanmäki for explanations and links!"""

    #########
    # class methods
    #########

    def __init__(self):
        self.doc = ET.parse(self.xmlPath)

    def displayIntro(self):
        os.system('clear')
        print(self.introMessage)

    def getCountryCodes(self):
        """returns a list of all country codes"""
        return [str(n.get('code')) for n in self.getNodesFromXml("country[@code]")]

    def selectCountryCode(self):
        """lets user choose a country code and returns the chosen value"""

        countryCodes = self.getCountryCodes()

        print("\nAvailable country codes:\n")
        print(countryCodes)

        country = ""

        while country not in countryCodes:
            country = raw_input("\nGet providers for which country code? : ")

        return country

    def getNodesFromXml(self, xquery):
        """returns results of xquery as a list"""
        return self.doc.findall(xquery)

    def getProviders(self, countryCode):
        """returns list of providers for countryCode"""
        nodes = self.getNodesFromXml('country[@code=\'' + countryCode + '\']/provider/name')
        return [n.text for n in nodes]

    def selectProvider(self, countryCode):
        """lets user choose a provider and returns the chosen provider name"""
        providers = self.getProviders(countryCode)

        index = self.getUserChoice(providers, "Providers for '" + countryCode + "':", "Choose a provider")
        return providers[index]

    def selectApn(self, node):
        """takes a provider node, lets user select one apn (if several exist) and returns the chosen node"""
        apns = node.findall("*/apn")
        apnnames = [n.get("value") for n in apns]

        apncount = len(apns)
        if apncount == 1:
            return apns[0]

        index = self.getUserChoice(apnnames, "Available APNs:", "Choose an APN")
        return apns[index]

    def makeConfig(self, countryCode, provider):
        """get final information from user and assembles configuration section. the configuration is either written to wvdial.conf or printed for manual insertion"""
        providerNode = self.getNodesFromXml("country[@code='" + countryCode + "']/provider[name='" + provider + "']")[0]
        apnNode = self.selectApn(providerNode)

        parameters = self.parseProviderNode(apnNode)
        parameters["modem"] = self.getModemDevice()
        parameters["profileName"] = self.getUserInput("Enter name for configuration: ", "DefaultProfile")

        editConf = raw_input("\nDo you want me to try to modify " + self.configPath + " (you will need superuser rights)? Y/n: ")
        os.system('clear')
        if editConf in ["", "Y", "y"]:
            self.writeConfig(parameters)
        else:
            print("\n\nDone. Insert the following into " + self.configPath + " and run 'wvdial " + parameters["profileName"] + "' to start the connection.\n\n")
            print(self.formatConfig(parameters))

    def writeConfig(self, parameters):
        """append or replace the configuration section to wvdial.conf"""
        if not os.path.exists(self.configPath):
            print("\nWarning: " + self.configPath + " doesn't exist, creating new file.")
            f = open(self.configPath, 'w')
            f.close()

        f = open(self.configPath, 'r')
        text = f.read()
        f.close()

        section = self.formatConfig(parameters)

        snippetStart = text.find("[Dialer %(profileName)s]" % parameters)
        if snippetStart != -1:
            snippetEnd = text.find("[Dialer ", snippetStart + 1)
            print("\nThe following part of wvdial.conf will be replaced: \n\n" + text[snippetStart:snippetEnd])
            print("by: \n\n" + section)
            text = text.replace(text[snippetStart:snippetEnd], section)
        else:
            print("\nThe following will be appended to wvdial.conf: \n\n" + section)
            text += "\n" + section

        editConf = raw_input("Write to file? Y/n: ")
        if editConf in ["", "Y", "y"]:
            f = open(self.configPath, 'w')
            f.write(text)
            f.close()

            print("wvdial.conf edited successfully, run 'wvdial " + parameters["profileName"] + "' to start the connection.\n\n")

    def formatConfig(self, parameters):
        """formats the information contained in parameters into a valid wvdial.conf format"""

        if 'usr' not in parameters:
            parameters['usr'] = ""

        if 'pw' not in parameters:
            parameters['pw'] = ""

        return """[Dialer %(profileName)s]
Modem Type = Analog Modem
Phone = *99***1#
ISDN = 0
Baud = 460800
Username = %(usr)s
Password = %(pw)s
Modem = %(modem)s
Init1 = ATZ
Init2 = at+cgdcont=1,"ip","%(apn)s"
Stupid Mode = 1
""" % parameters

    def getModemDevice(self):
        """return modem location provided by user"""
        defaultLocation = "/dev/ttyUSB0"
        modemDevice = "initialValue"

        while not modemDevice.startswith("/dev/") or len(modemDevice) == 0:
            modemDevice = self.getUserInput("Enter modem location (default is /dev/ttyUSB0): ", defaultLocation)

        if len(modemDevice.strip()) == 0:
            modemDevice = defaultLocation

        return modemDevice

    def getUserChoice(self, l, header, prompt):
        """takes a string list, a text prompt and a header, and returns user choice"""

        print('')
        print(header)
        print('')

        count = len(l)
        for k, v in zip(range(count), l):
            print(str(k) + ": " + v)

        choice = -1
        while choice >= count or choice < 0:
            inputStr = self.getUserInput(prompt + " [0-" + str(count - 1) + "]:")
            try:
                choice = atoi(inputStr)
                if choice < 0 or choice >= count:
                    print("Input needs to be between 0 and " + str(count - 1))
            except ValueError:
                choice = -1
                print("Input needs to be an integer.")

        return int(choice)

    def getUserInput(self, prompt, default=""):
        """utility method for getting user input. displays prompt, optional default fallback"""
        accept = "n"
        inp = ""
        while accept == "n" or accept == "N":
            inp = raw_input("\n" + prompt)
            if len(inp.strip()) == 0:
                inp = default
            accept = raw_input("Your choice: '" + inp + "'. Is this correct? Y/n: ")
        return inp

    def parseProviderNode(self, apnNode):
        """return initially filled parameter dictionary from provider xml node"""
        parameters = {}

        apn = apnNode.get("value")
        parameters["apn"] = apn

        usr = apnNode.findtext("username")
        if usr:
            parameters["usr"] = usr

        pw = apnNode.findtext("password")
        if pw:
            parameters["pw"] = pw

        return parameters


if __name__ == "__main__":

    mkwvconf = Mkwvconf()

    mkwvconf.displayIntro()
    countryCode = mkwvconf.selectCountryCode()
    provider = mkwvconf.selectProvider(countryCode)
    mkwvconf.makeConfig(countryCode, provider)
