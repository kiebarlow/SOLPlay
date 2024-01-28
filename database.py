import pyrebase
from transactions import transaction

firebaseConfig={
    "apiKey": "AIzaSyD-CptpGm8jx493slHUT98UL-PX7pBxHis",
  "authDomain": "hackathondjproject.firebaseapp.com",
  "databaseURL": "https://hackathondjproject-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "hackathondjproject",
  "storageBucket": "hackathondjproject.appspot.com",
  "messagingSenderId": "931783441197",
  "appId": "1:931783441197:web:cdbec23b901f14d3ee31a4",
  "measurementId": "G-X8KB6Q74HY"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def checkUser(walletId):
    
    global db
    user=db.child("Users").get()
    for u in user.each():
        if u.val()["Wallet"] == walletId:
            return True
    return False
        
    
def createUser(walletId):
    global db
    wall = walletId
    escrow = transaction().newUser()
    pub = str(escrow[0])
    priv = str(escrow[1])
    data={"Wallet":wall,"Escrow":{"PrivateKey":priv,"PublicKey":pub},"Queue":[{"SongName":'NO REQUESTS',"SongArtist":'NO REQUESTS',"SpecialMessage":'NO REQUESTS',"Price":'NO REQUESTS',"PaidFrom":'NO REQUESTS',"State":"NO REQUESTS"}]}
    db.child("Users").push(data)  

def getEscrowPub(walletId):
    global db
    user=db.child("Users").get()
    for u in user.each():
    
        if u.val()["Wallet"]==walletId:
            pub = db.child("Users").child(u.key()).child("Escrow").child("PublicKey").get()
            return pub.val()

def getEscrowPriv(walletId):
    global db
    user=db.child("Users").get()
    for u in user.each():
    
        if u.val()["Wallet"]==walletId:
            priv = db.child("Users").child(u.key()).child("Escrow").child("PrivateKey").get()
            return priv.val()
    
       
def addToQueue(walletId,name,artist,message,price,paidFrom):
    global db
    user=db.child("Users").get()
    for u in user.each():
    
        if u.val()["Wallet"]==walletId:
            req = db.child("Users").child(u.key()).child("Queue").get()
            reqArr = []
            numOfREQ = 0
            Empty = True
            
            for r in req.each():
                reqArr.append(r)
                info = db.child("Users").child(u.key()).child("Queue").child(r.key()).get()
                for i in info.each():   
                    # print(i.val())
                    if i.val() != 'NO REQUESTS':
                        Empty = False
                # print("")
                numOfREQ+=1
                
            if Empty == True:
                db.child("Users").child(u.key()).child("Queue").child(0).set({"SongName":name,"SongArtist":artist,"SpecialMessage":message,"Price":price,"PaidFrom":paidFrom,"State":"Pending","UniqueId":numOfREQ - 1})
            else:
                db.child("Users").child(u.key()).child("Queue").child(numOfREQ).set({"SongName":name,"SongArtist":artist,"SpecialMessage":message,"Price":price,"PaidFrom":paidFrom,"State":"Pending","UniqueId":numOfREQ})


def checkRequests(walletId):
    global db
    user=db.child("Users").get()
    for u in user.each():
    
        if u.val()["Wallet"]==walletId:
            req = db.child("Users").child(u.key()).child("Queue").get()
            reqArr = []
            numOfREQ = 0
            reqList = []
        
        
            for r in req.each():
                reqArr.append(r)
                info = db.child("Users").child(u.key()).child("Queue").child(r.key()).get()
                reqList.append(r.val())
                # for i in info.each():   
                #     print(i.val())
                # print("")
                numOfREQ+=1
            return reqList
        
        
def changeState(walletId,songId,newState):
    global db
    user=db.child("Users").get()
    for u in user.each():
    
        if u.val()["Wallet"]==walletId:
            db.child("Users").child(u.key()).child("Queue").child(songId).child("State").set(newState)