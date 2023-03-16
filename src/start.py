from ui.ui import MovieRental_UI
from ui.gui import MovieRental_GUI
from src.repository.repositories import RepoMovie, RepoClient, RepoRental
from src.repository.textfile_repository import TextFileRepoMovie, TextFileRepoClient, TextFileRepoRental
from src.repository.binaryfile_repository import BinaryFileRepoMovie, BinaryFileRepoClient, BinaryFileRepoRental
from src.repository.validators import ValidClient, ValidRental, ValidMovie
from src.services.services import SrvMovie, SrvRental, SrvClient, SrvUndoRedo, SrvRemove

#if __name__ == '__main__':
 #   unittest.main()


""""
1,  Big Fat Greek Wedding,  ,  Comedy
2,  The Life Ahead,  ,  Drama
3,  Almost Famous,  ,  Drama
4,  Pretty Woman,  ,  Romance
5,  Monster in Law,  ,  Comedy
6,  La vita e bella,  ,  Drama
7,  Secrets of the Saqqara Tomb,  ,  Documentary
8,  Bridget Jones` Diary,  ,  Comedy
9, Polar Express, With Tom Hanks as voice actor, Animation
"""

class Settings:
    def __init__(self):
        self.__properties = {}
        self.__load_properties()

    def __load_properties(self):
        with open("settings.properties", "rt") as settings:
            lines = settings.readlines()
            for line in lines:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    self.__properties[key] = value

    def get_repositories(self):
        """"
        Returns a list of repositories (as objects of TextFileRepoMovie/BinaryFileRepoMovie/RepoMovie, TextFileRepoClient/BinaryFileRepoClient/RepoClient,
             TextFileRepoRental/BinaryFileRepoRental/RepoRental classes respectively)
        """

        if self.__properties['repository'] == 'textfiles':
            repoMovies = TextFileRepoMovie(self.__properties['movies'])
            repoClient = TextFileRepoClient(self.__properties['clients'])
            repoRental = TextFileRepoRental(self.__properties['rentals'], repoClient, repoMovies)
            return [repoMovies, repoClient, repoRental]
        elif self.__properties['repository'] == 'binaryfiles':
            repoMovies = BinaryFileRepoMovie(self.__properties['movies'])
            repoClient = BinaryFileRepoClient(self.__properties['clients'])
            repoRental = BinaryFileRepoRental(self.__properties['rentals'], repoClient, repoMovies)
            return [repoMovies, repoClient, repoRental]
        elif self.__properties['repository'] == 'runtime':
            repoMovies = RepoMovie()
            repoClient = RepoClient()
            repoRental = RepoRental(repoClient, repoMovies)
            return [repoMovies, repoClient, repoRental]

    def get_ui(self):
        """"
        returns whether 'UI' or 'GUI'
        """
        return self.__properties['ui'].lower()



class StartupData(SrvMovie, SrvClient, SrvRental):

    def __init__(self, serviceMovie, serviceClient, serviceRental):
        self.__srvMovie = serviceMovie
        self.__srvClient = serviceClient
        self.__srvRental = serviceRental

    def generate(self):
        self.__srvMovie._generate_random_movies()
        self.__srvClient._generate_random_clients()
        self.__srvRental._generate_random_rentals()


settings = Settings()
repoMovies, repoClient, repoRental = settings.get_repositories()


validMovie = ValidMovie()
validClient = ValidClient()
validRental = ValidRental()

#dependency injection - what we did here...

serviceUndoRedo = SrvUndoRedo()
serviceMovie = SrvMovie(repoMovies, validMovie, serviceUndoRedo)
serviceClient = SrvClient(repoClient, validClient, serviceUndoRedo)
serviceRental = SrvRental(repoClient, repoMovies, repoRental, validRental, serviceUndoRedo)
serviceRemove = SrvRemove(serviceUndoRedo, repoMovies, repoClient, repoRental)

ui = settings.get_ui()

# startup_data = StartupData(serviceMovie, serviceClient, serviceRental)
# startup_data.generate()

# print("""How will you use the application?
#     1. In console
#     2. With GUI""")
#
# mode = input('>>>')

if ui == 'ui':
    console = MovieRental_UI(serviceMovie, serviceClient, serviceRental, serviceRemove, serviceUndoRedo)
    console.start_console()
elif ui == 'gui':
    console = MovieRental_GUI(serviceMovie, serviceClient, serviceRental, serviceRemove, serviceUndoRedo)
    console.start()