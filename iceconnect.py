from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


class DbConnector:
    def __init__(self):
        self.db_config = read_db_config()
        self.status = ' '
        try:
            self.conn = MySQLConnection(**self.db_config)
            if self.conn.is_connected():
                self.status = 'OK'
            else:
                self.status = 'connection failed.'
        except Error as error:
            self.status = error

    def execute_function(self, func_header=None, argument_list=None):
        cursor = self.conn.cursor()
        try:
            if argument_list:
                func = func_header % argument_list
            else:
                func = func_header
            cursor.execute(func)
            result = cursor.fetchone()
        except Error as e:
            self.status = e
            result = None
        finally:
            cursor.close()
        return result[0]

    def execute_procedure(self, proc_name, argument_list=None):
        result_list = list()
        cursor = self.conn.cursor()
        try:
            if argument_list:
                cursor.callproc(proc_name, argument_list)
            else:
                cursor.callproc(proc_name)
            self.conn.commit()
            for result in cursor.stored_results():
                result_list = [list(elem) for elem in result.fetchall()]
        except Error as e:
            print(e)
            self.status = e
        finally:
            cursor.close()
        return result_list


class PlaceDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_place(self, name, region, population, web, latitude=None, longitude=None):
        new_id = 0
        result = self.execute_procedure('AddPlace', [name, region, population, web, latitude, longitude])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_place(self, place_id):
        result = self.execute_procedure('PlaceInfo', [place_id])
        if result:
            return result[0]
        else:
            return list()

    def get_place_list(self):
        result = self.execute_procedure('PlaceList')
        if result:
            return result
        else:
            return list()

    def update_place(self, place_id, name, region, population, web, coord=None):
        rows_affected = 0
        result = self.execute_procedure('UpdatePlace', [place_id, name, coord, region, population, web])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_place(self, place_id):
        rows_affected = 0
        result = self.execute_procedure('DeletePlace', [place_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def add_place_coordinates(self, place_id, coordinate_id):
        rows_affected = 0
        result = self.execute_procedure('AddPlaceCoordinates', [place_id, coordinate_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def change_place_coordinates(self, place_id, coordinate_id):
        rows_affected = 0
        result = self.execute_procedure('ChangePlaceCoordinates', [place_id, coordinate_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def remove_place_coordinates(self, place_id):
        rows_affected = 0
        result = self.execute_procedure('RemovePlaceCoordinates', [place_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected


class HotelDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_hotel(self, name, address, manager, web, email, phone, dist, lat=None, long=None):
        new_id = 0
        result = self.execute_procedure('AddHotel',
                                        [name, address, lat, long, manager, web, email, phone, dist])
        if result:
            new_id = int(result[0][0])
        return new_id

    def add_hotel_media(self,hotel_id, media_id, media_url):
        number_of_added_rows = 0
        result = self.execute_procedure('AddHotelMedia', [hotel_id, media_id, media_url])
        if result:
            number_of_added_rows = int(result[0][0])
        return number_of_added_rows

    def get_hotel(self, hotel_id):
        result = self.execute_procedure('HotelInfo', [hotel_id])
        if result:
            return result[0]
        else:
            return list()

    def get_hotel_list(self):
        result = self.execute_procedure('HotelList')
        if result:
            return result
        else:
            return list()

    def get_hotel_media_list(self, hotel_id):
        result = self.execute_procedure('HotelMediaList', [hotel_id])
        if result:
            return result
        else:
            return list()

    def update_hotel(self, hotel_id, name, address, manager, web, email, phone, dist, coord=None):
        rows_affected = 0
        result = self.execute_procedure('UpdateHotel',
                                        [hotel_id, name, address, coord, manager, web, email, phone, dist])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def change_hotel_coordinates(self, hotel_id, coordinate_id):
        rows_affected = 0
        result = self.execute_procedure('UpdateHotelCoordinates', [hotel_id, coordinate_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_hotel(self, hotel_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteHotel', [hotel_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def remove_hotel_media(self, hotel_id, media_id):
        rows_affected = 0
        result = self.execute_procedure('RemoveHotelMedia', [hotel_id, media_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected


class RestaurantDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_restaurant(self, name, cusine, capacity, address, manager, web, phone, dist, lat=None, long=None):
        new_id = 0
        result = self.execute_procedure('AddRestaurant',
                                        [name, cusine, capacity, address, lat, long, manager, web, phone, dist])
        if result:
            new_id = int(result[0][0])
        return new_id

    def add_restaurant_media(self, restaurant_id, media_id, media_url):
        new_id = 0
        result = self.execute_procedure('AddRestaurantMedia', [restaurant_id, media_id, media_url])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_restaurant(self, restaurant_id):
        result = self.execute_procedure('RestaurantInfo', [restaurant_id])
        if result:
            return result[0]
        else:
            return list()

    def get_restaurant_list(self):
        result = self.execute_procedure('RestaurantList')
        if result:
            return result
        else:
            return list()

    def get_restaurant_media_list(self, restaurant_id):
        result = self.execute_procedure('RestaurantMediaList', [restaurant_id])
        if result:
            return result
        else:
            return list()

    def update_restaurant(self, r_id, name, cusine, capacity, address, manager, web, phone, dist, coord=None):
        rows_affected = 0
        result = self.execute_procedure('UpdateRestaurant',
                                        [r_id, name, cusine, capacity, address, coord, manager, web, phone, dist])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def change_restaurant_coordinates(self, restaurant_id, coordinate_id):
        pass

    def change_restaurant_district(self, restaurant_id, district_id):
        pass

    def delete_restaurant(self, restaurant_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteRestaurant', [restaurant_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def remove_restaurant_media(self, restaurant_id, media_id):
        rows_affected = 0
        result = self.execute_procedure('RemoveRestaurantMedia', [restaurant_id, media_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected


class ActivityDB(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_activity(self, name, company, web, dist):
        new_id = 0
        result = self.execute_procedure('AddActivity', [name, company, web, dist])
        if result:
            new_id = int(result[0][0])
        return new_id

    def add_activity_media(self, activity_id, media_id, media_url):
        new_id = 0
        result = self.execute_procedure('AddActivityMedia', [activity_id, media_id, media_url])
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_activity(self, activity_id):
        result = self.execute_procedure('ActivityInfo', [activity_id])
        if result:
            return result[0]
        else:
            return list()

    def activity_list(self):
        result = self.execute_procedure('ActivityList')
        if result:
            return result
        else:
            return list()

    def update_activity(self, activity_id, name, company, web, dist):
        rows_affected = 0
        result = self.execute_procedure('UpdateActivity', [activity_id, name, company, web, dist])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_activity(self, activity_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteActivity', [activity_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def remove_activity_media(self, activity_id, media_id):
        rows_affected = 0
        result = self.execute_procedure('RemoveActivityMedia', [activity_id, media_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected


class Utility(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def add_social_media(self, media_name, media_url):
        new_id = 0
        result = self.execute_procedure('AddSocialMedia', (media_name, media_url))
        if result:
            new_id = int(result[0][0])
        return new_id

    def get_social_media(self, media_id):
        result = self.execute_procedure('SocialMediaInfo', [media_id])
        return_list = [list(elem) for elem in result]
        return return_list

    def social_media_list(self):
        result = self.execute_procedure('SocialMediaList')
        return_list = [list(elem) for elem in result]
        return return_list

    def update_social_media(self, media_id, media_name, media_url):
        rows_affected = 0
        result = self.execute_procedure('UpdateSocialMedia', (media_id, media_name, media_url))
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delete_social_media(self, media_id):
        rows_affected = 0
        result = self.execute_procedure('DeleteSocialMedia', [media_id])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def add_coordinates(self, latitude, longitude):
        new_id = 0
        result = self.execute_procedure('AddCoordinates', [latitude, longitude])
        if result:
            new_id = int(result[0][0])
        return new_id

    def total_number_of_hotels(self):
        return self.execute_function('select TotalNumberOfHotels()')

    def number_of_hotels_by_district(self, district_id):
        return self.execute_function('select NumberOfDistrictHotels(%d)', district_id)
