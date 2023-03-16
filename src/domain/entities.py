import datetime

class Movie :
    """"
    Movie class defines the data type movie, which has an id and a title, a description and a genre attribute
    """
    def __init__(self, movie_id, title, description, genre):
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__genre = genre

    def get_movie_id(self):
        return self.__movie_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def set_description(self, new_description):
        self.__description = new_description

    def get_genre(self):
        return self.__genre

    def set_genre(self, new_genre):
        self.__genre = new_genre

    def __eq__(self, other):
        return str(self.__movie_id) == str(other.__movie_id) and str(self.__title) == str(other.__title) and str(self.__description) == str(other.__description) and str(self.__genre) == str(other.__genre)

class Client :
    """"
    Client class defines the data type client, which has an id and a name attribute
    """
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    def get_client_id(self):
        return self.__client_id

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name

    def __eq__(self, other):
        return str(self.__client_id) == str(other.__client_id) and str(self.__name) == str(other.__name)


class Rental :
    def __init__(self, rental_id, client_id, movie_id, rented_date, due_date, returned_date):
        self.__rental_id = rental_id
        self.__client_id = client_id
        self.__movie_id = movie_id
        self.__rented_date = rented_date
        self.__due_date = due_date
        self.__returned_date = returned_date

    def get_rental_id(self):
        return self.__rental_id

    def get_client_id(self):
        return self.__client_id

    def get_movie_id(self):
        return self.__movie_id

    def get_rented_date(self):
        return self.__rented_date

    def get_due_date(self):
        return self.__due_date

    def get_returned_date(self):
        return self.__returned_date

    def set_returned_date(self, new_date):
        self.__returned_date = new_date

    def get_return_delay(self):
        if self.__returned_date == datetime.date.min and datetime.date.today() > self.__due_date:
            return (datetime.date.today() - self.__due_date).days
        else:
            # return datetime.date.today() - datetime.date.today()
            return 0

    def get_rented_days(self):
        """"
        returns: the number of days for which the movie corresponding to the given rental was/has been rented
                -timedelta type
        """
        if self.__returned_date != datetime.date.min:
            return (self.__returned_date - self.__rented_date).days
        else:
            return (datetime.date.today()-self.__rented_date).days

    def __eq__(self, other):
        return self.__rental_id == other.__rental_id and self.__client_id == other.__client_id and self.__movie_id == other.__movie_id and self.__rented_date == other.__rented_date and self.__due_date == other.__due_date and self.__returned_date == other.__returned_date