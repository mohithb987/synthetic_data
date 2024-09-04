DROP TABLE Client;
CREATE TABLE Client (
    Client_num INTEGER PRIMARY KEY,
    Customer_name VARCHAR(100),
    Customer_age INT,
    Gender VARCHAR(10),
    Dependent_count INT,
    Education_Level VARCHAR(20),
    Marital_status VARCHAR(20),
    Income_category VARCHAR(20),
    Email VARCHAR(100),
    Contact_number VARCHAR(20)
);

SELECT * FROM client limit 10;
DROP TABLE Bank;
CREATE TABLE Bank (
 BankID INTEGER PRIMARY KEY,
 Name VARCHAR,
 BranchName VARCHAR,
 RoutingNumber VARCHAR
);

SELECT * FROM Bank;

DROP TABLE creditcard;
CREATE TABLE creditcard (
    CardNumber BIGINT PRIMARY KEY,
    BankID INTEGER,
    Client_num INTEGER,
    Card_category VARCHAR(20),
    Credit_limit DECIMAL(10, 2),
    Avg_utilization_ratio DECIMAL(5, 2),
    Total_revolving_balance DECIMAL(10, 2),
    Open_to_buy DECIMAL(10, 2),
    Card_Status VARCHAR(10),
    Expiry_Date DATE,
    Credit_score INTEGER,
    FOREIGN KEY (BankID) REFERENCES bank (BankID),
    FOREIGN KEY (Client_num) REFERENCES client (Client_num)
);

select * from creditcard limit 10;

DROP TABLE Merchant;
CREATE TABLE Merchant (
 MerchantID INTEGER PRIMARY KEY,
 Name VARCHAR,
 Category VARCHAR,
 Location VARCHAR
)

DROP TABLE Transaction ;
CREATE TABLE Transaction (
                             TransactionID INTEGER PRIMARY KEY,
                             CardNumber BIGINT,
                             MerchantID INTEGER,
                             Transaction_amt DECIMAL(10, 2),
                             Transaction_time TIMESTAMP,
                             FOREIGN KEY (CardNumber) REFERENCES CreditCard(CardNumber),
                             FOREIGN KEY (MerchantID) REFERENCES Merchant(MerchantID)
);



Create Table CommunicationPreference (
                                         PreferenceID INTEGER PRIMARY KEY,
                                         Client_num INTEGER,
                                         PreferenceType VARCHAR,
                                         EmailSubscription BOOLEAN,
                                         SMSSubscription BOOLEAN,
                                         PhoneCallSubscription BOOLEAN,
                                         FOREIGN KEY (Client_num) REFERENCES Client(Client_num)
)


select * from CommunicationPreference limit 10;


CREATE TABLE CustomerSupport (
 SupportTicketID INTEGER PRIMARY KEY,
 Client_num INTEGER,
 IssueType VARCHAR,
 Status VARCHAR,
 SupportTicket_date TIMESTAMP,
 Assigned_to VARCHAR,
 FOREIGN KEY (Client_num) REFERENCES Client (Client_num)
)


CREATE TABLE AccountInformation (
                                    AccountNo INTEGER PRIMARY KEY,
                                    Client_num INTEGER,
                                    BankID INTEGER,
                                    AccountType VARCHAR,
                                    Balance DECIMAL,
                                    Open_date TIMESTAMP,
                                    Close_date TIMESTAMP,
                                    Overdraft_limit DECIMAL,
                                    FOREIGN KEY (Client_num) REFERENCES Client(Client_num),
                                    FOREIGN KEY (BankID) REFERENCES Bank(BankID)
)

CREATE TABLE Rewards (
                         RewardID INTEGER PRIMARY KEY,
                         CardNumber BIGINT,
                         Reward_points_balance INTEGER,
                         Reward_points_consumed INTEGER,
                         ExpiryDate TIMESTAMP,
                         FOREIGN KEY (CardNumber) REFERENCES CreditCard(CardNumber)
);

DROP TABLE PolicyTypes;
CREATE TABLE PolicyTypes (
 PolicyType VARCHAR PRIMARY KEY,
 Coverage_amount DECIMAL,
 Premium_amount DECIMAL
)

CREATE TABLE InsurancePolicy (
                                 PolicyID INTEGER PRIMARY KEY,
                                 CardNumber BIGINT,
                                 PolicyType VARCHAR,
                                 Policy_start_date TIMESTAMP,
                                 Policy_end_date TIMESTAMP,
                                 FOREIGN KEY (CardNumber) REFERENCES
                                     CreditCard(CardNumber)
)
