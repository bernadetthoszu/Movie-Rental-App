import datetime
from src.exceptions import RepositoryError
from src.services.sort_filter import IterableDictionary

class RepoMovie :

    """"
    This class represents the repo for movies
    Movies can : - have same title, description and/or genre
                 - NOT have same id
    """

    def __init__(self):
        """"
        key = movie_id
        """
        self._movies = IterableDictionary()

    def add_movie(self, movie):
        """"
        params: Receives the object 'movie' of type Movie which is to be added to the repository
        Adds the object 'movie' of type Movie to the repository
        Raises RepositoryError if a movie with the same ID has already been added
        ! ID must be unique
        """
        # for m in self._movies:
        #     if m.get_movie_id() == movie.get_movie_id() :
        #         raise RepositoryError('Movie id already in list!')
        # self._movies.append(movie)

        try:
            self._movies.add(movie.get_movie_id(), movie)
        except ValueError:
            raise RepositoryError('Movie id already in list!')


    def remove_movie(self, movie_id):
        """"
        params: Receives the ID of the movie to be removed
        Removes the movie from the repository
        Raises RepositoryError if the movie is not in list
        """
        # for m in self._movies :
        #     if m.get_movie_id() == movie_id :
        #         self._movies.remove(m)
        #         return
        # raise RepositoryError('Movie not in list!')

        try:
            del self._movies[movie_id]
        except KeyError:
            raise RepositoryError('Movie not in list!')

    def search_movie_by_id(self, movie_id):
        """"
        Only used for business purposes, not needed in the ui section
        params: Receives the ID of the movie being searched for
        Returns the object of type Movie which has the given id
        Raises RepositoryError if the movie is not in list
        """
        # for m in self._movies :
        #     if m.get_movie_id() == movie_id :
        #         return m
        # raise RepositoryError('Movie not in list!')
        try:
            return self._movies[movie_id]
        except ValueError:
            raise RepositoryError('Movie not in list!')

    def update_movie(self, movie_id, attribute, new_value):
        """"
        params: Receives the ID of the movie to be updated, the attribute to be modified (description or genre) and the replacement value
        Description can be anything but genre must be from the list ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation']
        Updates the movie from the repository with the given new value for the given field
        Raises RepositoryError if the movie is not in list
        """
        # for m in self._movies :
        #     if m.get_movie_id() == movie_id :
        #         if attribute == 'description' :
        #             m.set_description(new_value)
        #             return
        #         else :
        #             m.set_genre(new_value)
        #             return
        # raise RepositoryError('Movie not in list!')
        try:
            movie = self._movies[movie_id]
        except ValueError:
            raise RepositoryError('Movie not in list!')
        if attribute == 'description':
            movie.set_description(new_value)
            return
        else:
            movie.set_genre(new_value)
            return

    def get_all_movies(self):
        """"
        Returns all contents of the repository - a list with objects of type Movie
        """
        # return self._movies
        return self._movies

    def search_movie(self, string_movie):
        """"
        params: Receives the string being searched by
        Returns a list with all movies of type Movie which have 'string_movie' in their composition
        Raises RepositoryError if no movie contains the given substring
        """
        string_movie = string_movie.lower()
        found_movies = []
        for movie_id in self._movies:
            movie = self.search_movie_by_id(movie_id)
            id_aux = str(movie.get_movie_id()).lower()
            title_aux = str(movie.get_title()).lower()
            description_aux = str(movie.get_description()).lower()
            genre_aux = str(movie.get_genre()).lower()
            if string_movie in id_aux or string_movie in title_aux or string_movie in description_aux or string_movie in genre_aux:
                found_movies.append(movie)
        if found_movies == []:
            raise RepositoryError('No movie found!')
        return found_movies


    def __len__(self):
        return len(self._movies)


class RepoClient :

    """"
    This class represents the repository of clients
    Clients can : - have same name (name coincidence)
                  - NOT have same id
    """

    def __init__(self):
        self._clients = IterableDictionary()

    def add_client(self, client):
        """"
        params: Receives the object 'client' of type Client which is to be added to the repository
        Adds the object 'client' of type Client to the repository
        Raises RepositoryError if a client with the same ID has already been added
        ! ID must be unique
        """
        # for c in self._clients:
        #     if c.get_client_id() == client.get_client_id():
        #         raise RepositoryError('Client id already in list!')
        # self._clients.append(client)

        try:
            self._clients.add(client.get_client_id(), client)
        except ValueError:
            raise RepositoryError('Client id already in list!')

    def remove_client(self, client_id):
        """"
        params: Receives the ID of the client to be removed
        Removes the client from the repository
        Raises RepositoryError if the client is not in list
        """
        # for c in self._clients:
        #     if c.get_client_id() == client_id:
        #         self._clients.remove(c)
        #         return
        # raise RepositoryError('Inexisting client!')
        try:
            del self._clients[client_id]
        except KeyError:
            raise RepositoryError('Inexisting client!')

    def search_client_by_id(self, client_id):
        """"
        Only used for business purposes, not needed in the ui section
        params: Receives the ID of the client being searched for
        Returns the object of type Client which has the given id
        Raises RepositoryError if the client is not in list
        """
        # for c in self._clients:
        #     if c.get_client_id() == client_id:
        #         return c
        # raise RepositoryError('Inexisting client!')
        try:
            return self._clients[client_id]
        except ValueError:
            raise RepositoryError('Inexisting client!')

    def update_client(self, client_id, new_value):
        """"
        params: Receives the ID of the client to be updated and the new name
        Updates the client in the repository with the new value
        Raises RepositoryError if the client is not in list
        """
        # for c in self._clients :
        #     if c.get_client_id() == client_id :
        #         c.set_name(new_value)
        #         return
        # raise RepositoryError('Inexisting client!')
        try:
            client = self._clients[client_id]
            client.set_name(new_value)
        except ValueError:
            raise RepositoryError('Inexisting client!')
        return

    def get_all_clients(self):
        """"
        Returns all contents of the repository - a list with objects of type Movie
        """
        return self._clients

    def search_client(self, string_client):
        """"
        params: Receives the string being searched by
        Returns a list with all clients of type Client which have 'string_client' in their composition
        Raises RepositoryError if no client contains the given substring
        """
        string_client = string_client.lower()
        found_clients = []
        for client_id in self._clients:
            client = self.search_client_by_id(client_id)
            id_aux = str(client.get_client_id()).lower()
            name_aux = str(client.get_name()).lower()
            if string_client in id_aux or string_client in name_aux:
                found_clients.append(client)
        if found_clients == []:
            raise RepositoryError('No client found!')
        return found_clients

    def __len__(self):
        return len(self._clients)

class RepoRental :
    def __init__(self, repoClient, repoMovie):
        self._rentals = IterableDictionary()
        self.__repositoryClient = repoClient
        self.__repositoryMovie = repoMovie

    def search_rental_by_id(self, rental_id):
        # for r in self._rentals:
        #     if r.get_rental_id() == rental_id:
        #         return r
        # raise RepositoryError('Inexisting rental!')
        try:
            return self._rentals[rental_id]
        except ValueError:
            raise RepositoryError('Inexisting rental!')

    def get_rentals_of_client(self, client_id):
        client_rentals = IterableDictionary()
        for rental_id in self._rentals:
            rental = self.search_rental_by_id(rental_id)
            if rental.get_client_id() == client_id:
                client_rentals.add(rental_id, rental)
        return client_rentals

    def get_rentals_of_a_movie(self, movie_id):
        movie_rentals = IterableDictionary()
        for rental_id in self._rentals:
            rental = self.search_rental_by_id(rental_id)
            if rental.get_movie_id() == movie_id:
                movie_rentals.add(rental_id, rental)
        return movie_rentals

    def get_all_rentals(self):
        return self._rentals

    def rent_movie(self, rental):
        """"
        A client can rent a movie under the conditions :
                - the client has no rented movie passed its due date (returned_date == datetime.date.min and datetime.date.today() > due_date)
                - the client hasn't got the same movie already rented and not returned (returned_date == datetime.date.min and client_id == rental.client_id and movie_id == rental.movie_id)
        The rental id can't be one already present in the list of rentals.txt
        The movie must exist in the repository of movies
        The client must exist in the repository of clients (if not it has to be added in order to rent...)

        """
        for rental_id in self._rentals:
            if rental_id == rental.get_rental_id():
                raise RepositoryError('Rental id already in list!')

        #If meaning of var names is false, the assignments will raise RepositoryErrors
        movie_is_in_movie_repo = self.__repositoryMovie.search_movie_by_id(rental.get_movie_id())
        client_is_in_client_repo = self.__repositoryClient.search_client_by_id(rental.get_client_id())
        client_rentals = self.get_rentals_of_client(rental.get_client_id())

        for r_id in client_rentals:
            r = client_rentals[r_id]
            if r.get_returned_date() == datetime.date.min and datetime.date.today() > r.get_due_date():
                raise RepositoryError('Client has rental which passed its due date!')

        for r_id in client_rentals:
            r = client_rentals[r_id]
            if r.get_movie_id() == rental.get_movie_id() and r.get_returned_date() == datetime.date.min:
                raise RepositoryError('The client has already rented this movie but has not returned it yet!')

        self._rentals.add(rental.get_rental_id(), rental)

    def return_movie(self, rental):
        if rental.get_returned_date() > datetime.date.min:
            raise RepositoryError('Rental was already returned!')
        rental.set_returned_date(datetime.date.today())

    def remove_rental(self, rental_id):
            del self._rentals[rental_id]


    def reverse_return(self, rental_id):
        rental = self._rentals[rental_id]
        rental.set_returned_date(datetime.date.min)

    def __len__(self):
        return len(self._rentals)