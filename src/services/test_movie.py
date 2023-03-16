import unittest
from src.services.services import SrvMovie, SrvUndoRedo
from src.repository.repositories import RepoMovie
from src.repository.validators import ValidMovie
from src.domain.entities import Movie
from src.exceptions import ValidationError, RepositoryError
from src.services.sort_filter import IterableDictionary


#TODO Create a suite
#loadTestsFromTestCase(testCaseClass)


class TestMovieServices(unittest.TestCase) :

    """"
    names start with the letters 'test' - this naming convention informs the test runner about which methods represent tests
    """

    def setUp(self):
        unittest.TestCase.setUp(self)
        testRepo = RepoMovie()
        testValidator = ValidMovie()
        testSrvUndoRedo = SrvUndoRedo()
        self.testSrv = SrvMovie(testRepo, testValidator, testSrvUndoRedo)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_add_movie(self):

        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        movie1 = Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        self.assertEqual(self.testSrv.search_movie_by_id('1'), movie1)
        self.assertRaisesRegex(RepositoryError, 'Movie id already in list!', self.testSrv.add_movie, '1', 'Pretty Woman', '', 'Romance')
        self.assertRaisesRegex(ValidationError, 'Invalid id! Invalid genre!', self.testSrv.add_movie, '-1', 'Pretty Woman', '', 'Romantic Comedy')
        #! Here the repo and validation functionalities should also be tested in order to see if they WORK WELL TOGETHER

    def test_remove_movie(self):
        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        self.testSrv.remove_movie('1')
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testSrv.search_movie_by_id, '1')
        self.assertRaisesRegex(ValidationError, 'Invalid movie id!', self.testSrv.remove_movie, '-1')

    def test_update_movie(self):
        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        self.testSrv.update_movie('1', 'description', 'Starring Richard Gere and Julia Roberts')
        self.assertEqual(self.testSrv.search_movie_by_id('1') , Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance'))
        self.testSrv.update_movie('1', 'genre', 'Comedy')
        self.assertEqual(self.testSrv.search_movie_by_id('1') , Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Comedy'))
        self.assertRaisesRegex(ValidationError, 'Invalid attribute!', self.testSrv.update_movie, '1', 'title', 'What a girl wants')
        self.assertRaisesRegex(ValidationError, 'Invalid genre!', self.testSrv.update_movie, '1', 'genre', 'Romanic Comedy')
        self.assertRaisesRegex(ValidationError, 'Invalid movie id!', self.testSrv.update_movie, '-1', 'description', '')
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testSrv.update_movie, '2', 'description', '')

    def test_get_all_movies(self):
        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        other_dict_iter =IterableDictionary()
        other_dict_iter.add('1', Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance'))
        self.assertEqual(self.testSrv.get_all_movies(), other_dict_iter)
        self.testSrv.remove_movie('1')
        other_dict_iter = IterableDictionary()
        self.assertEqual(self.testSrv.get_all_movies(), other_dict_iter)

    def test_search_movie_by_id(self):
        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        self.assertEqual(self.testSrv.search_movie_by_id('1'), Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance'))
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testSrv.search_movie_by_id, '2')

    def test_search_movie(self):
        self.testSrv.add_movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')
        self.testSrv.add_movie('2','What a girl wants', 'Daphne, an American teenager, searches her prominent politician father from UK', 'Comedy')
        self.assertEqual(self.testSrv.search_movie('prETTy'), [Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance')])
        self.assertEqual(self.testSrv.search_movie('AN'), [Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance'), Movie('2','What a girl wants', 'Daphne, an American teenager, searches her prominent politician father from UK', 'Comedy')])
        self.assertEqual(self.testSrv.search_movie(' '), [Movie('1', 'Pretty Woman', 'A rich entrepreneur (Gere) hires a prostitute (Roberts), eventually falling in love with her.', 'Romance'), Movie('2','What a girl wants', 'Daphne, an American teenager, searches her prominent politician father from UK', 'Comedy')])
        self.assertRaisesRegex(RepositoryError, 'No movie found!', self.testSrv.search_movie, 'Schindler')


class TestMovieValidators(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.testValidator = ValidMovie()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_validate(self):
        #With regard to the previous 2do, here you test only the validator's functionalities
        movie = Movie('a', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.assertRaisesRegex(ValidationError, 'Invalid id! ', self.testValidator.validate, movie)
        movie = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romantic comedy')
        self.assertRaisesRegex(ValidationError, 'Invalid genre! ', self.testValidator.validate, movie)
        movie = Movie('a', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romantic comedy')
        self.assertRaisesRegex(ValidationError, 'Invalid id! Invalid genre! ', self.testValidator.validate, movie)

    def test_validate_update(self):
        self.assertRaisesRegex(ValidationError, 'Invalid attribute!', self.testValidator.validate_update, 'movie_id', '12')
        self.assertRaisesRegex(ValidationError, 'Invalid genre!', self.testValidator.validate_update, 'genre', 'Romantic Comedy')

    def test_validate_id(self):
        self.assertRaisesRegex(ValidationError, 'Invalid movie id!', self.testValidator.validate_movie_id, '-1')

class TestMovieRepository(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.testRepo = RepoMovie()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_add_movie(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        movie2 = Movie('1','What a girl wants', 'Daphne, an American teenager, searches her prominent politician father from UK', 'Comedy')
        self.assertRaisesRegex(RepositoryError, 'Movie id already in list!', self.testRepo.add_movie, movie2)

    def test_remove_movie(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        self.testRepo.remove_movie('1')
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testRepo.remove_movie, '1')

    def test_update_movie(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        self.testRepo.update_movie('1', 'genre', 'Comedy')
        self.assertEqual(self.testRepo.search_movie_by_id('1'), Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Comedy'))
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testRepo.update_movie , '2', 'description', 'Starring Amanda Bynes, Colin Firth and Kelly Preston')

    def test_get_all_movies(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        other_dict_iter = IterableDictionary()
        other_dict_iter.add('1', Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance'))
        self.assertEqual(self.testRepo.get_all_movies(), other_dict_iter)
        self.assertEqual(len(self.testRepo), 1)
        self.testRepo.remove_movie('1')
        other_dict_iter = IterableDictionary()
        self.assertEqual(self.testRepo.get_all_movies(), other_dict_iter)
        self.assertEqual(len(self.testRepo), 0)

    def test_search_movie_by_id(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        self.assertEqual(self.testRepo.search_movie_by_id('1'), Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance'))
        self.assertRaisesRegex(RepositoryError, 'Movie not in list!', self.testRepo.search_movie_by_id, '2')

    def test_search_movie(self):
        movie1 = Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')
        self.testRepo.add_movie(movie1)
        self.assertRaisesRegex(RepositoryError, 'No movie found', self.testRepo.search_movie, '1 Pretty')
        self.assertEqual(self.testRepo.search_movie(' riCH'), [Movie('1', 'Pretty Woman', 'Starring Richard Gere and Julia Roberts', 'Romance')])