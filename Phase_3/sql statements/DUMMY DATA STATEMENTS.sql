USE `TradePlaza`;

#User
INSERT INTO USER VALUES ('ngardner9@gatech.edu', 'cs6400', 'Nathan', 'Gardner', 'Nate', '30363');
INSERT INTO USER VALUES ('cagim3@gatech.edu', 'cs6400', 'Chisom', 'Agim', 'Jane', '30354');
INSERT INTO USER VALUES ('ctsai97@gatech.edu', 'cs6400', 'Chin-Po', 'Tsai', 'Chin', '30364');
INSERT INTO USER VALUES ('mlukacsko3@gatech.edu', 'cs6400', 'Michael', 'Lukacsko', 'Mike', '30370');
INSERT INTO USER VALUES ('ebentivegna3@gatech.edu', 'cs6400', 'Elaine', 'Bentivegna', 'El', '63530');


#Item
INSERT INTO Item VALUES ('ngardner9@gatech.edu', 'Uno', '1', 'Heavily Used', 'The classic card game');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Monopoly', '2', 'Like New', 'A classic multiplayer economics game');
INSERT INTO Item VALUES ('ctsai97@gatech.edu', 'Mario Kart', '3', 'Lightly Used', 'Racing game for Nintendo');
INSERT INTO Item VALUES ('mlukacsko3@gatech.edu', 'Age of Empires II', '4', 'Damaged/Missing Parts', 'RTS game for PC');
INSERT INTO Item VALUES ('ebentivegna3@gatech.edu', 'Clue', '5', 'Moderately Used', 'Classic mysteryboard game');
INSERT INTO Item VALUES ('ngardner9@gatech.edu', 'Exploding Kittens', '6', 'Unopened', 'A Russian roulette card game');

INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Snakes', '7', 'Lightly Used', 'A classic snakey game');
INSERT INTO Item VALUES ('ebentivegna3@gatech.edu', 'Ludo', '8', 'Like New', 'A classic boring game');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Ladders', '9', 'Like New', 'A classic laddery game');
INSERT INTO Item VALUES ('mlukacsko3@gatech.edu', 'Taboo', '10', 'Lightly Used', 'A classic taboo-ey game');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Pokemon', '11', 'Unopened', 'A boring creature-card-collecting game');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Avatar: The Last Airbender', '12', 'Heavily Used', 'A classic and timeless card-collecting game from the most well-made series, animated or otherwise, to ever exist');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Skyrim', '13', 'Damaged/Missing Parts', 'The single most wonderful PC game to ever grace our video game history');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Uno', '14', 'Moderately Used', 'A pretty cool card game.');
INSERT INTO Item VALUES ('cagim3@gatech.edu', 'Detroit: Become Human', '15', 'Heavily Used', 'Idk...What can I say, it is a pretty nuanced game.');


##Item Subsets
#Item_Board_Game
INSERT INTO Item_Board_Game VALUES ('cagim3@gatech.edu', '2');
INSERT INTO Item_Board_Game VALUES ('ebentivegna3@gatech.edu', '5');

INSERT INTO Item_Board_Game VALUES ('cagim3@gatech.edu', '7');
INSERT INTO Item_Board_Game VALUES ('ebentivegna3@gatech.edu', '8');
INSERT INTO Item_Board_Game VALUES ('mlukacsko3@gatech.edu', '9');
INSERT INTO Item_Board_Game VALUES ('cagim3@gatech.edu', '10');


#Item_Collectable_Card_Game
INSERT INTO Item_Collectable_Card_Game VALUES ('cagim3@gatech.edu', '11', '10');
INSERT INTO Item_Collectable_Card_Game VALUES ('cagim3@gatech.edu', '12', '492');


#Item_Playing_Card_Game
INSERT INTO Item_Playing_Card_Game VALUES ('ngardner9@gatech.edu', '1');
INSERT INTO Item_Playing_Card_Game VALUES ('ngardner9@gatech.edu', '6');

INSERT INTO Item_Playing_Card_Game VALUES ('cagim3@gatech.edu', '14');


#Item_Computer_Game
INSERT INTO Item_Computer_Game VALUES ('mlukacsko3@gatech.edu', '4', 'Windows');

INSERT INTO Item_Computer_Game VALUES ('cagim3@gatech.edu', '13', 'Windows');


#Item_Video_Game
INSERT INTO Item_Video_Game VALUES ('ctsai97@gatech.edu', '3', 'Nintendo', 'Game Card');
INSERT INTO Item_Video_Game VALUES ('cagim3@gatech.edu', '15', 'PlayStation', 'Optical Disc');


#Trade auto_trade_id:, 'proposer_email+{}+counterparty_email+{}+desired_item_no+{}+proposer_item_no+{}'
INSERT INTO Trade VALUES ('ngardner9@gatech.edu', 'ebentivegna3@gatech.edu', '1', '5', '2022-07-11 08:45:32', NULL, 'Unaccepted', 'proposer_email+ngardner9@gatech.edu+counterparty_email+ebentivegna3@gatech.edu+desired_item_no+5+proposer_item_no+1');
INSERT INTO Trade VALUES ('ngardner9@gatech.edu', 'cagim3@gatech.edu', '1', '2', '2022-07-12 00:00:00', NULL, 'Unaccepted', 'proposer_email+ngardner9@gatech.edu+counterparty_email+cagim3@gatech.edu+desired_item_no+2+proposer_item_no+1');
INSERT INTO Trade VALUES ('mlukacsko3@gatech.edu', 'ctsai97@gatech.edu', '4', '3', '2022-07-10 00:00:00', '2022-07-10 00:00:00', 'Accepted', 'proposer_email+mlukacsko3@gatech.edu+counterparty_email+ctsai97@gatech.edu+desired_item_no+3+proposer_item_no+4');
INSERT INTO Trade VALUES ('ngardner9@gatech.edu', 'mlukacsko3@gatech.edu', '6', '4', '2022-07-09 00:00:00', '2022-07-09 00:00:00', 'Accepted', 'proposer_email+ngardner9@gatech.edu+counterparty_email+mlukacsko3@gatech.edu+desired_item_no+4+proposer_item_no+6');

INSERT INTO Trade VALUES ('cagim3@gatech.edu', 'ebentivegna3@gatech.edu', '7', '8', '2022-07-08 00:00:00', '2022-07-13 00:00:00', 'Accepted', 'proposer_email+cagim3@gatech.edu+counterparty_email+ebentivegna3@gatech.edu+desired_item_no+8+proposer_item_no+7');
