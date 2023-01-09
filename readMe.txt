AETHER: Desktop Application for the generation of realistic 3D outdoor virtual scenes using Natural Language Processing
Final Year Project

This is a Java based program which provides the implementation for Mesh Join to be used in a near realtime data warehouse. 
  Submitted to: FYP Committee FAST Islamabad
  Submitted by: Aamna Kamran, Momin Tariq and Safa Zaid Malik
  Roll Number: 19I-0454, 19I-0437 and 19I-0555
  Project Type: Development
  Group Number: F22-062
  Submission Date: Sunday, 9th January, 2023

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

