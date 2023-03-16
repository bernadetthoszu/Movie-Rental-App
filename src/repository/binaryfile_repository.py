import pickle
from src.repository.repositories import RepoMovie, RepoClient, RepoRental

class BinaryFileRepoMovie(RepoMovie):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        self._movies.clear()
        with open(self._file_name, "rb") as f:
            try:
                # while True:
                #     m = pickle.load(f)
                #     self._movies.add(m.get_movie_id(), m)
                self._movies = pickle.load(f)
            except EOFError:
                pass


    def _save_file(self):
        with open(self._file_name, "wb") as f:
            pickle.dump(self._movies, f)

    def add_movie(self, movie):
        """
        1. Do whatever the add method in the base class does
        2. Save the ingredients to file
        """
        super(BinaryFileRepoMovie, self).add_movie(movie)
        # super().add_movie(movie)
        self._save_file()

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



class BinaryFileRepoClient(RepoClient):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        self._clients.clear()
        with open(self._file_name, "rb") as f:
            try:
                # while True:
                #     c = pickle.load(f)
                #     self._clients.add(c.get_client_id(), c)
                self._clients = pickle.load(f)

            except EOFError:
                pass

    def _save_file(self):
        with open(self._file_name, "wb") as f:
            pickle.dump(self._clients, f)

    # def _update_file(self, client):
    #     with open(self._file_name, "ab") as f:
    #         pickle.dump(client, f)

    def add_client(self, client):
        super().add_client(client)
        self._save_file()

    def remove_client(self, client_id):
        super(BinaryFileRepoClient, self).remove_client(client_id)
        self._save_file()

    def search_client_by_id(self, client_id):
        return super(BinaryFileRepoClient, self).search_client_by_id(client_id)
        #this format is generated upon pressing 'enter' after having written the word 'super'
        #but is same with 'return super().search_client_by_id(client_id)'

    def update_client(self, client_id, new_value):
        super(BinaryFileRepoClient, self).update_client(client_id, new_value)
        self._save_file()

    def get_all_clients(self):
        return super(BinaryFileRepoClient, self).get_all_clients()

    def search_client(self, string_client):
        return super(BinaryFileRepoClient, self).search_client(string_client)

    def __len__(self):
        return super(BinaryFileRepoClient, self).__len__()



class BinaryFileRepoRental(RepoRental):

    def __init__(self, file_name, binRepoClient, binRepoMovie):
        super().__init__(binRepoClient, binRepoMovie)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        self._rentals.clear()
        with open(self._file_name, "rb") as f:
            try:
                # while True:
                    # r = pickle.load(f)
                    # self._rentals.add(r.get_rental_id(), r)
                self._rentals = pickle.load(f)
            except EOFError:
                pass

    def _save_file(self):
        with open(self._file_name, "wb") as f:
            pickle.dump(self._rentals, f)


    def rent_movie(self, rental):
        super(BinaryFileRepoRental, self).rent_movie(rental)
        self._save_file()

    def return_movie(self, rental):
        super(BinaryFileRepoRental, self).return_movie(rental)
        self._save_file()

    def remove_rental(self, rental_id):
        #super(BinaryFileRepoRental, self)._remove_rental(rental_id)
        super().remove_rental(rental_id)
        self._save_file()

    def reverse_return(self, rental_id):
        super(BinaryFileRepoRental, self).reverse_return(rental_id)
        self._save_file()

    def search_rental_by_id(self, rental_id):
        return super(BinaryFileRepoRental, self).search_rental_by_id(rental_id)

    def get_rentals_of_client(self, client_id):
        return super(BinaryFileRepoRental, self).get_rentals_of_client(client_id)

    def get_rentals_of_a_movie(self, movie_id):
        return super(BinaryFileRepoRental, self).get_rentals_of_a_movie(movie_id)

    def get_all_rentals(self):
        return super(BinaryFileRepoRental, self).get_all_rentals()

    # def get_rented_days(self, rental_id):
    #     return super(BinaryFileRepoRental, self).get_rented_days(rental_id)
    #
    # def get_return_delay(self, rental_id):
    #     return super(BinaryFileRepoRental, self).get_return_delay(rental_id)

    def __len__(self):
        return len(self._rentals)