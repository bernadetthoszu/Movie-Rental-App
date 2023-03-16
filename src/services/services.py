import datetime
import random
from src.domain.entities import Movie, Client, Rental
from src.exceptions import RepositoryError, UndoRedoError
from src.services.tools_undo_redo import Call, Operation, CascadedOperation
from src.services.sort_filter import IterableDictionary, Sort, Filter


class SrvMovie :
    """"
    The class of functionalities associated to a movie
    """
    def __init__(self, repoMovie, validMovie, srvUndoRedo):
        self.__repositoryMovie = repoMovie
        self.__validatorMovie = validMovie
        self.__serviceUndoRedo = srvUndoRedo

    def _generate_random_movies(self):
        movie_titles = ['Bridget Jones` Diary', 'Maid in Manhattan', 'Monster in Law', 'La vita e bella',
                        'Pretty Woman', 'What a girl wants', 'Spectre', 'Golden Eye']

        movie_genres = ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western',
                        'Documentary', 'Musical', 'Animation']
        for i in range(1, 9):
            movie = Movie(str(i), movie_titles[random.randint(0, 7)], '', movie_genres[random.randint(0, 10)])
            self.__repositoryMovie.add_movie(movie)

    def add_movie(self, movie_id, title, description, genre):
        """"
        params: the attributes of a movie : ID, title, description, genre
        Calls validation and  repo functions to add the object 'movie' of type Movie to the repository.
        """
        movie = Movie(movie_id, title, description, genre)
        self.__validatorMovie.validate(movie)
        self.__repositoryMovie.add_movie(movie)
        undo_call = Call(self.__repositoryMovie.remove_movie, movie_id)
        redo_call = Call(self.__repositoryMovie.add_movie, movie)
        cope = Operation(undo_call, redo_call)
        self.__serviceUndoRedo.record(cope)

    def remove_movie(self, movie_id):
        """"
        params: movie ID
        Calls validation and  repo functions to remove the object with the given movie ID from the repository.
        """
        self.__validatorMovie.validate_movie_id(movie_id)
        self.__repositoryMovie.remove_movie(movie_id)

    def update_movie(self, movie_id, attribute, new_value):
        """"
        params: movie ID, the attribute (description, genre) which is to be changed, the replacement value
        Description can be anything but the genre must be from ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation']
        Calls validation and  repo functions to update the object with the given movie ID in the repository.
        """
        self.__validatorMovie.validate_update(attribute, new_value)
        self.__validatorMovie.validate_movie_id(movie_id)

        movie_old = self.search_movie_by_id(movie_id)
        if attribute == 'description':
            old_value = movie_old.get_description()
        else:
            old_value = movie_old.get_genre()

        self.__repositoryMovie.update_movie(movie_id, attribute, new_value)

        undo_call = Call(self.__repositoryMovie.update_movie, movie_id, attribute, old_value)
        redo_call = Call(self.__repositoryMovie.update_movie, movie_id, attribute, new_value)
        cope = Operation(undo_call, redo_call)
        self.__serviceUndoRedo.record(cope)

    # def movies_starting_with_a(self):
    #     movies = self.__repositoryMovie.get_all_movies()
    #     return [x for x in movies if x.get_title()[0] == 'a']

    def search_movie_by_id(self, movie_id):
        """"
        params: movie ID
        Returns the object of type Movie which has the ID the value from the variable movie_id
        """
        return self.__repositoryMovie.search_movie_by_id(movie_id)

    def get_all_movies(self):
        """"
        Returns all movies retrieved from repository as an IterableDictionary type.
        """
        return self.__repositoryMovie.get_all_movies()

    def search_movie(self, string_movie):
        """"
        params: the string introduced by the user, by which the search is being done
        The search is case-insesitive, and goes with partial-match too
        Returns all movies which have 'string_client' in their composition
        Returns a list of objects of type Movie.
        """
        return self.__repositoryMovie.search_movie(string_movie)


class SrvClient :
    """"
    The class of functionalities associated to a client
    """
    def __init__(self, repoClient, validClient, srvUndoRedo):
        self.__repositoryClient = repoClient
        self.__validatorClient = validClient
        self.__serviceUndoRedo = srvUndoRedo

    def _generate_random_clients(self):
        names = ['Lucy', 'Ben', 'Ryan', 'Diana', 'Jennifer', 'Alex', 'Thomas', 'Geraldine', 'Pamela']
        for i in range(1, 9):
            client = Client(str(i), names[random.randint(0, 8)])
            self.__repositoryClient.add_client(client)

    def add_client(self, client_id, name):
        """"
        params: the attributes of a client : ID, name
        Calls validation and  repo functions to add the object 'client' of type Client to the repository.
        """
        client = Client(client_id, name)
        self.__validatorClient.validate_client_id(client_id)
        self.__repositoryClient.add_client(client)
        undo_call = Call(self.__repositoryClient.remove_client, client_id)
        redo_call = Call(self.__repositoryClient.add_client, client)
        cope = Operation(undo_call, redo_call)
        self.__serviceUndoRedo.record(cope)

    def remove_client(self, client_id):
        """"
        params: client ID
        Calls validation and  repo functions to remove the object with the given client ID from the repository.
        """
        self.__validatorClient.validate_client_id(client_id)
        self.__repositoryClient.remove_client(client_id)

    def update_client(self, client_id, new_value):
        """"
        params: movie ID, the attribute which is to be changed, the replacement value
        Calls validation and  repo functions to update the object with the given movie ID in the repository.
        """
        self.__validatorClient.validate_client_id(client_id)
        client = self.search_client_by_id(client_id)
        old_value = client.get_name()
        self.__repositoryClient.update_client(client_id, new_value)
        undo_call = Call(self.__repositoryClient.update_client, client_id, old_value)
        redo_call = Call(self.__repositoryClient.update_client, client_id, new_value)
        cope = Operation(undo_call, redo_call)
        self.__serviceUndoRedo.record(cope)

    def search_client_by_id(self, client_id):
        """"
        Only used for business purposes, not from UI.
        Returns the object of type Client which has the ID the value from the variable client_id
        """
        return self.__repositoryClient.search_client_by_id(client_id)

    def get_all_clients(self):
        """"
        Returns all clients retreived from repository.
        """
        return self.__repositoryClient.get_all_clients()

    def search_client(self, string_client):
        """"
        params: the string introduced by the user, by which the search is being done
        The search is case-insesitive, and goes with partial-match too
        Returns all clients which have 'string_client' in their composition
        """
        return self.__repositoryClient.search_client(string_client)


class SrvRental :

    def __init__(self, repoClient, repoMovie, repoRental, validRental, srvUndoRedo):
        self.__repositoryClient = repoClient
        self.__repositoryMovie = repoMovie
        self.__repositoryRental = repoRental
        self.__validatorRental = validRental
        self.__serviceUndoRedo = srvUndoRedo

    def _generate_random_rentals(self):
        rental_dates = [['2010-12-13', '2011-01-03'], ['2018-06-23', '2018-09-01'], ['2021-11-25', '2021-12-31']]
        i = 1
        while i < 5:
            try:
                rented_date, due_date = rental_dates[random.randint(0, 2)]
                rented_date = datetime.date.fromisoformat(rented_date)
                due_date = datetime.date.fromisoformat(due_date)
                returned_date = datetime.date.min
                rental = Rental(str(i), str(random.randint(1, 8)), str(random.randint(1, 8)), rented_date, due_date, returned_date)
                self.__repositoryRental.rent_movie(rental)
            except RepositoryError:
                i -= 1
            i += 1

    def search_rental_by_id(self, rental_id):
        """"
        Only used for business purposes, not from UI.
        Returns the object of type Rental which has the ID the value from the variable rental_id
        """
        return self.__repositoryRental.search_rental_by_id(rental_id)

    def get_rentals_of_client(self, client_id):
        """"
        Returns a list.
        """
        return self.__repositoryRental.get_rentals_of_client(client_id)

    def get_rentals_of_a_movie(self, movie_id):
        """"
        Returns a list.
        """
        return self.__repositoryRental.get_rentals_of_a_movie(movie_id)

    def get_all_rentals(self):
        """"
        Returns an IterableDictionary.
        """
        return self.__repositoryRental.get_all_rentals()

    def get_rentals_of_client_ui(self, client_id):
        self.__validatorRental.validate_client_id(client_id)
        client_rentals = self.__repositoryRental.get_rentals_of_client(client_id)
        client_rentals_ui = []
        for r_id in client_rentals:
            r = client_rentals[r_id]
            if r.get_returned_date() == datetime.date.min :
                client_rentals_ui.append((r.get_rental_id(), self.__repositoryMovie.search_movie_by_id(r.get_movie_id()).get_title()))
        return client_rentals_ui

    def rent_movie(self, rental_id, client_id, movie_id, rented_date, due_date):
        self.__validatorRental.validate(rental_id, client_id, movie_id, rented_date, due_date)
        rented_date = datetime.date.fromisoformat(rented_date)
        due_date = datetime.date.fromisoformat(due_date)
        returned_date = datetime.date.min
        rental = Rental(rental_id, client_id, movie_id, rented_date, due_date, returned_date)
        self.__repositoryRental.rent_movie(rental)
        undo_call = Call(self.__repositoryRental.remove_rental, rental_id)
        redo_call = Call(self.__repositoryRental.rent_movie, rental)
        cope = Operation(undo_call, redo_call)
        self.__serviceUndoRedo.record(cope)

    def return_movie(self, rental_id, client_id):
        self.__validatorRental.validate_rental_id(rental_id)
        rental = self.__repositoryRental.search_rental_by_id(rental_id)
        client_rentals = self.get_rentals_of_client(client_id)#this won't raise an exception at this stage
        if rental_id not in client_rentals:
            raise Exception('Bad rental id for client!')
        else :
            self.__repositoryRental.return_movie(rental)
            undo_call = Call(self.__repositoryRental.reverse_return, rental_id)
            redo_call = Call(self.__repositoryRental.return_movie, rental)
            cope = Operation(undo_call, redo_call)
            self.__serviceUndoRedo.record(cope)

    def sort_key(self, item):
        return item[1]

    def most_rented_movies(self):
        # movies = self.__repositoryMovie.get_all_movies()
        # nr_of_movies = len(movies)
        # rentals = self.__repositoryRental.get_all_rentals()
        # if len(rentals) == 0:
        #     raise Exception('No rentals!')
        # # total_nr_of_days_per_movie = [0, 0]*3 makes deep copy of the list [0, 0] !!!
        #
        # total_nr_of_days_per_movie = [[0, 0] for i in range(0, len(movies))]
        # i=0
        # while i < nr_of_movies:
        #     total_nr_of_days_per_movie[i][0] = i
        #     i += 1
        # i=0
        # for rental_id in rentals:
        #     rental = self.search_rental_by_id(rental_id)
        #     movie = self.__repositoryMovie.search_movie_by_id(rental.get_movie_id())
        #     total_nr_of_days_per_movie[i][1] += self.__repositoryRental.get_rented_days(rental_id).days
        #     i+=1
        #
        # total_nr_of_days_per_movie.sort(reverse=True, key=self.sort_key)
        #
        # movies_statistics = []
        # for l in total_nr_of_days_per_movie:
        #     movies_statistics.append(self.__repositoryMovie.search_movie_by_id(movies[l[0]].get_movie_id()))
        # return movies_statistics

        if len(self.__repositoryRental) == 0:
            raise Exception('No rentals!')
        movies_stats = IterableDictionary()    #key = movie_id, value = total nr of days
        all_movies = self.__repositoryMovie.get_all_movies()
        for movie_id in all_movies:
            rentals_of_movie = self.__repositoryRental.get_rentals_of_a_movie(movie_id)
            total_nr_of_days = 0
            for rental_id in rentals_of_movie:
                rental = self.__repositoryRental.search_rental_by_id(rental_id)
                total_nr_of_days += rental.get_rented_days()
            movies_stats.add(movie_id, total_nr_of_days)
        movies_sorted = Sort.shellSort(lambda x, y: x >= y, movies_stats)
        result = []
        for movie_id in movies_sorted:
            # movie = self.__repositoryMovie.search_movie_by_id(movie_id)
            movie = self.__repositoryMovie.search_movie_by_id(movie_id)
            result.append(movie)
        return result



    def most_active_clients(self):
        # clients = self.__repositoryClient.get_all_clients()
        # nr_of_clients = len(clients)
        # rentals = self.__repositoryRental.get_all_rentals()
        # if len(rentals) == 0:
        #     raise Exception('No rentals!')
        #
        # total_nr_of_days_per_client = [[0, 0] for i in range(0, len(clients))]
        # i = 0
        # while i < nr_of_clients:
        #     total_nr_of_days_per_client[i][0] = i
        #     i += 1
        # i=0
        # for client_id in clients:
        #     client_rentals = self.get_rentals_of_client(client_id)
        #     for rental in client_rentals:
        #         total_nr_of_days_per_client[i][1] += self.__repositoryRental.get_rented_days(client_id).days
        #     i+=1
        #
        # total_nr_of_days_per_client.sort(reverse=True, key=self.sort_key)
        #
        # clients_statistics = []
        # for l in total_nr_of_days_per_client:
        #     clients_statistics.append(self.__repositoryClient.search_client_by_id(clients[l[0]].get_client_id()))
        # return clients_statistics

        if len(self.__repositoryRental) == 0:
            raise Exception('No rentals!')
        clients_stats = IterableDictionary()  # key = client_id, value = total nr of days
        all_clients = self.__repositoryClient.get_all_clients()
        for client_id in all_clients:
            rentals_of_client = self.__repositoryRental.get_rentals_of_client(client_id)
            total_nr_of_days = 0
            for rental_id in rentals_of_client:
                rental = self.__repositoryRental.search_rental_by_id(rental_id)
                total_nr_of_days += rental.get_rented_days()
            clients_stats.add(client_id, total_nr_of_days)
        clients_sorted = Sort.shellSort(lambda x, y: x >= y, clients_stats)
        result = []
        for client_id in clients_sorted:
            # client = self.__repositoryClient.search_client_by_id(client_id)
            client = self.__repositoryClient.search_client_by_id(client_id)
            result.append(client)
        return result

    def late_rentals(self):
        all_rentals = self.__repositoryRental.get_all_rentals()
        if len(all_rentals) == 0:
            raise Exception('No rentals!')

        late_rentals = Filter.filter(lambda x: x.get_return_delay() > 0, all_rentals)
        sorted_late_rentals = Sort.shellSort(lambda x, y: x.get_return_delay() >= y.get_return_delay(), late_rentals)

        # total_nr_of_days_per_rental = []
        # for rental_id in rentals:
        #     delay = self.__repositoryRental.get_return_delay(rental_id).days
        #     if delay > 0:
        #         total_nr_of_days_per_rental.append([rental_id, delay])
        #
        # total_nr_of_days_per_rental.sort(reverse=True, key=self.sort_key)
        # nr_of_late_rentals = len(total_nr_of_days_per_rental)

        result = []
        # for l in total_nr_of_days_per_rental:
        #     #[id_rental, movie, delay]
        #     #id_rental - string, movie - Movie, delay - int
        #     stats.append([l[0], self.__repositoryMovie.search_movie_by_id(self.__repositoryRental.search_rental_by_id(l[0]).get_movie_id()), l[1]])
        # return stats

        for rental_id in sorted_late_rentals:
            rental = sorted_late_rentals[rental_id]
            result.append(rental)
        return result

    # def _remove_rental(self, rental_id):
    #     self.__repositoryRental._remove_rental(rental_id)
    #
    # def _reverse_return(self, rental_id):
    #     self.__repositoryRental._reverse_return(rental_id)

#class SrvUndoRedo(SrvRental):
class SrvUndoRedo:

    """"
    Undo/redo is available and needed only for functionalities which modify the repositories
    """

    def __init__(self):
        self._history = []
        self._index = -1

    def record(self, operation):
        self._history.append(operation)
        self._index = len(self._history) - 1

    def undo(self):
        if self._index == -1:
            raise UndoRedoError('No more undos!')
        self._history[self._index].undo()
        self._index -= 1

    def redo(self):
        if self._index >= (len(self._history) - 1):
            raise UndoRedoError('No more redos!')
        self._history[self._index + 1].redo()
        self._index += 1


class SrvRemove:
    def __init__(self, serviceUndoRedo, repositoryMovies, repositoryClient, repositoryRental):
        self.__serviceUndoRedo = serviceUndoRedo
        self.__repositoryRental = repositoryRental
        self.__repositoryMovies = repositoryMovies
        self.__repositoryClient = repositoryClient

    def remove_movie(self, movie_id):
        movie = self.__repositoryMovies.search_movie_by_id(movie_id)
        title = movie.get_title()
        description = movie.get_description()
        genre = movie.get_genre()
        """"
        Remove movie + undo/redo
        """
        undo_call = Call(self.__repositoryMovies.add_movie, movie)
        redo_call = Call(self.__repositoryMovies.remove_movie, movie_id)
        cope = CascadedOperation()
        cope.add(Operation(undo_call, redo_call))
        self.__repositoryMovies.remove_movie(movie_id)

        rentals_of_movie = self.__repositoryRental.get_rentals_of_a_movie(movie_id)
        for r_id in rentals_of_movie:
            """"
            Cascaded operation for adding/removing the corresponding rentals.txt + undo/redo.
            """
            r = self.__repositoryRental.search_rental_by_id(r_id)
            undo_call = Call(self.__repositoryRental.rent_movie, r)
            redo_call = Call(self.__repositoryRental.remove_rental, r.get_rental_id())
            cope.add(Operation(undo_call, redo_call))
            self.__repositoryRental.remove_rental(r.get_rental_id())

        self.__serviceUndoRedo.record(cope)

    def remove_client(self, client_id):
        client = self.__repositoryClient.search_client_by_id(client_id)
        name = client.get_name()
        """"
        Remove client + undo/redo
        """
        undo_call = Call(self.__repositoryClient.add_client, client)
        redo_call = Call(self.__repositoryClient.remove_client, client_id)
        cope = CascadedOperation()
        cope.add(Operation(undo_call, redo_call))
        self.__repositoryClient.remove_client(client_id)

        rentals_of_client = self.__repositoryRental.get_rentals_of_client(client_id)
        for r_id in rentals_of_client:
            """"
            Cascaded operation for adding/removing the corresponding rentals.txt + undo/redo.
            """
            r = self.__repositoryRental.search_rental_by_id(r_id)
            undo_call = Call(self.__repositoryRental.rent_movie,  r)
            redo_call = Call(self.__repositoryRental.remove_rental, r_id)
            cope.add(Operation(undo_call, redo_call))
            self.__repositoryRental.remove_rental(r_id)

        self.__serviceUndoRedo.record(cope)