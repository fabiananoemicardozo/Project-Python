from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('configuration.DevelopmentConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/products_py"
db = SQLAlchemy(app)

from my_app.product.views import product
app.register_blueprint(product)


with app.app_context():
    db.create_all()
app.run(debug=True)








