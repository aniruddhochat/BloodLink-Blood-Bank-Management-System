# BloodLink-Blood-Bank-Management-System
Blood Bank Management System to efficiently manage blood collection, storage, and distribution from donors to recipients. 


1. Web App Architecture: 

 

1.1 Web Architecture Design 

The web application architecture specifies the connections between web-based programs, databases, and middleware systems. It also makes sure that several programs can run at once. The web app that we have created follows the MVC schema as follows: 

Model: In our application all the backend data logic is stored in MySQL Workbench. 

View: For creating the front end of our application we have used HTML, CSS and Bootstrap. 

Controller: In our application Flask acts as the brain that will control how the data is displayed. 

 

 

 

Figure A: Architecture Diagram  

 

Users would be able to interact with the web application based on the above web framework diagram (Figure A), for which we designed the user interface using HTML, CSS, and Bootstrap. We constructed a MySql database at the backend. Flask is a Python-based web framework that may be used as a backend framework for constructing Python-based web applications. We have used it to create APIs and online services that interact with HTML, CSS, and Bootstrap frontend. Flask can handle user queries and responses, connect to databases, and perform other backend activities. Finally, we would use Netlify, a cloud-based web development platform, to deploy our web application. Netlify offers a comprehensive range of tools and services for developing, deploying, and managing contemporary web applications. It is a well-liked platform for hosting both full-stack web apps and static webpages. 

 

1.2 Backend Database 

We have used Flask, a micro web framework in python to simplify communication between python and our SQL database. Flask is a powerful tool that helps create and scale web apps quickly and simply. Initially, we created our database on MySQL Workbench and then we used the commands as seen in Figure B, to create a connection with the MySQL database server and to access the database.  

 

Data Security: Hashing has been applied to the password field to guarantee user data security. Our application is designed in such a way that other users cannot see the personal data of other users. 

 

 

 

 

 

Figure B: Code Snip- Database connection using Flask 

 

1.3 Frontend Web App 

We have built the frontend of our application using HTML, CSS and Bootstrap. HTML is the foundation of all our web pages and is used to define the structure and content of the page. CSS is used to style our web pages. It is basically used to create responsive designs and define the visual appearance of the HTML elements. Bootstrap is a popular front-end framework which provides pre-built components like navigation menus, forms, buttons that can be easily customized using CSS. 

 

Application Interactivity: 

Our web application is meant to allow users to execute CRUD operations such as click, choose, create, search, view, update and delete (admin privilege). The home page allows users to Signup, where they can select predefined values for Blood Type, Date of Birth, Gender, and User Type appearing in a drop-down format. Similarly, users will be able to examine blood inventory by clicking, and they will be able to interact with a location map on the Contact us page. After logging in, customers can book an appointment, and the appointment page allows them to search for blood banks based on their search query. The application also allows users to update their appointment in the appointment page. 

 

 

Admin privileges: 

The admin privileges in our web application include: 

Viewing and managing user accounts like editing and deleting user accounts. 

Managing the inventory like viewing and updating the blood stock. 

Maintaining and viewing the patient’s history. 

 

2. Web App Layout: 

The color scheme that we have used for our web app includes a combination of red, white, grey and black text. Initially, the users can view the home page (Figure C) which contains the welcome text and images. This page also consists of the navigation bar which will direct users to different pages mentioned below from which the users could make use of the application functionalities. 

 

 

Figure C: Application Home Page 

 

Web Pages: 

About Us: This page contains some basic information about the application, mission, and team; users can navigate to Contact Us page by selecting the 'Get in contact' button. 

 

Inserting image... 

Figure D: About Us Page 

 

Contact Us: The user can request information that is not mentioned in the application on this page. When a user requests information, an entry in the database is generated. This page offers a form where users can enter their questions, contact information, and a map that displays the application location.   

 

                     

Figure E: Get in Touch Page 

 

Sign Up: First-time users who want to donate or receive blood will be sent to this page. Fields such as Blood Type, Date of Birth, Gender, and User Type have predetermined values that users can utilize while entering information. The information entered on the page will be stored in four database tables: 'BloodLinkUsers' and 'Donor,' 'Recipient,' or 'Employee,' depending on the user type. 

 

 

Figure F: Sign Up Page 

 

Login: This page allows users to login into the application on recurring basis, further from which the user can make an appointment either for blood donation or for receiving blood.  

 

           		Figure G: Login Page 

 

Request Appoinment: Users who are logged in and want to book an appointment will be led to this page. The Date and Time fields provide an interface via which users can pick the desired data. Users can look up the blood bank where they want to make an appointment. The entered information is then saved in the Appoinment database, which is then queried to display the appointment information in the Employee and Admin pages.  

 

 

Figure H: Appointment Page 

 

 

Inventory: This page would be visible to logged in, employee and admin users, it provides information about the availability of different blood groups at different blood banks. This data is critical for users to make decisions depending on blood availability. 

 

 

Figure I: Inventory Page 

 

Admin: This view is only available to admins. Admin can change user information or delete any user from this page. Admins can view, update, and delete user scheduled appointments, as well as view user history and blood stock. This page handles the aforementioned database operations. 

 

 

Figure J: Admin Page 

 

 

 
