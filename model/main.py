#!/usr/bin/env python
# -*- coding: utf8 -*-
import os.path
import tornado.escape
import tornado.httpserver
import tornado.wsgi
import tornado.ioloop
import tornado.options
import tornado.web
import message
import accessories
import wsgiref.simple_server

class Application(tornado.web.Application):
	def __init__(self):

		handlers = [
			(r"/", MainHandler),
			(r"/accessories", AccesHandler),
			(r"/pictures", PicturesHandler),
			(r"/videos", VideosHandler),
            (r"/build", BuildHandler),
			(r"/contact", ContactHandler),
			(r"/mail", MailHandler),
			(r"/order", OrderHandler),	
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			compress_response=True,
			xheaders=True,
			debug=True,
			autoescape=None
			)
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"welcome.html",
			page = "/welcome",
		)

class AccesHandler(tornado.web.RequestHandler):
	def get(self):

		items=accessories.items
		features=accessories.features
		resumes=accessories.resumes
		pictures=accessories.pictures
		prices=accessories.prices
		references=accessories.references
               
		self.render(
			"accessories.html",
                        items=items,
                        features=features,
                        resumes=resumes,
                        pictures=pictures,
                        prices=prices,
                        references=references
		)

class ContactHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"contact.html",
		)

class BuildHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"build.html",
		)

class PicturesHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"pictures.html",
		)

class VideosHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"videos.html",
		)

class MailHandler(tornado.web.RequestHandler):
	def post(self):
				# Mandrill is a good free SMTP server you must register on www.mandrill.com to get an account and an API KEY
		        serveur = message.ServeurSMTP("smtp.mandrillapp.com", 2525, "account", "API KEY")
		        exped = self.get_argument('prenom') + " "+ self.get_argument('nom')+ " customer mail:"+ self.get_argument('mail')
		        #the email adress which you get customers orders
		        to = ["email@mail.com"]
		        cc = [""]
		        bcc = [""]
		        sujet = self.get_argument('sujet')
		        corps = self.get_argument('message')
		        pjointes=[]
		        codage ='UTF-8'
		        typetexte = 'plain'

		        try:
		        	mess = message.MessageSMTP(exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte)
		        except:
		        	print u"%s" % sys.exc_info()[1]

		        rep = message.envoieSMTP(mess, serveur)

		        self.render(
					"contact.html",
				)

class OrderHandler(tornado.web.RequestHandler):
	def post(self):
 				# Mandrill is a good free SMTP server you must register on www.mandrill.com to get an account and an API KEY
				serveur = message.ServeurSMTP("smtp.mandrillapp.com", 2525, "your account", "API KEY")
				exped = self.get_argument('nom')+ " customer mail: "+ self.get_argument('mail')
				to = ["email@mail.com"]
				cc = [""]
				bcc = [""]
				sujet = "Order"
				corps = "Name : "+self.get_argument('nom')+ "\n"+ "Email : "+self.get_argument('mail')+"\n"+"Tel : " + self.get_argument('tel') +"\n" + self.get_argument('liste_articles')
				pjointes=[]
				codage ='UTF-8'
				typetexte = 'plain'
				try:
					mess = message.MessageSMTP(exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte)
				except:
					print u"%s" % sys.exc_info()[1]

				rep = message.envoieSMTP(mess, serveur)

				self.render(
					"build.html",
				)

def main():
	wsgi_app = tornado.wsgi.WSGIAdapter(Application())
	server = wsgiref.simple_server.make_server('', 8000, wsgi_app)
	server.serve_forever()

if __name__ == "__main__":
	main()
