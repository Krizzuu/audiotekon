from website import create_app, HOST

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=5000)
