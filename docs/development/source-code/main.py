# can import anything define in website folder.
from datetime import timedelta
from website import create_app

app = create_app()

if __name__ == '__main__':
    
    #app.run( host='0.0.0.0', port=80 )
    app.run(debug=True)

    # everytime we make a Change to quell code will rerun automaticlly webserver
    # app.permanent_session_lifetime = timedelta(minutes=1)
