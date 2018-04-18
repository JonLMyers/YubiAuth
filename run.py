from app import import create_app

if __name__ == '__main__':
    APP = create_app()
    APP.run(debug=True)
