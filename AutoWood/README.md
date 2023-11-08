# AutoWood
#### Video Demo:  <https://www.youtube.com/watch?v=LNARAWRAKD0>
#### Description:

![](https://github.com/advdylan/my_projects/blob/main/AutoWood/static/login.jpg?raw=true)

AutoWood is web application that purpose is to controll the production process. It's created around an SQL database to help different parts of the company keep the track of production process. It involves the Warehouse, Orders and Productions subpages.
I would like to describe each of the sections.


## Orders

Orders are the main part of the application. Although the production process doesnt start here, all actions and statuses are visible here. 
![Orders table](https://github.com/advdylan/my_projects/blob/main/orders.jpg?raw=true)
Notes section allows you to leave a note for a certain order. It's saved inside database. Status shows the production progress on every order. The table's row change it's color in 3 conditions. Whether the order is complete, not even started, or in progress. DELETE function works for both the production and orders tables. Send to production does transfer and order from order table to production table. It doesn't work automatically. The last function here is finish. It sends certain order to Warehouse on click. The order is removed from production and orders table and then beign added to warehouse table. 


## Production

Production table is much simplier than orders. It requires the user/worker to just use checkboxes to indicate if certain object is done. It is also recorded in the database and that's exacly how orders table can see the progress via countdays.py program. Deletings rows or finishing the order is up to person menaging the orders table.


## Warehouse

Warehouse is just a list containing all the finished orders. For future use I would like to create an engine for manual barcode scanner via the worker could scan the pack and automatically remove 
order from the list. 

## Database

For the purpose of this project, I wrote code to import database from Excell XLS file. It's save for future usage but inactive for now as database is complete. It's located in helpers.py inside impdb() function:

>def impdb():

![Database](https://github.com/advdylan/my_projects/blob/main/database_diagram.png?raw=true)

Going to to DATABASE menu is showing the whole list of products for this firm. There are four simple filters to help navigate the user. This table like all the tables in AutoWood are supported by jQuery table library. User can choose the amount of viewed lines or search the whole table. Main use for the database table is to create the Barcode. 

![Barcode](https://github.com/advdylan/my_projects/blob/main/barcode.jpg?raw=true)

Clicking the EAN_CODE value will create a barcode inside orders folder. How to use it to add new orders it's time to present the Barcode Scanner.

## Barcode Scanner - ACTION/SCAN BARCODE

The Barcode created in Database table is just the represention of specific product. To add it to orders we need to specify ZD(which is unique name for each order and customer) and notes.
Notes are shown in orders table. User can change it in future at orders table. Week is also required to specify. It helps creating many tables rather than viewing all orders in one table.
After pressing the button "Add Order" we finished the circle of managing the program.

![Database](https://github.com/advdylan/my_projects/blob/main/scanner.jpg?raw=true)

# AUTOWOOD


 

