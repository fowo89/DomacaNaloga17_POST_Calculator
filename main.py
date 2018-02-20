#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class CalculateHandler(BaseHandler):
    def post(self):
        if self.request.get("operation") == "+":
            result = float(self.request.get("1st_number")) + float(self.request.get("2nd_number"))
        elif self.request.get("operation") == "-":
            result = float(self.request.get("1st_number")) - float(self.request.get("2nd_number"))
        elif self.request.get("operation") == "*":
            result = float(self.request.get("1st_number")) * float(self.request.get("2nd_number"))
        elif self.request.get("operation") == "/":
            result = float(self.request.get("1st_number")) / float(self.request.get("2nd_number"))
        else:
            return self.render_template("Error.html")



        podatki={"1st_number": self.request.get("1st_number"),
                 "2nd_number": self.request.get("2nd_number"),
                 "result": result}
        return self.render_template("Result.html", podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/calculate', CalculateHandler),
], debug=True)
