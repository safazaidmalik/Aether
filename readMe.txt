Near-Real_Time Data Warehouse Prototype - Semester 7 Practical Project

This is a Java based program which provides the implementation for Mesh Join to be used in a near realtime data warehouse. 
  Submitted to: Dr. Muhammad Asif Naeem
  Submitted by: Aamna Kamran
  Roll Number: 19I-0454
  Assignment Name: Practical Project: Building and Analysing a Near-Real-Time Data Warehouse
  Prototype for METRO Shopping Store in Pakistan
  Submission Date: Friday, 2nd December, 2022

*All analytical anaylsis and queries related to the data warehouse have been provided in a separate report.

Required Java Imports (already included in the project)
  import java.sql.Connection;
  import java.sql.PreparedStatement;
  import java.sql.ResultSet;
  import java.sql.Statement;
  import java.util.*;
  import java.util.Scanner;
  import java.util.Calendar;
  import java.text.ParseException;

For using MySQL as the database:
  1. create a table on your local host for storing the master data
    a) create transactions, customers, and products tables and populate them (or run the provided script)
  2. create another table on your local host for you data warehouse
    b) run script to create the dimension tables and the fact table
  3. add the .jar file present in the project's lib folder into the project structure
  
Running the Application
  1. build the program and then go to main and run the program
  2. you will be required to enter your database credentials (username, password wtc)
*no further input is required on the user's part

Please Note
  For execution of the program, a Java Runtime must be installed on the local operating system.
  
Troubleshooting
  In case you are not able to connect to your database check if your local host is set on port 3306; if not then go to MyJDBC class in the project 
  and change all occurences of the string: "jdbc:mysql://localhost:3306/" to "jdbc:mysql://localhost:#port number#/" where #port number# 
  will be replaced by whatever port your local host is using.

