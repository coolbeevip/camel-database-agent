CREATE TABLE Buildings (
    BuildingCode VARCHAR(50) NOT NULL PRIMARY KEY COMMENT '建筑物代码',
    BuildingName TEXT COMMENT '建筑物名称',
    NumberOfFloors INT COMMENT '楼层数量',
    ElevatorAccess TINYINT(1) NOT NULL DEFAULT 0 COMMENT '电梯可用性',
    SiteParkingAvailable TINYINT(1) NOT NULL DEFAULT 0 COMMENT '场地停车可用性'
) COMMENT = '建筑物信息表';

CREATE TABLE Categories (
    CategoryID VARCHAR(50) NOT NULL PRIMARY KEY COMMENT '类别ID',
    CategoryDescription TEXT COMMENT '类别描述',
    DepartmentID INT DEFAULT 0 COMMENT '部门ID'
) COMMENT = '类别信息表';

CREATE TABLE Majors (
    MajorID INT NOT NULL PRIMARY KEY COMMENT '专业ID',
    Major TEXT COMMENT '专业名称'
) COMMENT = '专业信息表';

CREATE TABLE Staff (
    StaffID INT NOT NULL PRIMARY KEY COMMENT '员工ID',
    StfFirstName TEXT COMMENT '员工名',
    StfLastname TEXT COMMENT '员工姓',
    StfStreetAddress TEXT COMMENT '员工街道地址',
    StfCity TEXT COMMENT '员工城市',
    StfState TEXT COMMENT '员工州',
    StfZipCode TEXT COMMENT '员工邮政编码',
    StfAreaCode TEXT COMMENT '员工区号',
    StfPhoneNumber TEXT COMMENT '员工电话号码',
    Salary FLOAT COMMENT '薪资',
    DateHired DATE COMMENT '雇佣日期',
    Position TEXT COMMENT '职位'
) COMMENT = '员工信息表';

CREATE TABLE Student_Class_Status (
    ClassStatus INT NOT NULL PRIMARY KEY COMMENT '班级状态ID',
    ClassStatusDescription TEXT COMMENT '班级状态描述'
) COMMENT = '班级状态信息表';

CREATE TABLE Class_Rooms (
    ClassRoomID INT NOT NULL PRIMARY KEY COMMENT '教室ID',
    BuildingCode VARCHAR(50) COMMENT '建筑物代码',
    PhoneAvailable TINYINT(1) NOT NULL DEFAULT 0 COMMENT '电话可用性'
) COMMENT = '教室信息表';

CREATE TABLE Departments (
    DepartmentID INT NOT NULL PRIMARY KEY COMMENT '部门ID',
    DeptName TEXT COMMENT '部门名称',
    DeptChair INT DEFAULT 0 COMMENT '部门主任ID'
) COMMENT = '部门信息表';

CREATE TABLE Faculty (
    StaffID INT NOT NULL PRIMARY KEY COMMENT '员工ID',
    Title TEXT COMMENT '职称',
    Status TEXT COMMENT '状态',
    Tenured TINYINT(1) NOT NULL DEFAULT 0 COMMENT '终身职教职'
) COMMENT = '教职员工信息表';

CREATE TABLE Students (
    StudentID INT NOT NULL PRIMARY KEY COMMENT '学生ID',
    StudFirstName TEXT COMMENT '学生名',
    StudLastName TEXT COMMENT '学生姓',
    StudStreetAddress TEXT COMMENT '学生街道地址',
    StudCity TEXT COMMENT '学生城市',
    StudState TEXT COMMENT '学生州',
    StudZipCode TEXT COMMENT '学生邮政编码',
    StudAreaCode TEXT COMMENT '学生区号',
    StudPhoneNumber TEXT COMMENT '学生电话号码',
    StudGPA FLOAT DEFAULT 0 COMMENT '学生GPA',
    StudMajor INT COMMENT '学生专业ID'
) COMMENT = '学生信息表';

CREATE TABLE Subjects (
    SubjectID INT NOT NULL PRIMARY KEY COMMENT '科目ID',
    CategoryID VARCHAR(50) COMMENT '类别ID',
    SubjectCode TEXT COMMENT '科目代码',
    SubjectName TEXT COMMENT '科目名称',
    SubjectPreReq TEXT DEFAULT NULL COMMENT '科目先修课程',
    SubjectDescription TEXT COMMENT '科目描述'
) COMMENT = '科目信息表';

CREATE TABLE Classes (
    ClassID INT NOT NULL PRIMARY KEY COMMENT '课程ID',
    SubjectID INT DEFAULT 0 COMMENT '科目ID',
    ClassRoomID INT DEFAULT 0 COMMENT '教室ID',
    Credits INT DEFAULT 0 COMMENT '学分',
    StartDate DATE COMMENT '开始日期',
    StartTime TIME COMMENT '开始时间',
    Duration INT DEFAULT 0 COMMENT '���续时间',
    MondaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '周一课程安排',
    TuesdaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '���二课程安排',
    WednesdaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '周三课程安排',
    ThursdaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '周四课程安排',
    FridaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '周五课程安排',
    SaturdaySchedule TINYINT(1) NOT NULL DEFAULT 0 COMMENT '周六课程安排'
) COMMENT = '课程信息表';

CREATE TABLE Faculty_Categories (
    StaffID INT NOT NULL COMMENT '员工ID',
    CategoryID VARCHAR(50) NOT NULL COMMENT '类别ID',
    PRIMARY KEY (StaffID, CategoryID)
) COMMENT = '教职员工类别信息表';

CREATE TABLE Faculty_Subjects (
    StaffID INT NOT NULL COMMENT '员工ID',
    SubjectID INT NOT NULL COMMENT '科目ID',
    ProficiencyRating FLOAT DEFAULT 0 COMMENT '专业能力评分',
    PRIMARY KEY (StaffID, SubjectID)
) COMMENT = '教职员工科目信息表';

CREATE TABLE Faculty_Classes (
    ClassID INT NOT NULL COMMENT '课程ID',
    StaffID INT NOT NULL COMMENT '员工ID',
    PRIMARY KEY (ClassID, StaffID)
) COMMENT = '教职员工授课信息表';

CREATE TABLE Student_Schedules (
    StudentID INT NOT NULL COMMENT '学生ID',
    ClassID INT NOT NULL COMMENT '课程ID',
    ClassStatus INT DEFAULT 0 COMMENT '班级状态',
    Grade FLOAT DEFAULT 0 COMMENT '成绩',
    PRIMARY KEY (StudentID, ClassID)
) COMMENT = '学生课程安排信息表';