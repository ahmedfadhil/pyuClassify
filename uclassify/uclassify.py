#!/usr/bin/python

from xml.dom.minidom import Document
from time import gmtime, strftime
from uclassify_eh import uClassifyError
import xml.dom.minidom
import requests
import base64

class uclassify:
    def __init__(self):
        self.api_url = "http://api.uclassify.com"
        self.writeApiKey=None
        self.readApiKey=None

    def setWriteApiKey(self,key):
        self.writeApiKey = key

    def setReadApiKey(self,key):
        self.readApiKey = key

    def _buildbasicXMLdoc(self):
        doc = Document()
        root_element = doc.createElementNS('http://api.uclassify.com/1/RequestSchema', 'uclassify')
        root_element.setAttribute("version", "1.01")
        root_element.setAttribute("xmlns", "http://api.uclassify.com/1/RequestSchema")
        doc.appendChild(root_element)
        #texts = doc.createElement("texts")
        #root_element.appendChild(texts)
        #print(doc.toprettyxml())
        return doc,root_element

    def _getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def _getResponseCode(self,content):
        """Returns the status code from the content.
           :param content: (required) XML Response content
        """
        doc = xml.dom.minidom.parseString(content)
        node = doc.documentElement
        status = node.getElementsByTagName("status")
        success = status[0].getAttribute("success")
        status_code = status[0].getAttribute("statusCode")
        text = self._getText(status[0].childNodes)
        return success, status_code, text

    def create(self,classifierName):
        """Creates a new classifier.
           :param classifierName: (required) The Classifier Name you are going to create.
        """
        doc,root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("writeApiKey",self.writeApiKey) #Add exception handling here
        writecalls.setAttribute("classifierName",classifierName)
        create = doc.createElement("create")
        cur_time = strftime("%Y%m%d%H%M", gmtime())
        create.setAttribute("id",cur_time + "create" + classifierName)
        root_element.appendChild(writecalls)
        writecalls.appendChild(create)
        r = requests.post(self.api_url,doc.toxml())
        if r.status_code == 200:
            success, status_code, text = self._getResponseCode(r.content)
            if success == "false":
                raise uClassifyError(text,status_code)
        else:
            raise uClassifyError("Bad XML Request Sent")

    def addClass(self,className,classifierName):
        """Adds class to an existing Classifier.
           :param className: (required) A List containing various classes that has to be added for the given Classifier.
           :param classifierName: (required) Classifier where the classes will be added to.
        """
        doc, root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        if self.writeApiKey == None:
            raise uClassifyError("Write API Key not Initialized")
        writecalls.setAttribute("writeApiKey",self.writeApiKey)
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(writecalls)
        for clas in className:
            addclass = doc.createElement("addClass")
            addclass.setAttribute("id","AddClass" + clas)
            addclass.setAttribute("className",clas)
            writecalls.appendChild(addclass)
        r = requests.post(self.api_url,doc.toxml())
        if r.status_code == 200:
            success, status_code, text = self._getResponseCode(r.content)
            if success == "false":
                raise uClassifyError(text,status_code)
        else:
            raise uClassifyError("Bad XML Request Sent")
     
    def train(self,texts,className,classifierName):
        """Performs training on a single classs.
           :param texts: (required) A List of text used up for training.
           :param className: (required) Name of the class that needs to be trained.
           :param classifierName: (required) Name of the Classifier
        """
        base64texts = []
        for text in texts:
            base64_text = base64.b64encode(text) #For Python version 3, need to change.
            base64texts.append(base64_text)
        doc,root_element = self._buildbasicXMLdoc()
        textstag = doc.createElement("texts")
        writecalls = doc.createElement("writeCalls")
        if self.writeApiKey == None:
            raise uClassifyError("Write API Key not Initialized")
        writecalls.setAttribute("writeApiKey",self.writeApiKey)
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(textstag)
        root_element.appendChild(writecalls)
        counter = 1
        for text in base64texts:
            textbase64 = doc.createElement("textBase64")
            traintag = doc.createElement("train")
            textbase64.setAttribute("id",className + "Text" + str(counter))
            ptext = doc.createTextNode(text)
            textbase64.appendChild(ptext)
            textstag.appendChild(textbase64)
            traintag.setAttribute("id","Train"+className+ str(counter))
            traintag.setAttribute("className",className)
            traintag.setAttribute("textId",className + "Text" + str(counter))
            counter = counter + 1
            writecalls.appendChild(traintag)
        r = requests.post(self.api_url,doc.toxml())
        if r.status_code == 200:
            success, status_code, text = self._getResponseCode(r.content)
            if success == "false":
                raise uClassifyError(text,status_code)
        else:
            raise uClassifyError("Bad XML Request Sent")
            
if __name__ == "__main__":
    a = uclassify()
    a.setWriteApiKey("fsqAft7Hs29BgAc1AWeCIWdGnY")
    #a.create("ManorWoma")
    #a.addClass(["man","woman"],"ManorWoma")
    a.train(["dffddddddteddddxt1","teddddxfddddddddt2","taaaaffaaaaaedddddddddddddxt3"],"woman","ManorWoma")
