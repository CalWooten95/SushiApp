from flask import Flask, render_template, request
server_app = Flask(__name__)

@server_app.route('/')
def server_main_page():
   return render_template('server/server.html')

if __name__ == '__main__':
   server_app.run()