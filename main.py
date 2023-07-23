from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3 as sql
from urllib.parse import unquote
from datetime import date
from secureHashing import encode

app = Flask(__name__)
app.secret_key = "abcd"

host = 'http://127.0.0.1:5000/'

@app.route("/")
def index():
    return render_template('loginPage.html')


@app.route("/login", methods=['POST', 'GET'])
def loginPage():
    session["username"] = None
    session["currentRole"] = None

    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()

    username = request.form.get('username')
    password = request.form.get('password')
    selectedRole = request.form.get('role')
    if password != None:
        encodedPassword = encode(password)
    fetch_password_query = "SELECT password FROM users WHERE email = ?"
    cursor.execute(fetch_password_query, [username])
    savedPasswords = cursor.fetchall()
    if selectedRole != None and username != None:
        fetch_role_query = f"SELECT COUNT(*) FROM {selectedRole} WHERE email = ?"
        cursor.execute(fetch_role_query, [username])
        accessToRole = cursor.fetchone()

        if savedPasswords is not None and len(savedPasswords) == 1 and encodedPassword == savedPasswords[0][0] and accessToRole[0] == 1:
            session["currentRole"] = selectedRole
            session["username"] = username
            if selectedRole == "bidders":
                return redirect(url_for('homeBidder'))
            elif selectedRole == "sellers":
                return redirect(url_for('homeSeller'))
            elif selectedRole == "helpdeskUsers":
                return redirect(url_for('homeHelpdesk'))

        return render_template('loginPage.html', error=True)
    return render_template('loginPage.html')

    connection.commit()
    connection.close()

@app.route("/homeBidder")
def homeBidder():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    fetch_categories_query = "SELECT * FROM categories"
    cursor.execute(fetch_categories_query)
    categories = cursor.fetchall()
    session['hierarchy'] = createHierarchy("Root", categories)
    fetch_listing_query = "SELECT Seller_Email, Listing_ID, Auction_Title, Product_Name FROM auctionListings WHERE Status = ?"
    cursor.execute(fetch_listing_query, [1])
    listings = cursor.fetchall()
    return render_template('homeBidder.html', listings= listings, data = session['hierarchy'], selectedCategory = "Root")
    connection.commit()
    connection.close()

def createHierarchy(category, categoriesTuple):
    children = getChildren(category, categoriesTuple)

    if not children:
        return {"name": category}
    childListItems = []
    for child in children:
        childListItems.append(createHierarchy(child,categoriesTuple))

    return {"name": category, "children": childListItems}

def getChildren(category,categoriesTuple):
    children = [t[1] for t in categoriesTuple if t[0] == category]
    return children

@app.route("/homeBidder", methods=['POST'])
def homeBidderFilter():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    category = request.form.get('category')
    if category == "Root":
        fetch_listing_query = "SELECT Seller_Email, Listing_ID, Auction_Title, Product_Name FROM auctionListings WHERE Status = ?"
        cursor.execute(fetch_listing_query, [1])
    else:
        fetch_listing_query = "SELECT Seller_Email, Listing_ID, Auction_Title, Product_Name FROM auctionListings WHERE Status = ? AND Category = ?"
        cursor.execute(fetch_listing_query, [1,category])
    listings = cursor.fetchall()
    return render_template('homeBidder.html', listings=listings, data= session['hierarchy'], selectedCategory=category)
    connection.commit()
    connection.close()

@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if  session["currentRole"] == "bidders":
        return redirect(url_for('profileBidder'))

@app.route("/role", methods=['POST', 'GET'])
def changeRole():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    selectedRole = request.form.get('role')
    fetch_role_query = f"SELECT COUNT(*) FROM {selectedRole} WHERE email = ?"

    if session["username"] != None and selectedRole != None:
        cursor.execute(fetch_role_query, [session["username"]])
        accessToRole = cursor.fetchone()
        if accessToRole[0] == 1:
            session["currentRole"] = selectedRole
            if selectedRole == "bidders":
                return redirect(url_for('homeBidder'))
            elif selectedRole == "sellers":
                return redirect(url_for('homeSeller'))
            elif selectedRole == "helpdeskUsers":
                return redirect(url_for('homeHelpdesk'))

        return render_template('changeRole.html', error = True)

    return render_template('changeRole.html')
    connection.commit()
    connection.close()


@app.route("/listing/<id>/<string:seller>", methods=['POST','GET'])
def auctionListing(id,seller):
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    encoded_email = seller
    decoded_email = unquote(encoded_email)

    fetch_listing_query = "SELECT * FROM auctionListings WHERE Seller_Email = ? AND Listing_ID= ?"
    fetch_bid_count_query = "SELECT COUNT(*) FROM bids WHERE Listing_ID= ?"
    fetch_highest_bid_query = "SELECT MAX(Bid_Price), Bidder_Email FROM bids WHERE Listing_ID= ? and Seller_Email = ?"

    cursor.execute(fetch_listing_query, [decoded_email, int(id)])
    listing = cursor.fetchone()

    cursor.execute(fetch_bid_count_query, [int(id)])
    bidCount = cursor.fetchone()

    cursor.execute(fetch_highest_bid_query, [int(id), decoded_email])
    highestBidList = cursor.fetchone()

    if highestBidList[0] == None:
        highestBid = 0
    else:
        highestBid = int(highestBidList[0])

    remainingBid = listing[8] - bidCount[0]

    bidAmount = request.form.get('bidAmount')
    bidPlaced = False
    error= False
    biddingOpen = True
    eligibleToBid = True

    if remainingBid <= 0:
        biddingOpen = False
    canBid = True
    if highestBidList[1] == session['username']:
        canBid = False
    if session['username'] == decoded_email:
        eligibleToBid = False
    if bidAmount != None and int(bidAmount) > 0 and biddingOpen == True and canBid == True and eligibleToBid == True:
        if (int(bidAmount)-int(highestBid)) < 1:
            error = True
        else:
            insert_bid_query = "INSERT INTO bids (Seller_Email,Listing_ID,Bidder_Email,Bid_Price) VALUES (?,?,?,?)"
            cursor.execute(insert_bid_query, [decoded_email,int(id),session['username'],int(bidAmount)])
            cursor.execute(fetch_listing_query, [decoded_email, int(id)])
            listing = cursor.fetchone()
            cursor.execute(fetch_bid_count_query, [int(id)])
            bidCount = cursor.fetchone()
            cursor.execute(fetch_highest_bid_query, [int(id), decoded_email])
            highestBidList = cursor.fetchone()
            highestBid = int(highestBidList[0])
            remainingBid = listing[8] - bidCount[0]
            if remainingBid <= 0:
                if int(bidAmount) >= int(listing[7][1:]):
                    session['sellerEmail'] = decoded_email
                    session['listingID'] = int(id)
                    session['winningBidAmount'] = int(bidAmount)
                    return redirect(url_for('paymentBidder'))

                biddingOpen = False
            connection.commit()
            bidPlaced = True

    return render_template('auctionListing.html', listing=listing, remainingBid=remainingBid, highestBid=highestBid,
                           bidPlaced=bidPlaced, error=error, biddingOpen= biddingOpen, canBid = canBid, eligibleToBid=eligibleToBid)

    connection.close()

@app.route("/payment", methods=['POST','GET'])
def paymentBidder():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    creditCardType = request.form.get("creditCardType")
    creditCardNumber = request.form.get("cardNumber")
    expireMonth = request.form.get("expireMonth")
    expireYear = request.form.get("expireYear")
    securityCode = request.form.get("securityCode")
    saveCreditCard = request.form.get("saveCreditCard")
    submitValue = request.form.get("submit")

    fetch_credit_card_query = "SELECT card_type, credit_card_num, expire_month, expire_year  FROM creditCardInformation WHERE Owner_email = ?"
    cursor.execute(fetch_credit_card_query, [session['username']])
    creditCards = cursor.fetchall()

    if submitValue == "Submit Credit Card Details" and saveCreditCard == "True":
        insert_credit_card_query = "INSERT INTO creditCardInformation (credit_card_num,card_type,expire_month,expire_year,security_code,Owner_email) VALUES (?,?,?,?,?,?)"
        cursor.execute(insert_credit_card_query, [creditCardNumber,creditCardType,int(expireMonth), int(expireYear), int(securityCode), session['username']])
        connection.commit()

    if submitValue != None:
        insert_transaction_query = "INSERT INTO transactions (Seller_Email,Listing_ID,Bidder_Email,Date,Payment) VALUES (?,?,?,?,?)"
        cursor.execute(insert_transaction_query,[session['sellerEmail'],session['listingID'], session['username'], date.today().strftime("%d/%m/%y"), session['winningBidAmount']])
        connection.commit()
        update_listing_query = "UPDATE auctionListings SET Status = 2 WHERE Seller_Email = ? AND Listing_ID = ?"
        cursor.execute(update_listing_query, [session['sellerEmail'], session['listingID']])
        connection.commit()
        return redirect(url_for('homeBidder'))

    return render_template('paymentBidder.html', creditCards = creditCards)
    connection.commit()
    connection.close()

@app.route("/homeSeller", methods=['POST','GET'])
def homeSeller():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()
    fetch_listing_query = "SELECT * FROM auctionListings WHERE Seller_Email = ? and Status = ?"
    cursor.execute(fetch_listing_query, [session['username'], 1])
    activeListing = cursor.fetchall()

    cursor.execute(fetch_listing_query, [session['username'], 0])
    inactiveListing = cursor.fetchall()

    cursor.execute(fetch_listing_query, [session['username'], 2])
    soldListing = cursor.fetchall()

    return render_template('homeSeller.html', activeListing= activeListing, inactiveListing=inactiveListing, soldListing = soldListing)
    connection.commit()
    connection.close()

@app.route("/addListing", methods=['POST','GET'])
def addListing():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()

    auctionTitle = request.form.get("auctionTitle")
    productName = request.form.get("productName")
    productDescription = request.form.get("productDescription")
    quantity = request.form.get("quantity")
    reservePrice = request.form.get("reservePrice")
    maxBids = request.form.get("maxBids")
    selectedCategory = request.form.get("categories")
    submit = request.form.get("submit")

    fetch_categories_query = "SELECT * FROM categories"
    cursor.execute(fetch_categories_query)
    categories = cursor.fetchall()
    categoriesSet = set()
    for category in categories:
        categoriesSet.add(category[0])
        categoriesSet.add(category[1])
    error = False
    fetch_listing_query = "SELECT COUNT(*) FROM auctionListings WHERE Seller_Email = ? and Status = ?"
    cursor.execute(fetch_listing_query, [session['username'], 1])
    listingCount = cursor.fetchone()[0]
    if submit == "Publish Listing":
        if int(listingCount) != 0:
            error = True
        else:
            insert_auction_listing_query = "INSERT INTO auctionListings (Seller_Email,Category,Auction_Title,Product_Name,Product_Description,Quantity,Reserve_Price,Max_bids,Status) VALUES (?,?,?,?,?,?,?,?,?)"
            cursor.execute(insert_auction_listing_query, [session['username'], selectedCategory,auctionTitle,productName,productDescription,quantity,'$'+reservePrice,maxBids,1])
            connection.commit()
            return redirect(url_for('homeSeller'))

    return render_template('addListing.html',categoriesSet=categoriesSet, error=error)
    connection.commit()
    connection.close()

@app.route("/viewListing/<id>/<string:seller>", methods=['POST','GET'])
def viewListing(id,seller):
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()

    auctionTitle = request.form.get("auctionTitle")
    productName = request.form.get("productName")
    productDescription = request.form.get("productDescription")
    quantity = request.form.get("quantity")
    reservePrice = request.form.get("reservePrice")
    maxBids = request.form.get("maxBids")
    selectedCategory = request.form.get("categories")
    submit = request.form.get("submit")
    reasonOfRemoval = request.form.get("reasonOfRemoval")

    encoded_email = seller
    decoded_email = unquote(encoded_email)

    fetch_listing_query = "SELECT * FROM auctionListings WHERE Seller_Email = ? AND Listing_ID= ?"
    cursor.execute(fetch_listing_query, [decoded_email, int(id)])
    listing = cursor.fetchone()
    fetch_bid_count_query = "SELECT COUNT(*) FROM bids WHERE Listing_ID= ?"
    cursor.execute(fetch_bid_count_query, [int(id)])
    bidCount = cursor.fetchone()
    remainingBid = listing[8] - bidCount[0]
    changesMade = False
    listingPublished = False
    listingUnpublished = False

    fetch_categories_query = "SELECT * FROM categories"
    cursor.execute(fetch_categories_query)
    categories = cursor.fetchall()
    categoriesSet = set()
    for category in categories:
        categoriesSet.add(category[0])
        categoriesSet.add(category[1])


    if submit == "Make Changes":
        update_listing_query = "UPDATE auctionListings SET Category = ?,Auction_Title=?,Product_Name=?,Product_Description=?,Quantity=?,Reserve_Price=?,Max_bids=? WHERE Seller_Email = ? AND Listing_ID = ?"
        cursor.execute(update_listing_query, [selectedCategory,auctionTitle,productName,productDescription, quantity, '$'+reservePrice,maxBids,decoded_email,int(id)])
        connection.commit()
        changesMade = True

    if submit == "Unpublish Listing":
        update_listing_query = "UPDATE auctionListings SET Status=0 WHERE Seller_Email = ? AND Listing_ID = ?"
        cursor.execute(update_listing_query,
                       [decoded_email, int(id)])
        connection.commit()
        insert_removed_listing_query = "INSERT INTO removedListings (listing_ID, reason_of_removal, remaining_bids) VALUES (?,?,?)"
        cursor.execute(insert_removed_listing_query,[int(id),reasonOfRemoval, remainingBid])
        connection.commit()
        listingUnpublished=True

    if submit == "Publish Listing":
            update_listing_query = "UPDATE auctionListings SET Category = ?,Auction_Title=?,Product_Name=?,Product_Description=?,Quantity=?,Reserve_Price=?,Max_bids=?, Status = ? WHERE Seller_Email = ? AND Listing_ID = ?"
            cursor.execute(update_listing_query,
                       [selectedCategory, auctionTitle, productName, productDescription, quantity, '$'+reservePrice,
                        maxBids, 1 ,decoded_email, int(id)])
            connection.commit()
            listingPublished = True

    cursor.execute(fetch_listing_query, [decoded_email, int(id)])
    listing = cursor.fetchone()

    connection.commit()
    connection.close()
    return render_template('viewListing.html', listing=listing, changesMade= changesMade, listingPublished= listingPublished, categoriesSet=categoriesSet, listingUnpublished=listingUnpublished)

@app.route("/homeHelpdesk", methods=['POST','GET'])
def homeHelpdesk():
    return render_template('homeHelpdesk.html')

@app.route("/profile/bidder", methods=['POST','GET'])
def profileBidder():
    connection = sql.connect("LionAuction.db")
    cursor = connection.cursor()

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    age = request.form.get("age")
    gender = request.form.get("gender")
    major = request.form.get("major")
    streetNum = request.form.get("streetNum")
    streetName = request.form.get("streetName")
    city = request.form.get("city")
    state = request.form.get("state")
    zip = request.form.get("zipcode")
    submit = request.form.get("submit")

    fetch_user_query = "SELECT * FROM users WHERE email = ?"
    cursor.execute(fetch_user_query, [session['username']])
    user=cursor.fetchone()

    fetch_bidder_query = "SELECT * FROM bidders WHERE email = ?"
    cursor.execute(fetch_bidder_query, [session['username']])
    bidder = cursor.fetchone()

    fetch_address_query = "SELECT * FROM address WHERE address_id = ?"
    cursor.execute(fetch_address_query, [bidder[5]])
    address = cursor.fetchone()

    fetch_zipcode_query = "SELECT * FROM zipcodeinfo WHERE zipcode = ?"
    cursor.execute(fetch_zipcode_query, [address[1]])
    zipcode = cursor.fetchone()

    madeChanges = False

    if submit == "Make Changes":
        madeChanges = True

        update_bidder_query = "UPDATE bidders SET first_name = ?, last_name=?, gender=?, age=?, major=? WHERE email = ?"
        cursor.execute(update_bidder_query, [firstName,lastName,gender,age,major ,session['username']])
        connection.commit()

        cursor.execute(fetch_zipcode_query, [zip])
        zipcodeExists = cursor.fetchone()
        if zipcodeExists == None:
            insert_zipcode_query = "INSERT INTO zipcodeInfo(zipcode,city,state) VALUES(?,?,?)"
            cursor.execute(insert_zipcode_query,[zip,city,state])
            connection.commit()

        update_address_query = "UPDATE address SET zipcode = ?, street_num=?, street_name=? WHERE address_id = ?"
        cursor.execute(update_address_query, [zip, streetNum, streetName, bidder[5]])
        connection.commit()

    cursor.execute(fetch_user_query, [session['username']])
    user = cursor.fetchone()

    cursor.execute(fetch_bidder_query, [session['username']])
    bidder = cursor.fetchone()

    cursor.execute(fetch_address_query, [bidder[5]])
    address = cursor.fetchone()

    cursor.execute(fetch_zipcode_query, [address[1]])
    zipcode = cursor.fetchone()

    return render_template('profileBidder.html', user=user, bidder=bidder, address=address, zipcode= zipcode, madeChanges=madeChanges)



    connection.commit()
    connection.close()


if __name__ == "__main__":
    app.run(debug=True)

