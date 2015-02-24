#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
import os
#if you use an SMTP with SSL encryption : from smtplib import SMTP_SSL
from smtplib import SMTP
from email import Encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
 
##############################################################################
class ServeurSMTP(object):
    def __init__(self, adresse="", port=25, login="", mdpasse=""):
        """keep parameters of an email account on a SMTP server"""
        self.adresse = adresse
        self.port = port
        self.login = login
        self.mdpasse = mdpasse
 
##############################################################################
class MessageSMTP(object):
 
    def __init__(self, exped="", to=[], cc=[], bcc=[], sujet="", corps="", pjointes=[], codage='UTF-8', typetexte='plain'):
        """maje a detailed email"""
 
        # prepare data
        self.expediteur = exped
        if type(pjointes)==str or type(pjointes)==unicode:
            pjointes = pjointes.split(';')
        if codage==None or codage=="":
            codage = 'UTF-8'
        if to==[] or to==['']:
            self.destinataires = []
            self.mail = ""
            raise ValueError ("error: no receiver")
 
        # build the mail
 
        if pjointes==[]:
            # message without attachment
            msg = MIMEText(corps.encode(codage), typetexte, _charset=codage)
        else:
            # "multipart" message with one or several attachment
            msg = MIMEMultipart('alternatives')
 
        msg['From'] = exped
        msg['To'] = ', '.join(to)
        msg['Cc'] = ', '.join(cc)
        msg['Bcc'] = ', '.join(bcc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = sujet.encode(codage)
        msg['Charset'] = codage
        msg['Content-Type'] = 'text/' + typetexte + '; charset=' + codage
 
        if pjointes!=[]:
            msg.attach(MIMEText(corps.encode(codage), typetexte, _charset=codage))
 
            # add attachment
            for fichier in pjointes:
                part = MIMEBase('application', "octet-stream")
                try:
                    f = open(fichier,"rb")
                    part.set_payload(f.read())
                    f.close()
                except:
                    coderr = "%s" % sys.exc_info()[1]
                    raise ValueError ("attachment error (" + coderr + ")")
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename="%s" % os.path.basename(fichier))
                msg.attach(part)
 
        # final package of the message
        self.mail = msg.as_string()
 
        # build the complete list of reveivers
        self.destinataires = to
        self.destinataires.extend(cc)
        self.destinataires.extend(bcc)
 
##############################################################################
def envoieSMTP(message, serveur):
    """send the message at the SMTP server"""
    try:
        # if you use a SSL encrypted SSL Server replace by smtp = SMTP_SSL(serveur.adresse, serveur.port)
        smtp = SMTP(serveur.adresse, serveur.port)
    except:
        coderr = "%s" % sys.exc_info()[1]
        return u"connection error (" + coderr + ")"
 
    # smtp.set_debuglevel(1)  # uncomment to show protocol exchanges
    if serveur.login != "":
        try:
            smtp.login(serveur.login, serveur.mdpasse)
        except:
            coderr = "%s" % sys.exc_info()[1]
            smtp.quit()
            return u"error: bad login/password (" + coderr + ")"
    try:
        rep = smtp.sendmail(message.expediteur, message.destinataires, message.mail)
    except:
        coderr = "%s" % sys.exc_info()[1]
        smtp.quit()
        return u"sending mail error (" + coderr + ")"
    smtp.quit()
    return rep

if __name__ == "__main__":
    # Add your smtp server adress
    # if you have no identification not use 2 last parameters
    # the default port is 25
    serveur = ServeurSMTP("smtp.mandrillapp.com", 2525, "account", "API KEY")
     
    # sender email
    exped = "firstname lastname <mail>"
     
    # recipient adress
    to = ["dest"]
     
    # recipient copy adress
    cc = [""]
     
    # recipient hidden copy adress
    bcc = [""]
     
    # mail subject
    sujet = "Hi Albert!"
     
    # mail corps
    corps = unicode("""
    Hi Albert!
     
    I hope you are good !     
    See you soon !
    
    Bye.

    thibaud
    """, "utf-8")
     
    # attachment here
    pjointes=[]
     
    # choose your encodage: 'US-ASCII', 'ISO-8859-1', 'ISO-8859-15', 'UTF-8', None (None=default encodage)
    # recall: ISO-8859-15 allows at additional to l'ISO-8859-1, using the euro acronym (€)
    codage ='UTF-8'
    # text type : 'plain', 'html', ... here, it's 'plain'
    typetexte = 'plain'
     
    # create the mail
    try:
        message = MessageSMTP(exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte)
    except:
        print u"%s" % sys.exc_info()[1]
        sys.exit()
     
    # send the mail and show the result
    rep = envoieSMTP(message, serveur)
