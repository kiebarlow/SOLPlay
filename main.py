from flask import Flask, render_template, request, session, redirect
import jsonify
from flask_cors import CORS
import json
from transactions import transaction
from database import checkRequests, addToQueue, checkUser, createUser, getEscrowPub, changeState, getEscrowPriv


app = Flask(__name__)
CORS(app)

app.secret_key = 'imsupersecretbigchunguscodeyeahyeahthatsme'

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        # You can use user_id to fetch user-specific data from the database or perform other actions
        print(f"User ID from session: {user_id}")
        print(checkRequests(user_id))
        return render_template('dashboard.html', songs=checkRequests(user_id), userId=user_id)
    else:
        return render_template('login.html')

@app.route('/payforsong/<userid>')
def payforsong(userid):
    djEscrow = getEscrowPub(userid)
    print("djescrow is:", djEscrow)
    return render_template('payforsong.html', userid=userid, djEscrow=djEscrow)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/clear_session')
def clear_session():
    session.clear()
    return 'Session cleared'


@app.route('/qrCode')
def qrCode():
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template('qrcode.html', userId=user_id)
    else:
        return render_template('login.html')

@app.route('/api/login', methods=['POST', 'GET'])
def apiLogin():
    if request.method == "POST":
        # Retrieve the data that was submitted in the POST request and assign it to the corresponding values.
        req = request.get_json()
        print(req)
        try:
            if 'wallet' in req:
                wallet_address = req['wallet']
                if checkUser(wallet_address) == False:
                    createUser(wallet_address)
                session['user_id'] = str(wallet_address)
                print(session)
                return "done"
        except:
            return 'Method Not Allowed', 405
        

@app.route('/api/grabFormData', methods=['POST', 'GET'])
def grabformdata():
    if request.method == "POST":
        req = request.get_json()
        songName = req['songName']
        artist = req['artist']
        description = req['description']
        price = req['price']
        walletThatPayed = req['wallet']
        djuserId = req['djid']
        print(djuserId,songName,artist,description,price,walletThatPayed)
        addToQueue(djuserId,songName,artist,description,price,walletThatPayed)
        return "done"
        
@app.route('/api/genEscrow')
def genEscrow():
    return str(transaction().newUser());

@app.route('/api/changeSongState', methods=['POST', 'GET'])
def changeSongState():
    if request.method == "POST":
        req = request.get_json()
        userId = req['userId']
        uniqueSongId = req['uniqueSongId']
        newState = req['newState']
        songPrice = req['songPrice']
        songPaidfrom = req['songPaidFrom']
        print(newState, " <--- new state")

        if newState == "Accepted":
            print(transaction().songAccepted(getEscrowPub(userId), getEscrowPriv(userId), float(songPrice), userId))
        elif newState == "Declined":
            print(transaction().songDeclined(songPaidfrom, getEscrowPriv(userId), getEscrowPub(userId), float(songPrice)))

        

        print("______________")
        print(userId, newState, uniqueSongId)
        changeState(userId, uniqueSongId, newState)

        print("done")
    return "fdone"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)