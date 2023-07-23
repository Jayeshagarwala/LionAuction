# LionAuction
This project implements a web-based auction system using Flask, HTML, Jinja, and SQLite. The system is designed to allow users to log in, browse auction listings by category, publish and manage auctions as sellers, and bid on auctions as bidders.

## Technologies Used

The LionAuction system was built using the following technologies:

- Flask
- HTML
- Jinja
- SQLite
## Features

The LionAuction system has the following features:

### User LogIn
This feature allows users (sellers, bidders, or helpdesk staff) to log in to the system using their email and password. The system recognizes the user by their email and password, and the user's password is hashed when stored in the system. Users may have multiple roles (i.e., seller, bidder, or helpdesk staff) and can switch roles after login. Upon logging in, users are directed to a welcome page where they can perform allowable operations based on their role. Personal information of the user (e.g., name, email ID, age, gender, major, billing address, etc.) can be displayed/checked based on the user's role. The welcome page provides entry points for other operations, e.g., browsing categories, checking the status of auctions, and so on.

### Category Browsing
This feature allows users to browse auctions by category. Auction listings available in LionAuction are categorized based on a predefined category hierarchy in the categories table. Users can traverse the category hierarchy by clicking on a subcategory to see the product items under that specific category. The system dynamically queries the database to find the next-level subcategories for display. When a user clicks on an auction listing, the auction details (e.g., title, product information, seller information, quantity, remaining number of bids, etc.) are displayed, along with a button to facilitate bidding.

### AuctionBidding
This feature allows bidders to place bids on auctions. Bids must be at least $1 higher than all previous bids

### Auction Listing
This feature allows sellers to publish/take off an auction listing in LionAuction. Before publishing a listing, sellers must enter detailed information about the auction (e.g., title, product details, category, etc.). The published auction listing is immediately available for display in its category when users browse the category hierarchy. Sellers can also make changes to active or inactive auction listings, and take a published auction listing off the market. Useful information about the auction listing, including the remaining number of bids and reasons for taking it off the market, is maintained. The auction listings of a seller are properly grouped (as active, inactive, and sold) and displayed to the seller for further actions.

### User Profile
View and Change user profile information. 

Important Files: 

1. main.py: Main function file for LionAuction. Run this file to run the LionAuction Website. 
2. resetDB.py: Resets all the database tables i.e. drops the current tables, create a new one and fill the data from csv files.