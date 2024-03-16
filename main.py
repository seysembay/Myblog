from flask import Flask

# engine = create_engine('postgresql://user:password@172.18.0.2:5432/myblog', echo=True)
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
