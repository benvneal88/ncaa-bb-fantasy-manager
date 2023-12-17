from api.__init__ import create_app
from api import model

if __name__ == '__main__':
    model.init_database()
    app = create_app()
    app.run(debug=False)
