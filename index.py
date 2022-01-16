import tornado.web 
import tornado.ioloop

class BasicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

class StaticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class QueryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"
        self.write("the number " + str(n) + " is " + r)

class ResourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("Querying")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", BasicRequestHandler),
        (r"/blog", StaticRequestHandler),
        (r"/", QueryStringRequestHandler),
        (r"/tweet/([0-9]+)", ResourceRequestHandler)
    ])

    app.listen(8080)
    print("I'm listening port 8080")
    tornado.ioloop.IOLoop.current().start()