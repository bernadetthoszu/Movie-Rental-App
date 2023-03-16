import unittest
import datetime
from src.services.services import SrvRental, SrvUndoRedo
from src.repository.validators import ValidRental
from src.repository.repositories import RepoRental, RepoMovie, RepoClient
from src.domain.entities import Rental, Movie, Client
from src.exceptions import ValidationError, RepositoryError
from src.services.sort_filter import IterableDictionary

#TODO Implement tests for rental services

class TestRentalService(unittest.TestCase, SrvRental):

    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        repoClient = RepoClient()
        repoMovies = RepoMovie()
        repoRental = RepoRental(repoClient, repoMovies)
        validRental = ValidRental()
        srvUndoRedo = SrvUndoRedo()

        movie = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts.', 'Romance')
        movie2 = Movie('2', 'Crime Busters', 'With Terence Hill and Bud Spencer.', 'Comedy')
        client = Client('1', 'Lucy')
        client2 = Client('2', 'Sally')
        repoClient.add_client(client)
        repoClient.add_client(client2)
        repoMovies.add_movie(movie)
        repoMovies.add_movie(movie2)

        client3 = Client('4', 'Ryan')
        repoClient.add_client(client3)
        repoRental.rent_movie(Rental('4', '4', '1', datetime.date.fromisoformat('2021-11-14'), datetime.date.fromisoformat('2021-11-20'), datetime.date.fromisoformat('2021-11-17')))
        self.testSrv = SrvRental(repoClient, repoMovies, repoRental, validRental, srvUndoRedo)

    def test_search_rental_by_id(self):
        self.testSrv.rent_movie('1', '1', '1', '2021-11-14', '2021-12-14')
        self.assertEqual(self.testSrv.search_rental_by_id('1'), Rental('1', '1', '1', datetime.date.fromisoformat('2021-11-14'), datetime.date.fromisoformat('2021-12-14'), datetime.date.min))
        self.assertRaisesRegex(RepositoryError, 'Inexisting rental!', self.testSrv.search_rental_by_id, '2') #why does it not work?

    def test_get_rentals_of_client(self):
        self.testSrv.rent_movie('1', '1', '1', '2021-11-14', '2021-12-14')
        other_iter_dict = IterableDictionary()
        other_iter_dict.add('1', Rental('1', '1', '1', datetime.date.fromisoformat('2021-11-14'), datetime.date.fromisoformat('2021-12-14'), datetime.date.min))
        self.assertEqual(self.testSrv.get_rentals_of_client('1'), other_iter_dict)
        other_iter_dict = IterableDictionary()
        self.assertEqual(self.testSrv.get_rentals_of_client ('3'), other_iter_dict)
        self.assertEqual(self.testSrv.get_rentals_of_client('2'), other_iter_dict)

    def test_get_rentals_of_client_ui(self):
        self.testSrv.rent_movie('1', '1', '1', '2021-11-14', '2021-12-14')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testSrv.get_rentals_of_client_ui, '-1')
        self.assertEqual(self.testSrv.get_rentals_of_client_ui('1'), [('1', 'Pretty Woman')])
        self.assertEqual(self.testSrv.get_rentals_of_client_ui('3'), [])
        self.assertEqual(self.testSrv.get_rentals_of_client_ui('2'), [])


    def test_rent_movie(self):
        #Rental id already in list!
        #Movie not in list!
        #Inexisting client!
        #Client has rental which passed its due date!
        #The client has already rented this movie but has not returned it yet!

        rented_date_bad1 = '2021-11-14'
        due_date_bad1 = '2021-11-20'


        self.testSrv.rent_movie('1', '1', '1', '2021-11-14', '2121-12-14')
        self.testSrv.rent_movie('2', '2', '2', rented_date_bad1, due_date_bad1)
        self.assertRaisesRegex(ValidationError, 'Invalid rental id! Invalid client id! Invalid movie id! Invalid due date! Invalid rented date! ', self.testSrv.rent_movie, '-1', '-1', '-1', 'today-today-today', 'today-today-today')
        self.assertRaisesRegex(ValidationError, 'Invalid rental id! Invalid client id! Invalid movie id! Invalid dates! - Due date is before rented date', self.testSrv.rent_movie, '-1', '-1', '-1', '2021-12-20', '2021-11-20')
        self.assertRaisesRegex(RepositoryError, 'Rental id already in list!', self.testSrv.rent_movie, '1', '1', '1', '2021-11-14', '2021-12-14')
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testSrv.rent_movie, '3', '1', '3', '2021-11-14', '2021-12-14')
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testSrv.rent_movie, '3', '3', '1', '2021-11-14', '2021-12-14')
        self.assertRaisesRegex(RepositoryError, 'Client has rental which passed its due date!', self.testSrv.rent_movie, '3', '2', '1', '2021-11-14', '2021-12-14')
        self.assertRaisesRegex(RepositoryError, 'The client has already rented this movie but has not returned it yet!', self.testSrv.rent_movie, '3', '1', '1', '2021-11-14', '2021-12-14')

    def test_return_movie(self):

        # due_date_passed...
        rented_date_bad1 = '2021-11-14'
        due_date_bad1 = '2021-11-20'

        self.testSrv.rent_movie('1', '1', '1', '2021-11-14', '2021-12-14')
        self.testSrv.rent_movie('2', '2', '2', rented_date_bad1, due_date_bad1)
        self.assertRaisesRegex(ValidationError, 'Invalid rental id!', self.testSrv.return_movie, '-1', '1')
        self.assertRaisesRegex(RepositoryError, 'Inexisting rental!', self.testSrv.return_movie, '3', '1')
        self.assertRaisesRegex(Exception, 'Bad rental id for client!', self.testSrv.return_movie, '2', '1')
        self.assertRaisesRegex(RepositoryError, 'Rental was already returned!', self.testSrv.return_movie, '4', '4')

    def test_most_rented_movies(self):
        self.testSrv.rent_movie('1', '1', '2', '2021-11-14', '2021-12-14')
        self.assertEqual(self.testSrv.most_rented_movies(), [Movie('2', 'Crime Busters', 'With Terence Hill and Bud Spencer.', 'Comedy'), Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts.', 'Romance')])
        another_repo_client = RepoClient()
        another_repo_movies = RepoMovie()
        another_repo_rental = RepoRental(another_repo_client, another_repo_movies)
        another_valid_rental = ValidRental()
        another_srvUndoRedo = SrvUndoRedo()
        another_service = SrvRental(another_repo_client, another_repo_movies, another_repo_rental, another_valid_rental, another_srvUndoRedo)
        self.assertRaisesRegex(Exception, 'No rentals!', another_service.most_rented_movies)

    def test_most_active_clients(self):
        self.testSrv.rent_movie('1', '1', '2', '2021-11-14', '2021-12-14')
        self.testSrv.rent_movie('2', '4', '2', '2021-11-14', '2021-12-14')
        self.assertEqual(self.testSrv.most_active_clients(), [Client('4', 'Ryan'), Client('1', 'Lucy'), Client('2', 'Sally')])
        another_repo_client = RepoClient()
        another_repo_movies = RepoMovie()
        another_repo_rental = RepoRental(another_repo_client, another_repo_movies)
        another_valid_rental = ValidRental()
        another_srvUndoRedo = SrvUndoRedo
        another_service = SrvRental(another_repo_client, another_repo_movies, another_repo_rental, another_valid_rental, another_srvUndoRedo)
        self.assertRaisesRegex(Exception, 'No rentals!', another_service.most_active_clients)

    def test_late_rentals(self):
        self.testSrv.rent_movie('1', '1', '2', '2021-11-14', '2121-12-14')
        self.testSrv.rent_movie('2', '4', '2', '2021-11-14', '2021-11-24')
        self.assertEqual(self.testSrv.late_rentals(), [Rental('2', '4', '2', datetime.date.fromisoformat('2021-11-14'), datetime.date.fromisoformat('2021-11-24'), datetime.date.min)])
        another_repo_client = RepoClient()
        another_repo_movies = RepoMovie()
        another_repo_rental = RepoRental(another_repo_client, another_repo_movies)
        another_valid_rental = ValidRental()
        another_srvUndoRedo = SrvUndoRedo()
        another_service = SrvRental(another_repo_client, another_repo_movies, another_repo_rental, another_valid_rental, another_srvUndoRedo)
        self.assertRaisesRegex(Exception, 'No rentals!', another_service.late_rentals)


class TestRentalValidator(unittest.TestCase):

    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.testValidator = ValidRental()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_validate(self):
        self.assertRaisesRegex(ValidationError, 'Invalid rental id! Invalid client id! Invalid movie id! Invalid due date! Invalid rented date! ', self.testValidator.validate, '-1', '-1', '-1', 'today-today-today', 'today-today-today')
        self.assertRaisesRegex(ValidationError, 'Invalid rental id! Invalid client id! Invalid movie id! Invalid dates! - Due date is before rented date', self.testValidator.validate, '-1', '-1', '-1', '2021-12-20', '2021-11-20')

class TestRentalRepository(unittest.TestCase):

    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.testRepoMovie = RepoMovie()
        self.testRepoClient = RepoClient()
        self.testRepoRental = RepoRental(self.testRepoClient, self.testRepoMovie)


        #In testRepoMovie we have : 2 movies
        #In testRepoClient we have : 2 clients
        #In testRepoRental we have : 2 rentals, 1 for each client
        movie = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts.', 'Romance')
        movie2 = Movie('2', 'Crime Busters', 'With Terence Hill and Bud Spencer.', 'Comedy')
        client = Client('1', 'Lucy')
        client2 = Client('2', 'Sally')
        self.testRepoClient.add_client(client)
        self.testRepoClient.add_client(client2)
        self.testRepoMovie.add_movie(movie)
        self.testRepoMovie.add_movie(movie2)

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_get_rentals_of_client(self):
        # movie = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts.', 'Romance')
        # movie2 = Movie('2', 'Crime Busters', 'With Terence Hill and Bud Spencer.', 'Comedy')
        # client = Client('1', 'Lucy')
        # self.testRepoClient.add_client(client)
        # self.testRepoMovie.add_movie(movie)
        # self.testRepoMovie.add_movie(movie2)

        rented_date = datetime.date.fromisoformat('2021-11-14')
        due_date = datetime.date.fromisoformat('2121-12-14')
        returned_date = datetime.date.min

        # due_date_passed...
        rented_date_bad1 = datetime.date.fromisoformat('2021-11-14')
        due_date_bad1 = datetime.date.fromisoformat('2021-11-20')
        returned_date_bad1 = datetime.date.min

        client3 = Client('3', 'Ben')
        self.testRepoClient.add_client(client3)
        other_iter_dict = IterableDictionary()
        self.assertEqual(self.testRepoRental.get_rentals_of_client('3'), other_iter_dict)

        rental = Rental('1', '1', '1', rented_date, due_date, returned_date)  # good
        rental2 = Rental('2', '1', '2', rented_date_bad1, due_date_bad1, returned_date_bad1)  # good
        self.testRepoRental.rent_movie(rental)
        self.testRepoRental.rent_movie(rental2)

        client_rentals = self.testRepoRental.get_rentals_of_client('1')
        other_iter_dict.add('1', rental)
        other_iter_dict.add('2', rental2)
        self.assertEqual(client_rentals, other_iter_dict)

    def test_rent_movie(self):
        rented_date = datetime.date.fromisoformat('2021-11-14')
        due_date = datetime.date.fromisoformat('2121-12-14')
        returned_date = datetime.date.min

        # due_date_passed...
        rented_date_bad1 = datetime.date.fromisoformat('2021-11-14')
        due_date_bad1 = datetime.date.fromisoformat('2021-11-20')
        returned_date_bad1 = datetime.date.min

        rental = Rental('1', '1', '1', rented_date, due_date, returned_date)  # good
        rental2 = Rental('2', '2', '1', rented_date_bad1, due_date_bad1, returned_date_bad1)  # good
        self.testRepoRental.rent_movie(rental)
        self.testRepoRental.rent_movie(rental2)

        rental_bad1 = Rental('3', '1', '3', rented_date, due_date, returned_date)  # movie not in list
        rental_bad2 = Rental('3', '3', '1', rented_date, due_date, returned_date)  # inexistent client
        rental_bad3 = Rental('3', '1', '1', rented_date, due_date, returned_date)  # the client has already rented this movie, and not returned it yet
        rental_bad4 = Rental('3', '2', '2', rented_date, due_date, returned_date)  # the client has rental which passed its due date

        self.assertRaisesRegex(RepositoryError, 'Rental id already in list!', self.testRepoRental.rent_movie, rental)

        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testRepoRental.rent_movie, rental_bad1)

        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testRepoRental.rent_movie, rental_bad2)

        self.assertRaisesRegex(RepositoryError, 'The client has already rented this movie but has not returned it yet!', self.testRepoRental.rent_movie, rental_bad3)

        self.assertRaisesRegex(RepositoryError, 'Client has rental which passed its due date!', self.testRepoRental.rent_movie, rental_bad4)


    def test_return_movie(self):

        rented_date = datetime.date.fromisoformat('2021-11-14')
        due_date = datetime.date.fromisoformat('2121-12-14')
        returned_date = datetime.date.min

        # due_date_passed...
        rented_date_bad1 = datetime.date.fromisoformat('2021-11-14')
        due_date_bad1 = datetime.date.fromisoformat('2021-11-20')
        returned_date_bad1 = datetime.date.fromisoformat('2021-11-17')

        rental = Rental('1', '1', '1', rented_date, due_date, returned_date)  # good
        rental2 = Rental('2', '2', '1', rented_date_bad1, due_date_bad1, returned_date_bad1)
        self.testRepoRental.rent_movie(rental)
        self.testRepoRental.rent_movie(rental2)

        self.assertRaisesRegex(RepositoryError, 'Rental was already returned!', self.testRepoRental.return_movie, rental2)
        self.testRepoRental.return_movie(rental)
        self.assertEqual(self.testRepoRental.search_rental_by_id('1'), Rental('1', '1', '1', rented_date, due_date, datetime.date.today()))


    def test_remove_rental(self):
        rented_date = datetime.date.fromisoformat('2021-11-14')
        due_date = datetime.date.fromisoformat('2021-11-24')
        returned_date = datetime.date.min
        rental = Rental('1', '1', '1', rented_date, due_date, returned_date)
        self.testRepoRental.rent_movie(rental)
        self.assertEqual(len(self.testRepoRental), 1)
        self.testRepoRental.remove_rental('1')
        self.assertEqual(len(self.testRepoRental), 0)

    def test_reverse_return(self):
        rented_date = datetime.date.fromisoformat('2021-11-14')
        due_date = datetime.date.fromisoformat('2021-11-20')
        returned_date = datetime.date.fromisoformat('2021-11-17')
        rental2 = Rental('2', '2', '1', rented_date, due_date, returned_date)
        self.testRepoRental.rent_movie(rental2)
        self.testRepoRental.reverse_return('2')
        self.assertEqual(self.testRepoRental.search_rental_by_id('2').get_returned_date(), datetime.date.min)
