# AutoWood
#### Video Demo:  <URL HERE>
#### Description:

AutoWood is web application that purpose is to control the production process. It's created around SQL database to help different parts of company keep the track of production process. It involves the Warehouse, Orders and Productions subpages.
I would like to describe each of the sections.

#### Database

For the purpose of this project, I wrote code to import database from Excell XLS file. It's save for future usage but inactive for now as database is complete. It's located in helpers.py inside impdb() function:

>def impdb():

#### Orders

Orders is the main part of the application. Although the production process doesnt start here, all actions and status are visible here. 
![](https://github.com/advdylan/my_projects/blob/main/orders.jpg)
Notes section allows to leave a note to a certain order. It's saved inside database. Status shows the production progress on every of the order. The table's row change it's color in 3 conditions. Whether the order is complete, not even started or in progress. DELETE function works for both production and orders tables. Send to production does transfer and order from order table to production table. It doesnt work automatically. The last function here is finish. It sends certain order to Warehouse on click. The order is removed from production and orders table and then beign added to warehouse table. 

 

