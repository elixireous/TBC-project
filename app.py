from ext import app
from routes import index, shop, login, register, about, add_tea, tea_details, contact

if __name__ == "__main__":
    app.run(debug=True)
