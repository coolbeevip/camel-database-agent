INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('AS', 'Arts and Sciences', 3, 1, 1);
INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('CC', 'College Center', 3, 1, 0);
INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('GYM', 'PE and Wellness', 1, 0, 1);
INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('IB', 'Instructional Building', 3, 1, 1);
INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('LB', 'Library', 2, 1, 1);
INSERT INTO Buildings (BuildingCode, BuildingName, NumberOfFloors, ElevatorAccess, SiteParkingAvailable) VALUES ('TB', 'Technology Building', 2, 1, 1);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('ACC', 'Accounting', 1);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('ART', 'Art', 3);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('BIO', 'Biology', 2);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('BUS', 'Business', 1);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('CHE', 'Chemistry', 2);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('CIS', 'Computer Information Systems', 5);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('CSC', 'Computer Science', 5);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('ECO', 'Economics', 4);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('ENG', 'English', 3);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('FRE', 'French', 3);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('GEG', 'Geography', 4);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('GER', 'German', 3);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('HIS', 'History', 4);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('JRN', 'Journalism', 1);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('MAT', 'Math', 2);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('MUS', 'Music', 3);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('PHY', 'Physics', 2);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('POL', 'Political Science', 4);
INSERT INTO Categories (CategoryID, CategoryDescription, DepartmentID) VALUES ('PSY', 'Psychology', 4);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1131, 'LB', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1142, 'LB', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1231, 'LB', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1514, 'AS', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1515, 'AS', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1519, 'AS', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1525, 'AS', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1530, 'AS', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1532, 'AS', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1619, 'AS', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1622, 'AS', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1624, 'AS', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1627, 'AS', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1639, 'TB', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1640, 'TB', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1641, 'TB', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (1642, 'TB', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (2357, 'CC', 1);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (2408, 'IB', 0);
INSERT INTO Class_Rooms (ClassRoomID, BuildingCode, PhoneAvailable) VALUES (2423, 'IB', 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1000, 11, 1231, 5, '2017-09-12', '10:00:00', 50, 0, 1, 1, 1, 1, 1);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1002, 12, 1619, 4, '2017-09-11', '15:30:00', 110, 1, 0, 1, 0, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1004, 13, 1627, 4, '2017-09-11', '08:00:00', 50, 1, 0, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1006, 13, 1627, 4, '2017-09-11', '09:00:00', 110, 1, 0, 1, 0, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1012, 14, 1627, 4, '2017-09-12', '13:00:00', 110, 0, 1, 0, 1, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1020, 15, 3404, 4, '2017-09-12', '13:00:00', 110, 0, 1, 0, 1, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1030, 16, 1231, 5, '2017-09-11', '11:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1031, 16, 1231, 5, '2017-09-11', '14:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1156, 37, 3443, 5, '2017-09-11', '16:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1162, 37, 3443, 5, '2017-09-11', '09:00:00', 140, 1, 0, 1, 0, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1168, 37, 3445, 5, '2017-09-11', '11:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1180, 38, 3446, 5, '2017-09-11', '11:30:00', 140, 1, 0, 1, 0, 0, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1183, 38, 3415, 5, '2017-09-11', '13:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1184, 38, 3415, 5, '2017-09-11', '14:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1196, 39, 3415, 5, '2017-09-11', '15:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1500, 33, 1142, 5, '2017-09-11', '08:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1502, 34, 1142, 5, '2017-09-11', '09:00:00', 50, 1, 1, 1, 1, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1560, 35, 2408, 3, '2017-09-12', '10:00:00', 50, 0, 1, 0, 1, 0, 1);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1562, 36, 2408, 5, '2017-09-11', '12:00:00', 140, 1, 0, 0, 0, 1, 0);
INSERT INTO Classes (ClassID, SubjectID, ClassRoomID, Credits, StartDate, StartTime, Duration, MondaySchedule, TuesdaySchedule, WednesdaySchedule, ThursdaySchedule, FridaySchedule, SaturdaySchedule) VALUES (1642, 29, 1514, 2, '2017-09-12', '11:00:00', 50, 0, 1, 0, 1, 0, 0);
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (1, 'ACC', 'ACC 210', 'Financial Accounting Fundamentals I', 'Introduces basic accounting concepts, principles and prodcedures for recording business transactions and developing financial accounting reports. Excel spreadsheet component.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectPreReq, SubjectDescription) VALUES (2, 'ACC', 'ACC 220', 'Financial Accounting Fundamentals II', 'ACC 210', 'Applications of basic accounting concepts, principles and procedures to more complex business situations and to different forms of enterprise ownership. Includes computerized element. Prereq: ACC 210 or instructor permission.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectPreReq, SubjectDescription) VALUES (3, 'ACC', 'ACC 230', 'Fundamentals of Managerial Accounting', 'ACC 220', 'Analysis of accounting data as part of the managerial process of planning, decision making and control. Concentrates on economic decision making in enterprises. Includes computerized element. Prereq: ACC 220 or instructor permission.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectPreReq, SubjectDescription) VALUES (4, 'ACC', 'ACC 251', 'Intermediate Accounting', 'ACC 220', 'In-depth review of financial accounting principles. Emphasizes the conceptual framework of accounting, revenue and expense recognition. Accounts Receivable, Depreciation, and Amortization, etc. Prereq: ACC 220 or instructor permission.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectPreReq, SubjectDescription) VALUES (5, 'ACC', 'ACC 257', 'Business Tax Accounting', 'ACC 220', 'Basic principles, practices and governmental regulations (Federal, Washington, State, and local) involved in business tax accounting including filing returns, record keeping, tax planning, and registrations and business licenses. Prereq: ACC 220 or instructors permissions.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (6, 'BUS', 'BUS 101', 'Introduction to Business', 'Survey of businss practices. Covers business terminology, forms of business ownership, franchising, small and international businesses, leadership and management, marketing principles, financing and investment methods, and business environment.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (7, 'BUS', 'BUS 155', 'Developing A Feasibility Plan', 'With the aid of a counselor, a feasibility plan will be developed which will be the basis or start of your business plan. Must be concurrently enrolled in BUS 151.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (8, 'BUS', 'BUS 151', 'Introduction to Entrepreneurship', 'Overview of the entrepreneurial process, examination of the marketplace, and discussion of successful business strategies. Product selection, selling and marketing strategies. Sources of information and assistance. Must be concurrently enrolled in BUS 155.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (9, 'BUS', 'BUS 170', 'Information Technology I', 'Uses Word for Windows word processing skills, document formatting, keyboarding, and 10-key keypad skills. Emphasis on preparing letters, memos, reports, and tables. Introduces Excel spreadsheet basics.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectPreReq, SubjectDescription) VALUES (10, 'BUS', 'BUS 171', 'Information Technology II', 'BUS 170', 'Uses intermediate Word features including formatting and production, mail merge, macros, text columns, graphics, and fonts; Excel spreadsheet; and introduction to PowerPoint presentation software, Internet and email. Prereq: BUS 170 or permission from instructor.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (11, 'ART', 'ART 100', 'Introduction to Art', 'Historical backgrounds and design fundamentals which have affected art. Includes slide lectures, reading and practical studio applications.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (12, 'ART', 'ART 101', 'Design', 'Studio sudies in the fundamentals of two-dimensional art with problems based on line, space, texture, shape and color theories. Includes practical applications of these theories to design.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (13, 'ART', 'ART 111', 'Drawing', 'Study of line, value, space, perspective, and compostion through the use o charcoal, pencil, pen, and brush.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (14, 'ART', 'ART 201', 'Painting', 'Beginning painting in oil or synthetic media using still life. Emphasis on basics such as composition, value studies, color mixing, canvas preparation, and various styles and techniques. No prerequisite; some drawing background important.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (15, 'ART', 'ART 210', 'Computer Art', 'Explore the elements of art such as line, value, space, composition, and color through the use of the computer. Sudents will create works of art using the computer.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (16, 'ART', 'ART 251', 'Art History', 'Surveys major forms of visual expression from the Paleolithic, Egyptian, Mesopotamian, Greek, Roman, and Early Christian periods. Includes painting, sculpture, architecture, lectures, slides, and readings.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (17, 'BIO', 'BIO 100', 'Biological Principles', 'An introductory biology course with lab for the non-science major. May include maintenance of the balance between man and his environment, nutrition, genetics and inheritence, ecological principles, plant and animal diversity, and evolution.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (18, 'BIO', 'BIO 101', 'General Biology', 'Basic bilogical concepts with emphasis on general cell processes, plant and animal diversity, morphyology, limited reproduction, phylogeny of the living organisms, exploration of molecular genetics.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (19, 'BIO', 'BIO 280', 'Microbiology', 'Introduction to micro-organisms including microbial cell structure and function; metabolism; microbial genetics; and the role of micro-organisms in disease, immunity, and other selected applied areas.');
INSERT INTO Subjects (SubjectID, CategoryID, SubjectCode, SubjectName, SubjectDescription) VALUES (20, 'CHE', 'CHE 101', 'Chemistry', 'General chemistry for non-science majors. Completion of CHE 101 fulfills chemistry requirements for many health science majors.');
INSERT INTO Departments (DepartmentID, DeptName, DeptChair) VALUES (1, 'Business Administration', 98012);
INSERT INTO Departments (DepartmentID, DeptName, DeptChair) VALUES (2, 'Sciences', 98010);
INSERT INTO Departments (DepartmentID, DeptName, DeptChair) VALUES (3, 'Humanities', 98005);
INSERT INTO Departments (DepartmentID, DeptName, DeptChair) VALUES (4, 'Social Sciences', 98059);
INSERT INTO Departments (DepartmentID, DeptName, DeptChair) VALUES (5, 'Information Technology', 98007);
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98005, 'Suzanne', 'Viescas', '15127 NE 24th, #383', 'Redmond', 'WA', '98052', '425', '555-2686', 44000.0, '1986-05-31', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98007, 'Gary', 'Hallmark', 'Route 2, Box 203B', 'Auburn', 'WA', '98002', '253', '555-2676', 53000.0, '1985-01-21', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98010, 'Jeffrey', 'Smith', '30301 - 166th Ave. N.E.', 'Fremont', 'CA', '94538', '510', '555-2596', 52000.0, '1983-10-06', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98011, 'Ann', 'Patterson', '16 Maple Lane', 'Marysville', 'WA', '98271', '253', '555-2591', 45000.0, '1983-10-16', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98012, 'Robert', 'Brown', '672 Lamont Ave', 'Houston', 'TX', '77201', '713', '555-2491', 49000.0, '1989-02-09', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98013, 'Deb', 'Waldal', '908 W. Capital Way', 'Tacoma', 'WA', '98413', '253', '555-2496', 44000.0, '1986-07-05', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98014, 'Peter', 'Brehm', '722 Moss Bay Blvd.', 'Kirkland', 'WA', '98033', '425', '555-2501', 60000.0, '1986-07-16', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98019, 'Mariya', 'Sergienko', '901 Pine Avenue', 'Portland', 'OR', '97208', '503', '555-2526', 45000.0, '1989-11-02', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98020, 'Jim', 'Glynn', '13920 S.E. 40th Street', 'Bellevue', 'WA', '98009', '425', '555-2531', 45000.0, '1985-08-02', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98021, 'Tim', 'Smith', '30301 - 166th Ave. N.E.', 'Seattle', 'WA', '98106', '206', '555-2536', 40000.0, '1988-12-17', 'Registrar');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98025, 'Carol', 'Viescas', '722 Moss Bay Blvd.', 'Kirkland', 'WA', '98033', '425', '555-2576', 50000.0, '1984-04-12', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98028, 'Alaina', 'Hallmark', 'Route 2, Box 203B', 'Marysville', 'WA', '98270', '425', '555-2631', 57000.0, '1984-01-17', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98030, 'Liz', 'Keyser', '13920 S.E. 40th Street', 'Bellevue', 'WA', '98006', '425', '555-2556', 48000.0, '1988-05-31', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98036, 'Sam', 'Abolrous', '611 Alpine Drive', 'Palm Springs', 'CA', '92263', '760', '555-2611', 60000.0, '1982-11-20', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98040, 'Jim', 'Wilson', '101 NE 88th', 'Salem', 'OR', '97301', '503', '555-2636', 50000.0, '1987-01-13', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98042, 'David', 'Smith', '311 20th Ave. N.E.', 'Fremont', 'CA', '94538', '510', '555-2646', 52000.0, '1991-12-17', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98043, 'Kathryn', 'Patterson', '16 Maple Lane', 'Seattle', 'WA', '98115', '206', '555-2651', 25000.0, '1984-11-14', 'Secretary');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98045, 'Michael', 'Hernandez', 'PO Box 223311', 'Tacoma', 'WA', '98413', '253', '555-2711', 60000.0, '1990-08-20', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98048, 'Joyce', 'Bonnicksen', '2424 Thames Drive', 'Bellevue', 'WA', '98006', '425', '555-2726', 60000.0, '1986-03-02', 'Faculty');
INSERT INTO Staff (StaffID, StfFirstName, StfLastname, StfStreetAddress, StfCity, StfState, StfZipCode, StfAreaCode, StfPhoneNumber, Salary, DateHired, Position) VALUES (98052, 'Katherine', 'Ehrlich', '777 Fenexet Blvd', 'Redmond', 'WA', '98052', '425', '555-0399', 45000.0, '1985-03-08', 'Faculty');
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98005, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98007, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98010, 'Professor', 'On Leave', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98011, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98012, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98013, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98014, 'Associate Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98019, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98020, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98025, 'Associate Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98028, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98030, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98036, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98040, 'Associate Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98042, 'Associate Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98045, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98048, 'Professor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98052, 'Instructor', 'Part Time', 0);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98053, 'Instructor', 'Full Time', 1);
INSERT INTO Faculty (StaffID, Title, Status, Tenured) VALUES (98055, 'Professor', 'Full Time', 1);
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98005, 'ART');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98005, 'ENG');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98005, 'MUS');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98007, 'ACC');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98007, 'ART');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98007, 'CIS');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98007, 'MAT');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98010, 'ACC');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98010, 'CIS');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98010, 'MAT');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98011, 'ENG');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98011, 'HIS');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98011, 'MAT');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98012, 'ACC');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98012, 'ECO');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98012, 'MAT');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98013, 'CIS');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98013, 'CSC');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98013, 'MAT');
INSERT INTO Faculty_Categories (StaffID, CategoryID) VALUES (98014, 'ART');
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1000, 98014);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1002, 98036);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1004, 98019);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1006, 98045);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1012, 98030);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1020, 98028);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1030, 98036);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1031, 98005);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1156, 98055);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1162, 98064);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1168, 98055);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1180, 98011);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1183, 98005);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1184, 98011);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1196, 98028);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1500, 98028);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1502, 98036);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1560, 98028);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (1562, 98036);
INSERT INTO Faculty_Classes (ClassID, StaffID) VALUES (2001, 98020);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98005, 12, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98005, 16, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98005, 34, 9.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98005, 36, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98005, 38, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98007, 2, 9.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98007, 5, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98007, 14, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98007, 24, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98007, 46, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98010, 2, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98010, 5, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98010, 24, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98010, 48, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98011, 38, 9.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98011, 43, 8.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98011, 49, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98012, 1, 9.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98012, 4, 10.0);
INSERT INTO Faculty_Subjects (StaffID, SubjectID, ProficiencyRating) VALUES (98012, 32, 9.0);
INSERT INTO Majors (MajorID, Major) VALUES (1, 'General Studies');
INSERT INTO Majors (MajorID, Major) VALUES (2, 'English');
INSERT INTO Majors (MajorID, Major) VALUES (3, 'Music');
INSERT INTO Majors (MajorID, Major) VALUES (4, 'Information Sciences');
INSERT INTO Majors (MajorID, Major) VALUES (5, 'Accounting');
INSERT INTO Majors (MajorID, Major) VALUES (6, 'Art');
INSERT INTO Majors (MajorID, Major) VALUES (7, 'Mathematics');
INSERT INTO Student_Class_Status (ClassStatus, ClassStatusDescription) VALUES (1, 'Enrolled');
INSERT INTO Student_Class_Status (ClassStatus, ClassStatusDescription) VALUES (2, 'Completed');
INSERT INTO Student_Class_Status (ClassStatus, ClassStatusDescription) VALUES (3, 'Withdrew');
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 1000, 2, 99.83);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 1168, 2, 70.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 2907, 2, 67.33);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 3085, 2, 87.14);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 4180, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 5917, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1001, 6082, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1002, 1156, 2, 86.33);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1002, 1500, 2, 85.72);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1002, 2223, 3, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1002, 2889, 2, 68.22);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 1156, 2, 71.09);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 1500, 2, 89.05);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 1502, 2, 75.71);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 2911, 2, 85.39);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 4180, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 4560, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1003, 6082, 1, 0.0);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1004, 1162, 2, 91.44);
INSERT INTO Student_Schedules (StudentID, ClassID, ClassStatus, Grade) VALUES (1004, 2410, 2, 90.56);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1001, 'Kerry', 'Patterson', '9877 Hacienda Drive', 'San Antonio', 'TX', '78284', '210', '555-2706', 74.465, 1);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1002, 'David', 'Hamilton', '908 W. Capital Way', 'Tacoma', 'WA', '98413', '253', '555-2701', 78.755, 2);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1003, 'Betsy', 'Stadick', '611 Alpine Drive', 'Palm Springs', 'CA', '92263', '760', '555-2696', 85.235, 3);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1004, 'Janice', 'Galvin', '4110 Old Redmond Rd.', 'Redmond', 'WA', '98052', '425', '555-2691', 81.0, 4);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1005, 'Doris', 'Hartwig', '4726 - 11th Ave. N.E.', 'Seattle', 'WA', '98105', '206', '555-2671', 72.225, 5);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1006, 'Scott', 'Bishop', '66 Spring Valley Drive', 'Medford', 'OR', '97501', '541', '555-2666', 88.5, 6);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1007, 'Elizabeth', 'Hallmark', 'Route 2, Box 203B', 'Marysville', 'WA', '98271', '253', '555-2521', 87.65, 7);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1008, 'Sara', 'Sheskey', '16679 NE 41st Court', 'Portland', 'OR', '97208', '503', '555-2566', 84.625, 1);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1009, 'Karen', 'Smith', '30301 - 166th Ave. N.E.', 'Eugene', 'OR', '97401', '541', '555-2551', 80.0, 2);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1010, 'Marianne', 'Wier', '908 W. Capital Way', 'Tacoma', 'WA', '98413', '253', '555-2606', 83.55, 3);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1011, 'John', 'Kennedy', '16679 NE 41st Court', 'Portland', 'OR', '97208', '503', '555-2621', 77.65, 4);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1012, 'Sarah', 'Thompson', '2222 Springer Road', 'Lubbock', 'TX', '79402', '806', '555-2626', 89.5, 5);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1013, 'Michael', 'Viescas', '15127 NE 24th, #383', 'Redmond', 'WA', '98052', '425', '555-2656', 80.25, 6);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1014, 'Kendra', 'Bonnicksen', '12330 Larchlemont Lane', 'Seattle', 'WA', '98105', '206', '555-2716', 85.55, 7);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1015, 'Brannon', 'Jones', '777 Fenexet Blvd', 'Long Beach', 'CA', '90809', '562', '555-0399', 86.0, 2);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1016, 'Steve', 'Pundt', '2500 Rosales Lane', 'Dallas', 'TX', '75204', '972', '555-9938', 77.125, 4);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1017, 'George', 'Chavez', '281 Old Navy Road', 'Marysville', 'WA', '98270', '206', '555-9930', 79.25, 6);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA, StudMajor) VALUES (1018, 'Richard', 'Lum', '754 Fourth Ave', 'Seattle', 'WA', '98115', '206', '555-2296', 72.55, 7);
INSERT INTO Students (StudentID, StudFirstName, StudLastName, StudStreetAddress, StudCity, StudState, StudZipCode, StudAreaCode, StudPhoneNumber, StudGPA) VALUES (1019, 'Daffy', 'Dumbwit', '4567 NE 32nd Ct', 'Bellevue', 'WA', '98002', '425', '555-9872', 0.0);