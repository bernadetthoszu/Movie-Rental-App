import unittest
from src.services.services import SrvClient, SrvUndoRedo
from src.repository.repositories import RepoClient
from src.repository.validators import ValidClient
from src.domain.entities import Client
from src.exceptions import ValidationError, RepositoryError
from src.services.sort_filter import IterableDictionary

class TestClientServices(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        testRepo = RepoClient()
        testValidator = ValidClient()
        testSrvUndoRedo = SrvUndoRedo()
        self.testSrv = SrvClient(testRepo, testValidator, testSrvUndoRedo)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_add_movie(self):
        self.testSrv.add_client('1', 'Lucy')
        self.assertEqual(self.testSrv.search_client_by_id('1'), Client('1', 'Lucy'))
        self.assertRaisesRegex(RepositoryError, 'Client id already in list!', self.testSrv.add_client, '1', 'Lucy')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testSrv.add_client, '-1', 'Lucy')

    def test_remove_client(self):
        self.testSrv.add_client('1', 'Lucy')
        self.testSrv.remove_client('1')
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testSrv.remove_client, '1')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testSrv.remove_client, '-1')

    def test_update_client(self):
        self.testSrv.add_client('1', 'Lucy')
        self.testSrv.update_client('1', 'Mary')
        self.assertEqual(self.testSrv.search_client_by_id('1'), Client('1', 'Mary'))
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testSrv.update_client, '2', 'Mary')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testSrv.update_client, '-1', 'Mary')

    def test_get_all_clients(self):
        self.testSrv.add_client('1', 'Lucy')
        other_iter_dict = IterableDictionary()
        other_iter_dict.add('1', Client('1', 'Lucy'))
        self.assertEqual(self.testSrv.get_all_clients(), other_iter_dict)
        self.testSrv.remove_client('1')
        other_iter_dict2 = IterableDictionary()
        self.assertEqual(self.testSrv.get_all_clients(), other_iter_dict2)

    def test_search_client_by_id(self):
        self.testSrv.add_client('1', 'Lucy')
        self.assertEqual(self.testSrv.search_client_by_id('1'), Client('1', 'Lucy'))
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testSrv.search_client_by_id, '2')

    def test_search_client(self):
        self.testSrv.add_client('1', 'Lucy')
        self.testSrv.add_client('2', 'Darcy')
        self.assertEqual(self.testSrv.search_client('luc'), [Client('1', 'Lucy')])
        self.assertEqual(self.testSrv.search_client('c'), [Client('1', 'Lucy'), Client('2', 'Darcy')])
        self.assertRaisesRegex(RepositoryError, 'No client found!', self.testSrv.search_client, 'Ben')


class TestClientValidator(unittest.TestCase):

    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.testValidator = ValidClient()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_validate_id(self):
        self.testValidator.validate_client_id('123')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testValidator.validate_client_id, '1a')
        self.assertRaisesRegex(ValidationError, 'Invalid client id!', self.testValidator.validate_client_id, '-12')


class TestClientRepository(unittest.TestCase):

    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.testRepo = RepoClient()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_add_client(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        self.assertEqual(self.testRepo.search_client_by_id('1'), client1)
        client2 = Client('1', 'Mary')
        self.assertRaisesRegex(RepositoryError, 'Client id already in list!', self.testRepo.add_client, client2)

    def test_remove_client(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        self.testRepo.remove_client('1')
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testRepo.remove_client, '1')

    def test_update_client(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        self.testRepo.update_client('1', 'Mary')
        self.assertEqual(self.testRepo.search_client_by_id('1'), Client('1', 'Mary'))
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testRepo.update_client, '2', 'Ben')

    def test_get_all_clients(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        other_iter_dict = IterableDictionary()
        other_iter_dict.add('1', Client('1', 'Lucy'))
        self.assertEqual(self.testRepo.get_all_clients(), other_iter_dict)
        self.assertEqual(len(self.testRepo), 1)
        self.testRepo.remove_client('1')
        other_iter_dict2 = IterableDictionary()
        self.assertEqual(self.testRepo.get_all_clients(), other_iter_dict2)
        self.assertEqual(len(self.testRepo), 0)

    def test_search_client_by_id(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        self.assertEqual(self.testRepo.search_client_by_id('1'), Client('1', 'Lucy'))
        self.assertRaisesRegex(RepositoryError, 'Inexisting client!', self.testRepo.search_client_by_id, '2')

    def test_search_client(self):
        client1 = Client('1', 'Lucy')
        self.testRepo.add_client(client1)
        self.assertEqual(self.testRepo.search_client('1'), [Client('1', 'Lucy')])
        self.assertRaisesRegex(RepositoryError, 'No client found!', self.testRepo.search_client, '2')
