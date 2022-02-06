from flask import Flask

from views import index_bp


app = Flask(__name__, template_folder="templates")
app.register_blueprint(index_bp)


def main():
    app.run()


if __name__ == "__main__":
    main()
