from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from math import sin, cos, sqrt, atan2, radians
import csv


# >>> This function is already replaced by SQL query, leave it here just for testing
def calculate_distance_between_postal_code(lat1, lon1, lat2, lon2):
    '''
    Calculate the distance between two different postal_code.
    Code reference: reference: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    '''
    R = 3958.75 # approximate radius of earth (miles)

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    print("Result (miles):", distance)
    return distance


def get_text_color_from_response_time(cursor, conn,avg_response):
    '''
    Get text color from avg response time:
    -1   -   -1: black
    0    -    7: green
    7.1  -   14: yellow
    14.1 - 20.9: orange
    21   - 27.9: red
    > 28       : bolded red
    '''
    color = "black"
    response_lower_range = -1
    response_upper_range = -1
    if (avg_response == "None"):
        response_lower_range = -1
        response_upper_range = -1
    elif (0 <= avg_response and avg_response <= 7):
        response_lower_range = 0
        response_upper_range = 7
    elif (7.1 <= avg_response and avg_response <= 14):
        response_lower_range = 7.1
        response_upper_range = 14
    elif (14.1 <= avg_response and avg_response <= 20.9):
        response_lower_range = 14.1
        response_upper_range = 20.9
    elif (21 <= avg_response and avg_response <= 27.9):
        response_lower_range = 21
        response_upper_range = 27.9
    elif (28 <= avg_response):
        response_lower_range = 28
        response_upper_range = 10000
    else:
        print("Error, avg_response has invalid value, use color black as the default")

    try:
        # >>> query SQL
        cmd = "SELECT text_color FROM Response_color_lookup WHERE ABS(response_lower_range-{}) < 0.0001 AND ABS(response_upper_range - {}) < 0.0001;".format(response_lower_range, response_upper_range)
        # print("[Debug/get_text_color_from_response_time] about to run cmd: ", cmd)
        cursor.execute(cmd)
        row = cursor.fetchone()
        color = row[0]
        # print("color: ", color)
        return color
    except:
        return color

def get_color_from_distance(cursor, conn, distance):
    '''
    Get color from distance:
    0-25   : green
    25-50  : yellow
    50-100 : orange
    > 100  : red
    '''
    distance_lower_range = 0
    distance_upper_range = 0
    color = 'green'
    if (0 <= distance and distance <= 25):
        distance_lower_range = 0
        distance_upper_range = 25
    elif (25 < distance and distance <= 50):
        distance_lower_range = 25
        distance_upper_range = 50
    elif (50 < distance and distance <= 100):
        distance_lower_range = 50
        distance_upper_range = 100
    elif (100 < distance):
        distance_lower_range = 100
        distance_upper_range = 10000
    else:
        print("[Debug/get_color_from_distance] Error! You have an invalid distance!")
    
    try:
        # >>> query SQL
        cmd = "SELECT background_color FROM Distance_color_lookup WHERE distance_lower_range = {} AND distance_upper_range = {};".format(distance_lower_range, distance_upper_range)
        # print("[Debug/get_color_from_distance] about to run cmd: ", cmd)
        cursor.execute(cmd)
        row = cursor.fetchone()
        color = row[0]
        # print("color: ", color)
    except:
        print("[Debug/get_color_from_distance] Your color query has issues! Return default color now")
    return color

# >>> Show results
def show_all_tables(cursor, conn):
    print("-----> Show All Tables:")
    sql_query = """SHOW TABLES;"""
    cursor.execute(sql_query)
    for element in cursor.fetchall():
        print(element)
    print("\n\n")


def show_rows_in_table(cursor, conn, table_name):
    '''
    Show every rows within the given table
    '''
    cmd = "SELECT * FROM {}".format(table_name)
    print("[Debug/show_rows_in_table] about to run cmd: ", cmd)
    cursor.execute(cmd)
    for element in cursor.fetchall():
        print(element)


def remove_row_from_table():
    pass

def insert_row_into_table(cursor, conn, table_name, parameters):
    if (table_name == "User"):
        try:
            # cmd = """INSERT INTO User (email, first_name, last_name, nickname) VALUES ('chinpo.tsai17@gmail.com', 'Chin-Po', 'Tsai', 'cpt')"""
            cmd = "INSERT IGNORE INTO {} (email, password, first_name, last_name, nickname, postal_code) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(table_name, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5])
            print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
            cursor.execute(cmd)
            conn.commit()
            print("Inserted successfully")
        except:
            print("Error, insert failed")
    elif (table_name == "Item"):
        try:
            cmd = "INSERT IGNORE INTO {} (lister_email, title, item_no, condition, description) VALUES ('{}', '{}', {}, '{}', '{}');".format(table_name, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
            print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
            cursor.execute(cmd)
            conn.commit()
            print("Inserted successfully")
        except:
            print("Error, insert failed")
    elif (table_name == "Location_Lookup"):
        try:
            cmd = "INSERT IGNORE INTO {} (postal_code, city, state, latitude, longitude) VALUES ('{}', '{}', '{}', {}, {});".format(table_name, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
            print("lat: ", parameters[3])
            print("lon: ", parameters[4])
            print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
            cursor.execute(cmd)
            conn.commit()
            print("Inserted successfully")
        except:
            print("Error, insert failed")
    elif (table_name == "Distance_color_lookup"):
        try:
            cmd = "INSERT IGNORE INTO {} (distance_lower_range, distance_upper_range, background_color) VALUES ({}, {}, '{}');".format(table_name, parameters[0], parameters[1], parameters[2])
            print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
            cursor.execute(cmd)
            conn.commit()
            print("Inserted successfully")
        except:
            print("Error, insert failed")
    elif (table_name == "rank_lookup"):
        try:
            cmd = "INSERT IGNORE INTO {} (trade_lower_range, trade_upper_range, rank_label) VALUES ({}, {}, '{}');".format(table_name, parameters[0], parameters[1], parameters[2])
            # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
            cursor.execute(cmd)
            conn.commit()
            print("Inserted successfully")
        except:
            print("Error, insert failed")
    elif (table_name == "trade"):
        cmd = """INSERT IGNORE INTO {} (proposer_email, 
                                        counterparty_email, 
                                        proposer_item_no, 
                                        counterparty_item_no, 
                                        proposed_date, 
                                        accept_reject_date, 
                                        status, 
                                        auto_trade_id) VALUES ('{}', '{}', {}, {}, '{}', '{}', '{}', '{}');
                """.format(table_name, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], parameters[7])
        print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
        cursor.execute(cmd)
        conn.commit()
        print("Inserted successfully")

    elif (table_name == "Response_color_lookup"):
        cmd = """INSERT IGNORE INTO {} (response_lower_range, 
                                        response_upper_range, 
                                        text_color
                                        ) VALUES ({}, {}, '{}');
                """.format(table_name, parameters[0], parameters[1], parameters[2])
        print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
        cursor.execute(cmd)
        conn.commit()
        print("Inserted successfully")
    else:
        print("Error, the table name is not defined")


def remove_table(cursor, conn, table_name):
    try:
        cmd = "DROP TABLE {};".format(table_name)
        print("[Debug/remove_table] about to run cmd: ", cmd)
        cursor.execute(cmd)
        conn.commit()
        print("[Debug/remove_table] command succeeded!")
    except:
        print("[Debug/remove_table] Error, command failed")


def import_file_to_table(cursor, conn, table_name, file_path):
    '''
    Load file to table.
    '''
    print("file_path: ", file_path)


    with open(file_path) as csv_file:
        if (table_name == "Item"): # the cvs file (Items_All.csv) is separated by \t, need to handle it separately
            csv_reader = csv.reader(csv_file, delimiter='\t')
        else:
            csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count == 1:  # title
                print(f'Titles are {", ".join(row)}\n')
            else:                # real content
                line_count += 1

                # >>> insert into different tables
                if (table_name == "User"):
                    cmd = "INSERT IGNORE INTO {} (email, password, first_name, last_name, nickname, postal_code) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(table_name, row[0], row[1], row[2], row[3], row[4], row[5])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                    # print("Inserted successfully")
                elif (table_name == "Item"):
                    # print("row: ", row)

                    # >>> Handle the NULL case
                    # if (row[3] == ""):
                    #     row[3] = "Empty"
                    # if (row[6] == ""):
                    #     row[6] = "0"
                    # if (row[7] == ""):
                    #     row[7] = "Empty"
                    # if (row[8] == ""):
                    #     row[8] = "Empty"

                    # print("row[0]: ", row[0])
                    # print("row[1]: ", row[1])
                    # print("row[2]: ", row[2])
                    # print("row[3]: ", row[3])
                    # print("row[4]: ", row[4])
                    # print("row[5]: ", row[5])
                    # print("row[6]: ", row[6])
                    # print("row[7]: ", row[7])
                    # print("row[8]: ", row[8])

                    try:
                        # cmd = "INSERT IGNORE INTO {} (item_number, title, condition, description, email, type, card_count, platform, media) VALUES ({}, '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}');".format(table_name, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                        cmd = "INSERT IGNORE INTO {} (lister_email, title, item_no, `condition`, description) VALUES ('{}', '{}', {}, '{}', '{}');".format(table_name, row[4], row[1], row[0], row[2], row[3])

                        # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                        cursor.execute(cmd)
                        conn.commit()
                    except:
                        pass
                        # print("[Debug/insert_row_into_table] FAILED at running cmd: ", cmd) # TODO: fix it
                elif (table_name == "Location_Lookup"):
                    try:
                        cmd = "INSERT IGNORE INTO {} (postal_code, city, state, latitude, longitude) VALUES ('{}', '{}', '{}', {}, {});".format(table_name, row[0], row[1], row[2], row[3], row[4])
                        # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                        cursor.execute(cmd)
                        conn.commit()
                        # print("Inserted successfully")
                    except:
                        pass
                        # print("Error, cmd: ", cmd) # TODO: fix it
                elif (table_name == "Item_Board_Game"):
                    cmd = "INSERT IGNORE INTO {} (lister_email,item_no) VALUES ('{}', {});".format(table_name, row[1], row[0])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                elif (table_name == "Item_Playing_Card_Game"):
                    cmd = "INSERT IGNORE INTO {} (lister_email,item_no) VALUES ('{}', {});".format(table_name, row[1], row[0])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                elif (table_name == "Item_Collectable_Card_Game"):
                    cmd = "INSERT IGNORE INTO {} (lister_email,item_no, number_of_cards) VALUES ('{}', {}, {});".format(table_name, row[1], row[0], row[2])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                elif (table_name == "Item_Computer_Game"):
                    cmd = "INSERT IGNORE INTO {} (lister_email,item_no, platform) VALUES ('{}', {}, '{}');".format(table_name, row[1], row[0], row[2])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                elif (table_name == "Item_Video_Game"):
                    cmd = "INSERT IGNORE INTO {} (lister_email,item_no, platform, media) VALUES ('{}', {}, '{}', '{}');".format(table_name, row[1], row[0], row[2], row[3])
                    # print("[Debug/insert_row_into_table] about to run cmd: ", cmd)
                    cursor.execute(cmd)
                    conn.commit()
                else:
                    print("Error, something wrong with the table name")

            # if (line_count <= 10 and line_count != 1):
            #     print("row: ", row)
    # print("Finished importing file to table: ", table_name)


# INSERT IGNORE INTO Item (item_number, title, condition, description, email, type, card_count, platform, media) VALUES (1, 'The New Tetris', 'Like New', 'H2O Entertainment   ', 'usr001@gt.edu', 'Video Game', , 'Nintendo', 'Optical disc');



def create_tables(cursor, conn):

    cmd = """CREATE TABLE IF NOT EXISTS User (
                email VARCHAR(250) NOT NULL, 
                password VARCHAR(250) NOT NULL,
                first_name VARCHAR(250) NOT NULL, 
                last_name VARCHAR(250) NOT NULL, 
                nickname VARCHAR(250) NOT NULL,
                postal_code VARCHAR(250) NOT NULL,
                PRIMARY KEY (email)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "User", "./sample_data/Users.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Item (
                    lister_email VARCHAR(250) NOT NULL,
                    title VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    `condition`  VARCHAR(250) NOT NULL,
                    description VARCHAR(250) NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item", "./sample_data/Items_All.csv")

    cmd = """CREATE TABLE IF NOT EXISTS Item_Board_Game (
                    lister_email VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item_Board_Game", "./sample_data/Items_board_game.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Item_Playing_Card_Game (
                    lister_email VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item_Playing_Card_Game", "./sample_data/items_playing_card_game.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Item_Collectable_Card_Game (
                    lister_email VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    number_of_cards INT(16) NOT NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item_Collectable_Card_Game", "./sample_data/Items_collectible_card_game.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Item_Computer_Game (
                    lister_email VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    platform VARCHAR(250) NOT NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item_Computer_Game", "./sample_data/items_computer_game.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Item_Video_Game (
                    lister_email VARCHAR(250) NOT NULL,
                    item_no int(16) NOT NULL,
                    platform VARCHAR(250) NOT NULL,
                    media VARCHAR(250) NOT NULL,
                    PRIMARY KEY (item_no, lister_email)
                );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Item_Video_Game", "./sample_data/item_video_game.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Location_Lookup (
                postal_code VARCHAR(250) NOT NULL,
                city VARCHAR(250) NOT NULL,
                state VARCHAR(250) NOT NULL,
                latitude Decimal(8,6) NOT NULL,
                longitude Decimal(9,6) NULL,
                PRIMARY KEY (postal_code)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    import_file_to_table(cursor, conn, "Location_Lookup", "./sample_data/postal_codes.csv")


    cmd = """CREATE TABLE IF NOT EXISTS Distance_color_lookup (
                distance_lower_range FLOAT(8) NOT NULL,
                distance_upper_range FLOAT(8) NOT NULL,
                background_color VARCHAR(250) NOT NULL,
                PRIMARY KEY (distance_lower_range, distance_upper_range)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()


    cmd = """CREATE TABLE IF NOT EXISTS Trade (
                proposer_email VARCHAR(250) NOT NULL,
                counterparty_email varchar(250) NOT NULL,
                proposer_item_no INT(16) NOT NULL, 
                counterparty_item_no INT(16) NOT NULL,
                proposed_date DATETIME NOT NULL,
                accept_reject_date DATETIME NULL,
                status VARCHAR(250) NOT NULL, 
                auto_trade_id VARCHAR(250) NOT NULL,
                PRIMARY KEY (proposer_email, counterparty_email, proposer_item_no, counterparty_item_no)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    insert_row_into_table(cursor, conn, "trade", ['usr002@gt.edu', 'usr003@gt.edu', '4', '10', '2022-11-30 23:59:59.997', '2022-12-12 23:59:59.997', 'accepted', 'proposer_email+usr002@gt.edu+counterparty_email+usr003@gt.edu+proposer_item_no+4+counterparty_item_no+10'])
    insert_row_into_table(cursor, conn, "trade", ['usr002@gt.edu', 'usr003@gt.edu', '5', '11', '2022-12-11 23:59:59.997', '2022-12-16 23:59:59.997', 'accepted', 'proposer_email+usr002@gt.edu+counterparty_email+usr003@gt.edu+proposer_item_no+5+counterparty_item_no+11'])
    insert_row_into_table(cursor, conn, "trade", ['usr002@gt.edu', 'usr003@gt.edu', '6', '12', '2022-12-12 23:59:59.997', '2022-12-16 23:59:59.997', 'accepted', 'proposer_email+usr002@gt.edu+counterparty_email+usr003@gt.edu+proposer_item_no+6+counterparty_item_no+12'])
    insert_row_into_table(cursor, conn, "trade", ['usr002@gt.edu', 'usr003@gt.edu', '7', '13', '2022-12-13 23:59:59.997', '2022-12-16 23:59:59.997', 'unaccepted', 'proposer_email+usr002@gt.edu+counterparty_email+usr003@gt.edu+proposer_item_no+7+counterparty_item_no+13'])
    insert_row_into_table(cursor, conn, "trade", ['usr001@gt.edu', 'usr002@gt.edu', '1', '8', '2022-12-14 23:59:59.997', '2022-12-25 23:59:59.997', 'unaccepted', 'proposer_email+usr001@gt.edu+counterparty_email+usr002@gt.edu+proposer_item_no+1+counterparty_item_no+8'])
    insert_row_into_table(cursor, conn, "trade", ['usr001@gt.edu', 'usr002@gt.edu', '2', '9', '2022-12-14 23:59:59.997', '2022-12-24 23:59:59.997', 'unaccepted', 'proposer_email+usr001@gt.edu+counterparty_email+usr002@gt.edu+proposer_item_no+2+counterparty_item_no+9'])



    cmd = """CREATE TABLE IF NOT EXISTS Response_color_lookup (
                response_lower_range FLOAT(8) NOT NULL, 
                response_upper_range FLOAT(8) NOT NULL,
                text_color VARCHAR(250) NOT NULL, 
                PRIMARY KEY (response_lower_range, response_upper_range)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['-1', '-1', 'black'])
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['0', '7', 'green'])
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['7.1', '14', 'yellow'])
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['14.1', '20.9', 'orange'])
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['21', '27.9', 'red'])
    insert_row_into_table(cursor, conn, "Response_color_lookup", ['28', '10000', 'bolded_red'])



    cmd = """CREATE TABLE IF NOT EXISTS rank_lookup (
                trade_lower_range INT(16) NOT NULL,
                trade_upper_range INT(16) NOT NULL,
                rank_label VARCHAR(250) NOT NULL,
                PRIMARY KEY (trade_lower_range, trade_upper_range)
            );"""
    # print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    insert_row_into_table(cursor, conn, "rank_lookup", [0, 0, 'none'])
    insert_row_into_table(cursor, conn, "rank_lookup", [1, 2, 'Aluminium'])
    insert_row_into_table(cursor, conn, "rank_lookup", [3, 3, 'Bronze'])
    insert_row_into_table(cursor, conn, "rank_lookup", [4, 5, 'Silver'])
    insert_row_into_table(cursor, conn, "rank_lookup", [6, 7, 'Gold'])
    insert_row_into_table(cursor, conn, "rank_lookup", [8, 9, 'Platinum'])
    insert_row_into_table(cursor, conn, "rank_lookup", [10, 10000, 'Alexandinium'])



    cmd = """CREATE TABLE IF NOT EXISTS platform (
                name VARCHAR(250) NOT NULL,
                friendly_platform_name VARCHAR(250) NOT NULL,
                PRIMARY KEY (name, friendly_platform_name)
            );"""
    print("[Debug/create_tables] about to run cmd: ", cmd)
    cursor.execute(cmd)
    conn.commit()
    # insert elements
    cmd = "INSERT IGNORE INTO {} (name, friendly_platform_name) VALUES ('{}', '{}');".format("platform", "nintendo", "NINTENDO")
    cursor.execute(cmd)
    conn.commit()
    cmd = "INSERT IGNORE INTO {} (name, friendly_platform_name) VALUES ('{}', '{}');".format("platform", "playstation", "PLAYSTATION")
    cursor.execute(cmd)
    conn.commit()
    cmd = "INSERT IGNORE INTO {} (name, friendly_platform_name) VALUES ('{}', '{}');".format("platform", "xbox", "XBOX")
    cursor.execute(cmd)
    conn.commit()





######################################### INITIALIZE YOUR SQL DATABASE BELOW #########################################


app = Flask(__name__)

mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'tradeplaza'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

if __name__ == "__main__":
    create_tables(cursor, conn)

    # show_all_tables(cursor, conn)

    # insert_row_into_table(cursor, conn, "Distance_color_lookup", [0, 25, 'green'])
    # insert_row_into_table(cursor, conn, "Distance_color_lookup", [25, 50, 'yellow'])
    # insert_row_into_table(cursor, conn, "Distance_color_lookup", [50, 100, 'orange'])
    # insert_row_into_table(cursor, conn, "Distance_color_lookup", [100, 10000, 'red'])


    # show_rows_in_table(cursor, conn, "User")

    # remove_table(cursor, conn, "User")

    # conn.close() # TODO:
    # cursor.close() # TODO: