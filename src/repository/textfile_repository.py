import datetime
from src.repository.repositories import RepoMovie, RepoClient, RepoRental
from src.domain.entities import Movie, Client, Rental


class TextFileRepoMovie(RepoMovie):

    def __init__(self, file_name):
        """"
        The super() function is used to give access to methods and properties of a parent or sibling class.
        The super() function returns an object that represents the parent class.
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        with open(self._file_name, "rt") as f:
            """"
            rt : r - read mode
                 t - text
            readlines() : Reads all the lines and return them as each line a string element in a list.
            """
            self._movies.clear()
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    movie_id, title, description, genre = line.split(',', 3)
                    movie_id = movie_id.strip()
                    title = title.strip()
                    description = description.strip()
                    genre = genre.strip()
                    movie = Movie(movie_id, title, description, genre)
                    self._movies.append(movie)

    def _save_file(self):
        with open(self._file_name, "wt") as f:
            """"
            rt : r - read mode
                 t - text
            write() : Inserts the string str1 in a single line in the text file.
            """
            for movie in self._movies:
                f.write(str(movie.get_movie_id()) + ', ' + str(movie.get_title()) + ', ' + str(movie.get_description()) + ', ' + str(movie.get_genre()) +'\n')

    def _update_file(self, movie):
        with open(self._file_name, "at") as f:
            f.write(str(movie.get_movie_id()) + ', ' + str(movie.get_title()) + ', ' + str(movie.get_description()) + ', ' + str(movie.get_genre()) +'\n')

    def add_movie(self, movie):
        """
        1. Do whatever the add method in the base class does
        2. Save the ingredients to file
        """
        super(TextFileRepoMovie, self).add_movie(movie)
        self._update_file(movie)

    def remove_movie(self, movie_id):
        super().remove_movie(movie_id)
        self._save_file()

    def search_movie_by_id(self, movie_id):
        return super().search_movie_by_id(movie_id)
        #same as : return RepoMovie.search_movie_by_id(self, movie_id)

    def update_movie(self, movie_id, attribute, new_value):
        super(). update_movie(movie_id, attribute, new_value)
        self._save_file()

    def get_all_movies(self):
        return super().get_all_movies()

    def search_movie(self, string_movie):
        return super().search_movie(string_movie)

    def __len__(self):
        return super().__len__()


class TextFileRepoClient(RepoClient):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        self._clients.clear()
        with open(self._file_name, "rt") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    client_id, name = line.split(',', 1)
                    client_id = client_id.strip()
                    name = name.strip()
                    client = Client(client_id, name)
                    self._clients.append(client)

    def _save_file(self):
        with open(self._file_name, "wt") as f:
            for client in self._clients:
                f.write(str(client.get_client_id()) + ', ' + str(client.get_name()) + '\n')

    def _update_file(self ,client):
        with open(self._file_name, "at") as f:
            f.write(str(client.get_client_id()) + ', ' + str(client.get_name()) + '\n')

    def add_client(self, client):
        super().add_client(client)
        self._update_file(client)

    def remove_client(self, client_id):
        super(TextFileRepoClient, self).remove_client(client_id)
        self._save_file()

    def search_client_by_id(self, client_id):
        return super(TextFileRepoClient, self).search_client_by_id(client_id)
        #this format is generated upon pressing 'enter' after having written the word 'super'
        #but is same with 'return super().search_client_by_id(client_id)'

    def update_client(self, client_id, new_value):
        super(TextFileRepoClient, self).update_client(client_id, new_value)
        self._save_file()

    def get_all_clients(self):
        return super(TextFileRepoClient, self).get_all_clients()

    def search_client(self, string_client):
        return super(TextFileRepoClient, self).search_client(string_client)

    def __len__(self):
        return super(TextFileRepoClient, self).__len__()



class TextFileRepoRental(RepoRental):

    def __init__(self, file_name, txtRepoClient, txtRepoMovie):
        super().__init__(txtRepoClient, txtRepoMovie)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        self._rentals.clear()
        with open(self._file_name, "rt") as f:
            lines = f.readlines()
            for line in lines:
                if len(line) > 0:
                    line = line.strip()
                    rental_id, client_id, movie_id, rented_date, due_date, returned_date = line.split(' ', 5)
                    rental_id = rental_id.strip()
                    client_id = client_id.strip()
                    movie_id = movie_id.strip()
                    rented_date = rented_date.strip()
                    rented_date = datetime.date.fromisoformat(rented_date)
                    due_date = due_date.strip()
                    due_date = datetime.date.fromisoformat(due_date)
                    returned_date = returned_date.strip()
                    returned_date = datetime.date.fromisoformat(returned_date)
                    rental = Rental(rental_id, client_id, movie_id, rented_date, due_date, returned_date)
                    self._rentals.append(rental)

    def _save_file(self):
        with open(self._file_name, "wt") as f:
            for rental in self._rentals:
                f.write(str(rental.get_rental_id()) + ' ' + str(rental.get_client_id()) + ' ' + str(rental.get_movie_id()) + ' ' + rental.get_rented_date().isoformat() + ' ' + rental.get_due_date().isoformat() + ' ' + rental.get_returned_date().isoformat() + '\n')

    def _update_file(self, rental):
        with open(self._file_name, "at") as f:
            f.write(str(rental.get_rental_id()) + ' ' + str(rental.get_client_id()) + ' ' + str(rental.get_movie_id()) + ' ' + rental.get_rented_date().isoformat() + ' ' + rental.get_due_date().isoformat() + ' ' + rental.get_returned_date().isoformat() + '\n')

    def rent_movie(self, rental):
        super(TextFileRepoRental, self).rent_movie(rental)
        self._update_file(rental)

    def return_movie(self, rental):
        super(TextFileRepoRental, self).return_movie(rental)
        self._save_file()

    def _remove_rental(self, rental_id):
        super(TextFileRepoRental, self)._remove_rental(rental_id)
        self._save_file()

    def _reverse_return(self, rental_id):
        super(TextFileRepoRental, self)._reverse_return(rental_id)
        self._save_file()

    def search_rental_by_id(self, rental_id):
        return super(TextFileRepoRental, self).search_rental_by_id(rental_id)

    def get_rentals_of_client(self, client_id):
        return super(TextFileRepoRental, self).get_rentals_of_client(client_id)

    def get_rentals_of_a_movie(self, movie_id):
        return super(TextFileRepoRental, self).get_rentals_of_a_movie(movie_id)

    def get_all_rentals(self):
        return super(TextFileRepoRental, self).get_all_rentals()

    def get_rented_days(self, rental_id):
        return super(TextFileRepoRental, self).get_rented_days(rental_id)

    def get_return_delay(self, rental_id):
        return super(TextFileRepoRental, self).get_return_delay(rental_id)

    def __len__(self):
        return len(self._rentals)