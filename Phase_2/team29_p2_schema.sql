-- To check with SQLite3, run command: `$ sqlite3 < schema.sql`

CREATE TABLE `User` (
  email varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  nickname varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  PRIMARY KEY (email),
  UNIQUE(nickname),
  FOREIGN KEY (postal_code) REFERENCES Location_Lookup (postal_code)
);

CREATE TABLE Platform (
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (`name`)
);

CREATE TABLE Item (
  lister_email varchar(250) NOT NULL,
  title varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  condition varchar(250) NOT NULL,
  description varchar(250) NULL,
  listing_url varchar(250) NOT NULL,
  PRIMARY KEY (item_no, lister_email),
  FOREIGN KEY (lister_email) REFERENCES `User` (email)
);

CREATE TABLE Item_Collectable_Card_Game (
  lister_email varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  number_of_cards int(16) NOT NULL,
  PRIMARY KEY (item_no, lister_email),
  FOREIGN KEY (item_no) REFERENCES Item (item_no),
  FOREIGN KEY (lister_email) REFERENCES `User` (email)
);

CREATE TABLE Item_Board_Game (
  lister_email varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  PRIMARY KEY (item_no, lister_email),
  FOREIGN KEY (item_no) REFERENCES Item (item_no),
  FOREIGN KEY (lister_email) REFERENCES `User` (email)
);

CREATE TABLE Item_Playing_Card_Game (
  lister_email varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  PRIMARY KEY (item_no, lister_email),
  FOREIGN KEY (item_no) REFERENCES Item (item_no),
  FOREIGN KEY (lister_email) REFERENCES `User` (email)
);

CREATE TABLE Item_Computer_Game (
  lister_email varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  platform varchar(250) NOT NULL,
  PRIMARY KEY (item_no, lister_email),
  FOREIGN KEY (item_no) REFERENCES Item (item_no),
  FOREIGN KEY (lister_email) REFERENCES `User` (email),
  FOREIGN KEY (platform) REFERENCES Platform (`name`)
);

CREATE TABLE Item_Video_Game (
  lister_email varchar(250) NOT NULL,
  item_no int(16) NOT NULL,
  platform varchar(250) NOT NULL,
  media varchar(250) NOT NULL,
  PRIMARY KEY (item_no, lister_email, platform),
  FOREIGN KEY (item_no) REFERENCES Item (item_no),
  FOREIGN KEY (lister_email) REFERENCES `User` (email),
  FOREIGN KEY (platform) REFERENCES Platform (`name`)
);

CREATE TABLE Trade (
  proposer_email varchar(250) NOT NULL,
  counterparty_email varchar(250) NOT NULL,
  proposer_item_no int(16) NOT NULL,
  counterparty_item_no int(16) NOT NULL,
  proposed_date datetime NOT NULL,
  accept_reject_date datetime NULL,
  status varchar(250) NOT NULL,
  trade_history_link varchar(250) NOT NULL,
  auto_trade_id int(16) NOT NULL,
  PRIMARY KEY (proposer_email, counterparty_email, proposer_item_no, counterparty_item_no),
  FOREIGN KEY (proposer_email) REFERENCES `User` (email),
  FOREIGN KEY (counterparty_email) REFERENCES `User` (email),
  FOREIGN KEY (proposer_item_no) REFERENCES Item (item_no),
  FOREIGN KEY (counterparty_item_no) REFERENCES Item (item_no)
);

CREATE TABLE Location_Lookup (
  postal_code varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  latitude float(8) NOT NULL,
  longitude float(8) NOT NULL,
  PRIMARY KEY (postal_code)
  FOREIGN KEY (postal_code) REFERENCES `User` (postal_code)
);

CREATE TABLE Distance_color_lookup (
  distance_lower_range float(8) NOT NULL,
  distance_upper_range float(8) NOT NULL,
  background_color varchar(250) NOT NULL,
  PRIMARY KEY (distance_lower_range, distance_upper_range)
);

CREATE TABLE Response_color_lookup (
  response_lower_range float(8) NOT NULL,
  response_upper_range float(8) NOT NULL,
  text_color varchar(250) NOT NULL,
  PRIMARY KEY (response_lower_range, response_upper_range)
);

CREATE TABLE Rank_lookup (
  trade_lower_range int(16) NOT NULL,
  trade_upper_range int(16) NOT NULL,
  rank_label varchar(250) NOT NULL,
  PRIMARY KEY (trade_lower_range, trade_upper_range)
);