from website import create_app


app = create_app()

HOST = '0.0.0.0'

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=5000)
