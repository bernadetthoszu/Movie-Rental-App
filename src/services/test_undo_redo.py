import unittest
from src.services.services import SrvUndoRedo, SrvRental, SrvMovie, SrvClient, SrvRemove
from src.repository.repositories import RepoRental, RepoMovie, RepoClient
from src.repository.validators import ValidMovie, ValidClient, ValidRental
from src.exceptions import UndoRedoError

class TestUndoRedoService(unittest.TestCase, SrvUndoRedo):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.testSrv = SrvUndoRedo()
        self.validClient = ValidClient()
        self.validMovie = ValidMovie()
        self.validRental = ValidRental()
        self.repoClient = RepoClient()
        self.repoMovies = RepoMovie()
        self.repoRental = RepoRental(self.repoClient, self.repoMovies)
        self.srvClient = SrvClient(self.repoClient, self.validClient, self.testSrv)
        #self.srvClient.add_client('1', 'Lucy')
        self.srvMovies = SrvMovie(self.repoMovies, self.validMovie, self.testSrv)
        #self.srvMovies.add_movie('1', 'Pretty Woman', '1990', 'Romance')
        self.srvRental = SrvRental(self.repoClient, self.repoMovies, self.repoRental, self.validRental, self.testSrv)
        self.srvRemove = SrvRemove(self.testSrv, self.repoMovies, self.repoClient, self.repoRental)
        #self.srvRental.rent_movie('1', '1', '1', '2021-11-14', '2121-11-20')

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_record(self):
        self.srvMovies.add_movie('1', 'Pretty Woman', '1990', 'Romance')
        self.assertEqual(len(self.testSrv._history), 1)
        self.assertEqual(self.testSrv._index, 0)

    def test_undo_redo(self):
        self.srvMovies.add_movie('1', 'Pretty Woman', '1990', 'Romance')
        self.testSrv.undo()
        self.assertEqual(self.testSrv._index, -1)
        self.assertRaisesRegex(UndoRedoError, 'No more undos!', self.testSrv.undo)
        self.testSrv.redo()
        self.assertEqual(self.testSrv._index, 0)
        self.srvClient.add_client('1', 'Lucy')
        self.srvRental.rent_movie('1', '1', '1', '2021-11-14', '2021-12-14')
        # index = 2, len(history) = 3
        self.srvRemove.remove_movie('1')
        self.assertEqual(len(self.repoMovies), 0)
        self.assertEqual(len(self.repoRental), 0)
        self.testSrv.undo()
        self.assertEqual(len(self.repoMovies), 1)
        self.assertEqual(len(self.repoRental), 1)
        self.testSrv.redo()
        self.assertEqual(len(self.repoMovies), 0)
        self.assertEqual(len(self.repoRental), 0)

