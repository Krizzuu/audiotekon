from website import create_app
# import pydevd_pycharm
# pydevd_pycharm.settrace('host.docker.internal', port=5678, stdoutToServer=True, stderrToServer=True)


app = create_app()

HOST = '0.0.0.0'

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=5000)
