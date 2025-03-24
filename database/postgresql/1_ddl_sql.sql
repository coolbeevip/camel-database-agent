CREATE TABLE Buildings (
    BuildingCode TEXT NOT NULL PRIMARY KEY,
    BuildingName TEXT,
    NumberOfFloors INTEGER,
    ElevatorAccess BOOLEAN NOT NULL DEFAULT FALSE,
    SiteParkingAvailable BOOLEAN NOT NULL DEFAULT FALSE
);
COMMENT ON TABLE Buildings IS '建筑物信息表';
COMMENT ON COLUMN Buildings.BuildingCode IS '建筑物代码';
COMMENT ON COLUMN Buildings.BuildingName IS '建筑物名称';
COMMENT ON COLUMN Buildings.NumberOfFloors IS '楼层数量';
COMMENT ON COLUMN Buildings.ElevatorAccess IS '电梯可用性';
COMMENT ON COLUMN Buildings.SiteParkingAvailable IS '场地停车可用性';

CREATE TABLE Categories (
    CategoryID TEXT NOT NULL PRIMARY KEY,
    CategoryDescription TEXT,
    DepartmentID INTEGER DEFAULT 0
);
COMMENT ON TABLE Categories IS '类别信息表';
COMMENT ON COLUMN Categories.CategoryID IS '类别ID';
COMMENT ON COLUMN Categories.CategoryDescription IS '类别描述';
COMMENT ON COLUMN Categories.DepartmentID IS '部门ID';

CREATE TABLE Majors (
    MajorID INTEGER NOT NULL PRIMARY KEY,
    Major TEXT
);
COMMENT ON TABLE Majors IS '专业信息表';
COMMENT ON COLUMN Majors.MajorID IS '专业ID';
COMMENT ON COLUMN Majors.Major IS '专业名称';

CREATE TABLE Staff (
    StaffID INTEGER NOT NULL PRIMARY KEY,
    StfFirstName TEXT,
    StfLastname TEXT,
    StfStreetAddress TEXT,
    StfCity TEXT,
    StfState TEXT,
    StfZipCode TEXT,
    StfAreaCode TEXT,
    StfPhoneNumber TEXT,
    Salary REAL,
    DateHired DATE,
    Position TEXT
);
COMMENT ON TABLE Staff IS '员工信息表';
COMMENT ON COLUMN Staff.StaffID IS '员工ID';
COMMENT ON COLUMN Staff.StfFirstName IS '员工名';
COMMENT ON COLUMN Staff.StfLastname IS '员工姓';
COMMENT ON COLUMN Staff.StfStreetAddress IS '员工街道地址';
COMMENT ON COLUMN Staff.StfCity IS '员工城市';
COMMENT ON COLUMN Staff.StfState IS '员工州';
COMMENT ON COLUMN Staff.StfZipCode IS '员工邮政编码';
COMMENT ON COLUMN Staff.StfAreaCode IS '员工区号';
COMMENT ON COLUMN Staff.StfPhoneNumber IS '员工电话号码';
COMMENT ON COLUMN Staff.Salary IS '薪资';
COMMENT ON COLUMN Staff.DateHired IS '雇佣日期';
COMMENT ON COLUMN Staff.Position IS '职位';

CREATE TABLE Student_Class_Status (
    ClassStatus INTEGER NOT NULL PRIMARY KEY,
    ClassStatusDescription TEXT
);
COMMENT ON TABLE Student_Class_Status IS '班级状态信息表';
COMMENT ON COLUMN Student_Class_Status.ClassStatus IS '班级状态ID';
COMMENT ON COLUMN Student_Class_Status.ClassStatusDescription IS '班级状态描述';

CREATE TABLE Class_Rooms (
    ClassRoomID INTEGER NOT NULL PRIMARY KEY,
    BuildingCode TEXT,
    PhoneAvailable BOOLEAN NOT NULL DEFAULT FALSE
);
COMMENT ON TABLE Class_Rooms IS '教室信息表';
COMMENT ON COLUMN Class_Rooms.ClassRoomID IS '教室ID';
COMMENT ON COLUMN Class_Rooms.BuildingCode IS '建筑物代码';
COMMENT ON COLUMN Class_Rooms.PhoneAvailable IS '电话可用性';

CREATE TABLE Departments (
    DepartmentID INTEGER NOT NULL PRIMARY KEY,
    DeptName TEXT,
    DeptChair INTEGER DEFAULT 0
);
COMMENT ON TABLE Departments IS '部门信息表';
COMMENT ON COLUMN Departments.DepartmentID IS '部门ID';
COMMENT ON COLUMN Departments.DeptName IS '部门名称';
COMMENT ON COLUMN Departments.DeptChair IS '部门主任ID';

CREATE TABLE Faculty (
    StaffID INTEGER NOT NULL PRIMARY KEY,
    Title TEXT,
    Status TEXT,
    Tenured BOOLEAN NOT NULL DEFAULT FALSE
);
COMMENT ON TABLE Faculty IS '教职员工信息表';
COMMENT ON COLUMN Faculty.StaffID IS '员工ID';
COMMENT ON COLUMN Faculty.Title IS '职称';
COMMENT ON COLUMN Faculty.Status IS '状态';
COMMENT ON COLUMN Faculty.Tenured IS '终身职教职';

CREATE TABLE Students (
    StudentID INTEGER NOT NULL PRIMARY KEY,
    StudFirstName TEXT,
    StudLastName TEXT,
    StudStreetAddress TEXT,
    StudCity TEXT,
    StudState TEXT,
    StudZipCode TEXT,
    StudAreaCode TEXT,
    StudPhoneNumber TEXT,
    StudGPA REAL DEFAULT 0,
    StudMajor INTEGER
);
COMMENT ON TABLE Students IS '学生信息表';
COMMENT ON COLUMN Students.StudentID IS '学生ID';
COMMENT ON COLUMN Students.StudFirstName IS '学生名';
COMMENT ON COLUMN Students.StudLastName IS '学生姓';
COMMENT ON COLUMN Students.StudStreetAddress IS '学生街道地址';
COMMENT ON COLUMN Students.StudCity IS '学生城市';
COMMENT ON COLUMN Students.StudState IS '学生州';
COMMENT ON COLUMN Students.StudZipCode IS '学生邮政编码';
COMMENT ON COLUMN Students.StudAreaCode IS '学生区号';
COMMENT ON COLUMN Students.StudPhoneNumber IS '学生电话号码';
COMMENT ON COLUMN Students.StudGPA IS '学生GPA';
COMMENT ON COLUMN Students.StudMajor IS '学生专业ID';

CREATE TABLE Subjects (
    SubjectID INTEGER NOT NULL PRIMARY KEY,
    CategoryID TEXT,
    SubjectCode TEXT,
    SubjectName TEXT,
    SubjectPreReq TEXT DEFAULT NULL,
    SubjectDescription TEXT
);
COMMENT ON TABLE Subjects IS '科目信息表';
COMMENT ON COLUMN Subjects.SubjectID IS '科目ID';
COMMENT ON COLUMN Subjects.CategoryID IS '类别ID';
COMMENT ON COLUMN Subjects.SubjectCode IS '科目代码';
COMMENT ON COLUMN Subjects.SubjectName IS '科目名称';
COMMENT ON COLUMN Subjects.SubjectPreReq IS '科目先修课程';
COMMENT ON COLUMN Subjects.SubjectDescription IS '科目描述';

CREATE TABLE Classes (
    ClassID INTEGER NOT NULL PRIMARY KEY,
    SubjectID INTEGER DEFAULT 0,
    ClassRoomID INTEGER DEFAULT 0,
    Credits INTEGER DEFAULT 0,
    StartDate DATE,
    StartTime TIME,
    Duration INTEGER DEFAULT 0,
    MondaySchedule BOOLEAN NOT NULL DEFAULT FALSE,
    TuesdaySchedule BOOLEAN NOT NULL DEFAULT FALSE,
    WednesdaySchedule BOOLEAN NOT NULL DEFAULT FALSE,
    ThursdaySchedule BOOLEAN NOT NULL DEFAULT FALSE,
    FridaySchedule BOOLEAN NOT NULL DEFAULT FALSE,
    SaturdaySchedule BOOLEAN NOT NULL DEFAULT FALSE
);
COMMENT ON TABLE Classes IS '课程信息表';
COMMENT ON COLUMN Classes.ClassID IS '课程ID';
COMMENT ON COLUMN Classes.SubjectID IS '科目ID';
COMMENT ON COLUMN Classes.ClassRoomID IS '教室ID';
COMMENT ON COLUMN Classes.Credits IS '学分';
COMMENT ON COLUMN Classes.StartDate IS '开始日期';
COMMENT ON COLUMN Classes.StartTime IS '开始时间';
COMMENT ON COLUMN Classes.Duration IS '持续时间';
COMMENT ON COLUMN Classes.MondaySchedule IS '周一课程安排';
COMMENT ON COLUMN Classes.TuesdaySchedule IS '周二课程安排';
COMMENT ON COLUMN Classes.WednesdaySchedule IS '周三课程安排';
COMMENT ON COLUMN Classes.ThursdaySchedule IS '周四课程安排';
COMMENT ON COLUMN Classes.FridaySchedule IS '周五课程安排';
COMMENT ON COLUMN Classes.SaturdaySchedule IS '周六课程安排';

CREATE TABLE Faculty_Categories (
    StaffID INTEGER NOT NULL,
    CategoryID TEXT NOT NULL,
    PRIMARY KEY (StaffID, CategoryID)
);
COMMENT ON TABLE Faculty_Categories IS '教职员工类别信息表';
COMMENT ON COLUMN Faculty_Categories.StaffID IS '员工ID';
COMMENT ON COLUMN Faculty_Categories.CategoryID IS '类别ID';

CREATE TABLE Faculty_Subjects (
    StaffID INTEGER NOT NULL,
    SubjectID INTEGER NOT NULL,
    ProficiencyRating REAL DEFAULT 0,
    PRIMARY KEY (StaffID, SubjectID)
);
COMMENT ON TABLE Faculty_Subjects IS '教职员工科目信息表';
COMMENT ON COLUMN Faculty_Subjects.StaffID IS '员工ID';
COMMENT ON COLUMN Faculty_Subjects.SubjectID IS '科目ID';
COMMENT ON COLUMN Faculty_Subjects.ProficiencyRating IS '专业能力评分';

CREATE TABLE Faculty_Classes (
    ClassID INTEGER NOT NULL,
    StaffID INTEGER NOT NULL,
    PRIMARY KEY (ClassID, StaffID)
);
COMMENT ON TABLE Faculty_Classes IS '教职员工授课信息表';
COMMENT ON COLUMN Faculty_Classes.ClassID IS '课程ID';
COMMENT ON COLUMN Faculty_Classes.StaffID IS '员工ID';

CREATE TABLE Student_Schedules (
    StudentID INTEGER NOT NULL,
    ClassID INTEGER NOT NULL,
    ClassStatus INTEGER DEFAULT 0,
    Grade REAL DEFAULT 0,
    PRIMARY KEY (StudentID, ClassID)
);
COMMENT ON TABLE Student_Schedules IS '学生课程安排信息表';
COMMENT ON COLUMN Student_Schedules.StudentID IS '学生ID';
COMMENT ON COLUMN Student_Schedules.ClassID IS '课程ID';
COMMENT ON COLUMN Student_Schedules.ClassStatus IS '班级状态';
COMMENT ON COLUMN Student_Schedules.Grade IS '成绩';