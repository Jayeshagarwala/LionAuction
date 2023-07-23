import sqlite3 as sql
import csv
from secureHashing import encode

def createRemovedListings():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS removedListings"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS removedListings(
                            listing_ID TEXT PRIMARY KEY,
                            reason_of_removal TEXT NOT NULL,
                            remaining_bids INTEGER NOT NULL
                            ); """
    cursor.execute(create_query)
    connection.commit()
    connection.close()

def importUsers():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS users"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS users(
                        email TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                        ); """
    cursor.execute(create_query)

    user = open("Datasets/Users.csv")
    data = csv.reader(user)
    next(data)

    insert_query = "INSERT INTO users (email,password) values (?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], encode(row[1])))

    connection.commit()
    connection.close()

def importAddress():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS address"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS address(
                            address_id TEXT PRIMARY KEY,
                            zipcode INTEGER,
                            street_num INTEGER,
                            street_name TEXT,
                            FOREIGN KEY (zipcode) REFERENCES zipcodeInfo
                            ); """
    cursor.execute(create_query)

    address = open("Datasets/Address.csv")
    data = csv.reader(address)
    next(data)

    insert_query = "INSERT INTO address (address_id, zipcode, street_num, street_name) values (?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3]))

    connection.commit()
    connection.close()

def importAuctionListings():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS auctionListings"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS auctionListings(
                                Seller_Email TEXT,
                                Listing_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Category TEXT,
                                Auction_Title TEXT,
                                Product_Name TEXT,
                                Product_Description TEXT,
                                Quantity INTEGER,
                                Reserve_Price TEXT,
                                Max_bids INTEGER,
                                Status INTEGER,
                                UNIQUE (Seller_Email, Listing_ID)
                                ); """
    cursor.execute(create_query)

    listings = open("Datasets/Auction_Listings.csv")
    data = csv.reader(listings)
    next(data)

    insert_query = "INSERT INTO auctionListings (Seller_Email,Listing_ID,Category,Auction_Title,Product_Name,Product_Description,Quantity,Reserve_Price,Max_bids,Status) values (?,?,?,?,?,?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7],row[8],row[9]))

    connection.commit()
    connection.close()

def importBidders():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS bidders"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS bidders(
                                    email TEXT PRIMARY KEY,
                                    first_name TEXT,
                                    last_name TEXT,
                                    gender TEXT,
                                    age INTEGER,
                                    home_address_id TEXT,
                                    major TEXT,
                                    FOREIGN KEY (home_address_id) REFERENCES address,
                                    FOREIGN KEY (email) REFERENCES users
                                    ); """
    cursor.execute(create_query)

    bidders = open("Datasets/Bidders.csv")
    data = csv.reader(bidders)
    next(data)

    insert_query = "INSERT INTO bidders (email,first_name,last_name,gender,age,home_address_id,major) values (?,?,?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    connection.commit()
    connection.close()

def importBids():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS bids"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS bids(
                                        Bid_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Seller_Email TEXT,
                                        Listing_ID INTEGER,
                                        Bidder_Email TEXT,
                                        Bid_Price INTEGER
                                        ); """
    cursor.execute(create_query)

    bids = open("Datasets/Bids.csv")
    data = csv.reader(bids)
    next(data)

    insert_query = "INSERT INTO bids (Bid_ID,Seller_Email,Listing_ID,Bidder_Email,Bid_Price) values (?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4]))

    connection.commit()
    connection.close()

def importCategories():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS categories"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS categories(
                                parent_category TEXT,
                                category_name TEXT PRIMARY KEY
                                ); """
    cursor.execute(create_query)

    categories = open("Datasets/Categories.csv")
    data = csv.reader(categories)
    next(data)

    insert_query = "INSERT INTO categories (parent_category,category_name) values (?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1]))

    connection.commit()
    connection.close()

def importCreditCardInformation():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS creditCardInformation"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS creditCardInformation(
                                        credit_card_num TEXT PRIMARY KEY,
                                        card_type TEXT,
                                        expire_month INTEGER,
                                        expire_year INTEGER,
                                        security_code INTEGER,
                                        Owner_email TEXT,
                                        UNIQUE (credit_card_num, card_type, expire_month, expire_year, security_code)
                                        ); """
    cursor.execute(create_query)

    creditCardInformation = open("Datasets/Credit_Cards.csv")
    data = csv.reader(creditCardInformation)
    next(data)

    insert_query = "INSERT INTO creditCardInformation (credit_card_num,card_type,expire_month,expire_year,security_code,Owner_email) values (?,?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5]))

    connection.commit()
    connection.close()

def importHelpdeskUsers():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS helpdeskUsers"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS helpdeskUsers(
                                    email TEXT PRIMARY KEY,
                                    Position TEXT,
                                    FOREIGN KEY (email) REFERENCES users  
                                    ); """
    cursor.execute(create_query)

    helpdeskUsers = open("Datasets/Helpdesk.csv")
    data = csv.reader(helpdeskUsers)
    next(data)

    insert_query = "INSERT INTO helpdeskUsers (email,Position) values (?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1]))

    connection.commit()
    connection.close()

def importLocalVendors():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS localVendors"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS localVendors(
                                        Email TEXT PRIMARY KEY,
                                        Business_Name TEXT,
                                        Business_Address_ID TEXT,
                                        Customer_Service_Phone_Number TEXT,
                                        FOREIGN KEY (Business_Address_ID) REFERENCES address,
                                        FOREIGN KEY (Email) REFERENCES sellers(email)
                                        ); """
    cursor.execute(create_query)

    localVendors = open("Datasets/Local_Vendors.csv")
    data = csv.reader(localVendors)
    next(data)

    insert_query = "INSERT INTO localVendors (Email,Business_Name,Business_Address_ID,Customer_Service_Phone_Number) values (?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2],row[3]))

    connection.commit()
    connection.close()

def importRatings():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS ratings"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS ratings(
                                            Bidder_Email TEXT,
                                            Seller_Email TEXT,
                                            Date TEXT,
                                            Rating INTEGER,
                                            Rating_Desc TEXT,
                                            PRIMARY KEY (Bidder_Email, Seller_Email,Date)
                                            ); """
    cursor.execute(create_query)

    ratings = open("Datasets/Ratings.csv")
    data = csv.reader(ratings)
    next(data)

    insert_query = "INSERT INTO ratings (Bidder_Email,Seller_Email,Date,Rating,Rating_Desc) values (?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4]))

    connection.commit()
    connection.close()

def importRequests():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS requests"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS requests(
                                                request_id INTEGER PRIMARY KEY,
                                                sender_email TEXT,
                                                helpdesk_staff_email TEXT DEFAULT 'helpdeskteam@lsu.edu',
                                                request_type TEXT,
                                                request_desc TEXT,
                                                request_status INTEGER
                                                ); """
    cursor.execute(create_query)

    requests = open("Datasets/Requests.csv")
    data = csv.reader(requests)
    next(data)

    insert_query = "INSERT INTO requests (request_id,sender_email,helpdesk_staff_email,request_type,request_desc,request_status) values (?,?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5]))

    connection.commit()
    connection.close()

def importSellers():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS sellers"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS sellers(
                                                    email TEXT PRIMARY KEY,
                                                    bank_routing_number TEXT,
                                                    bank_account_number INTEGER,
                                                    balance INTEGER,
                                                    FOREIGN KEY (email) REFERENCES users
                                                    ); """
    cursor.execute(create_query)

    sellers = open("Datasets/Sellers.csv")
    data = csv.reader(sellers)
    next(data)

    insert_query = "INSERT INTO sellers (email,bank_routing_number,bank_account_number,balance) values (?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3]))

    connection.commit()
    connection.close()

def importTransactions():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS transactions"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS transactions(
                                                        Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        Seller_Email TEXT,
                                                        Listing_ID INTEGER,
                                                        Bidder_Email TEST,
                                                        Date TEXT,
                                                        Payment INTEGER,
                                                        FOREIGN KEY(Seller_Email, Listing_ID) REFERENCES auctionListings(Seller_Email, Listing_ID)
                                                        ); """
    cursor.execute(create_query)

    transactions = open("Datasets/Transactions.csv")
    data = csv.reader(transactions)
    next(data)

    insert_query = "INSERT INTO transactions (Transaction_ID,Seller_Email,Listing_ID,Bidder_Email,Date,Payment) values (?,?,?,?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5]))

    connection.commit()
    connection.close()

def importZipcodeInfo():
    connection = sql.connect("LionAuction.db")

    cursor = connection.cursor()

    drop_query = "DROP TABLE IF EXISTS zipcodeInfo"
    cursor.execute(drop_query)

    create_query = """CREATE TABLE IF NOT EXISTS zipcodeInfo(
                                                            zipcode INTEGER PRIMARY KEY,
                                                            city TEXT,
                                                            state TEXT
                                                            ); """
    cursor.execute(create_query)

    zipcodeInfo = open("Datasets/Zipcode_Info.csv")
    data = csv.reader(zipcodeInfo)
    next(data)

    insert_query = "INSERT INTO zipcodeInfo (zipcode,city,state) values (?,?,?)"
    for row in data:
        cursor.execute(insert_query, (row[0], row[1], row[2]))

    connection.commit()
    connection.close()


def main():
    createRemovedListings()
    importAddress()
    importAuctionListings()
    importBidders()
    importBids()
    importCategories()
    importCreditCardInformation()
    importHelpdeskUsers()
    importLocalVendors()
    importRatings()
    importRequests()
    importSellers()
    importTransactions()
    importUsers()
    importZipcodeInfo()


if __name__ == "__main__":
    main()
