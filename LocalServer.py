from flask import Flask, render_template, make_response, request
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
import configparser
from LinkedIn import LinkedInBot
import os
import imutils
from PIL import Image
import io

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb+srv://singhask:freMjpfBaWN3okw5@cluster0.j2f5i9l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)


class DataForm (Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('mainpage.html'), headers)


class CreatePost (Resource):

    def post(self):

        image_data = request.files.getlist("imagepath")
        text_post = request.form.get("posttext")
        post_title = request.form.get("title")
        github_link = request.form.get("github")
        save_data = request.form.get("upload")
        post_online = request.form.get("make_post")
        imagepaths = [os.path.abspath(image.filename) for image in image_data]

        if post_online == "Yes":
            config = configparser.ConfigParser()
            config.read('./config.ini')

            username = config["CREDS"]["USERNAME"]
            password = config["CREDS"]["PASSWORD"]
            bot = LinkedInBot(username, password)
            bot.login()

            if image_data[0].filename == '':
                bot.post_text(text_post, github_link)

            else:
                bot.post_with_image(text_post, github_link, imagepaths)

        if save_data == "Yes":
            imagenames = []
            for image in image_data:
                mongo.save_file(image.filename, image)
                imagenames.append(image.filename)

            post_data = {
                "text": text_post,
                "title": post_title,
                "images": imagenames,
                "Github": github_link
            }

            mongo.db.Projects.insert_one(post_data)

        return "Done!"


class Update_Database(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('update.html'), headers)

    def post(self):
        image_data = request.files.getlist("imagepath")
        text_post = request.form.get("posttext")
        post_title = request.form.get("title")
        github_link = request.form.get("github")
        linkedin_link = request.form.get("linkedin")

        if image_data[0].filename != "":
            for image in image_data:
                mongo.save_file(image.filename, image)

        if text_post != "":
            mongo.db.Projects.find_one_and_update(
                {"title": post_title}, {"$set": {"text": text_post}})

        if github_link != "":
            mongo.db.Projects.find_one_and_update(
                {"title": post_title}, {"$set": {"Github": github_link}})

        if linkedin_link != "":
            mongo.db.Projects.find_one_and_update(
                {"title": post_title}, {"$set": {"LinkedIn": linkedin_link}})

        return 200


api.add_resource(DataForm, "/")
api.add_resource(CreatePost, "/create")
api.add_resource(Update_Database, "/update")


if __name__ == "__main__":
    app.run(debug=True)
