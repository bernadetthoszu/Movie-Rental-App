from src.exceptions import ValidationError, RepositoryError, UndoRedoError

class MovieRental_UI :

    def __init__(self, srvMovie, srvClient, srvRental, srvRemove, srvUndoRedo):
        self.__serviceMovie = srvMovie
        self.__serviceClient = srvClient
        self.__serviceRental = srvRental
        self.__serviceRemove = srvRemove
        self.__serviceUndoRedo = srvUndoRedo


    def start_console(self):

        print("Welcome, cinephile!")
        print("""Actions: 
    add movie/client
    remove movie/client
    update movie/client
    list movies/clients/rentals.txt
    rent movie
    return movie
    search movie/client
    most rented movies
    most active clients
    late rentals.txt
    undo
    redo
    exit""")

        while True:


            print('\nType your action')
            cmd = input('>>>')


            if cmd == 'exit' :
                return

            elif cmd == '' :
                continue

            elif cmd == 'add movie' :
                movie_id = input('movie id : ')
                title = input('title : ')
                description = input('description : ')
                genre = input('genre : ')
                try :
                    self.__serviceMovie.add_movie(movie_id, title, description, genre)
                except ValidationError as ve :
                    print(str(ve))
                except RepositoryError as re :
                    print(str(re))

            elif cmd == 'remove movie' :
                print('What movie do you want to remove? (give id)')
                movie_id = input('>>>')
                try:
                    self.__serviceRemove.remove_movie(movie_id)
                except RepositoryError as re :
                    print(str(re))

            elif cmd == 'update movie' :
                print('What movie do you want to update? (give id)')
                movie_id = input('>>>')
                print('What do you want to update? (description or genre)')
                attribute = input('>>>')
                print('Give new attribute')
                new_value = input('>>>')
                try:
                    self.__serviceMovie.update_movie(movie_id, attribute, new_value)
                except RepositoryError as re :
                    print(str(re))
                except ValidationError as ve :
                    print(str(ve))

            elif cmd == 'list movies' :
                movies = self.__serviceMovie.get_all_movies()
                movies_string = ''
                if len(movies) > 0 :
                    for m in movies:
                        movies_string += '\n  ' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: ' + str(m.get_description()) + '\nGenre: ' + str(m.get_genre())
                    print(movies_string)
                else :
                    print('No movies to show!')

            elif cmd == 'add client' :
                client_id = input('client id : ')
                name = input('name : ')
                try :
                    self.__serviceClient.add_client(client_id, name)
                except ValidationError as ve :
                    print(str(ve))
                except RepositoryError as re :
                    print(str(re))

            elif cmd == 'remove client' :
                print('Who do you want to remove? (give client id)')
                client_id = input('>>>')
                try:
                    self.__serviceRemove.remove_client(client_id)
                except ValidationError as ve :
                    print(str(ve))
                except RepositoryError as re :
                    print(str(re))

            elif cmd == 'update client' :
                print('Whose info do you want to update? (give client_id)')
                client_id = input('>>>')
                print('Introduce new name')
                new_value = input('>>>')
                try:
                    self.__serviceClient.update_client(client_id, new_value)
                except ValidationError as ve :
                    print(str(ve))
                except RepositoryError as re :
                    print(str(re))

            elif cmd == 'list clients' :
                clients = self.__serviceClient.get_all_clients()
                clients_string = ''
                if len(clients) > 0 :
                    for c in clients:
                        clients_string += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
                    print(clients_string)
                else :
                    print('No more clients left!')

            elif cmd == 'rent movie' :
                print('Who rents? (give client id)')
                client_id = input('>>>')
                print('Which movie? (give id)')
                movie_id = input('>>>')
                rental_id = input('Rental id: ')
                print('Rented date: ')
                rented_day = input('day: ')
                rented_month = input('month: ')
                rented_year = input('year: ')
                rented_date = str(rented_year) + '-' + str(rented_month) + '-' + str(rented_day)
                print('Due date: ')
                due_day = input('day: ')
                due_month = input('month: ')
                due_year  = input('year: ')
                due_date = str(due_year) + '-'+ str(due_month) + '-' + str(due_day)
                try:
                    self.__serviceRental.rent_movie(rental_id, client_id, movie_id, rented_date, due_date)
                except ValidationError as ve:
                    print(str(ve))
                except RepositoryError as re:
                    print(str(re))

            elif cmd == 'list rentals.txt':
                rentals = self.__serviceRental.get_all_rentals()
                rentals_string = ''
                if len(rentals) > 0:
                    for r in rentals:
                        rentals_string += '\n' + str(r.get_rental_id()) + ' - ' + str(r.get_client_id())+ ' - ' + str(r.get_movie_id())+ ' - ' + str(r.get_rented_date())+ ' - ' + str(r.get_due_date())+ ' - ' + str(r.get_returned_date())
                    print(rentals_string)
                else:
                    print('No rentals.txt registered!')

            elif cmd == 'return movie' :
                print('Who returns? (give client id)')
                client_id = input('>>>')
                print('Your active rentals.txt are:')
                try:
                    client_rentals = self.__serviceRental.get_rentals_of_client_ui(client_id)
                    if client_rentals == []:
                        print('No active rentals.txt!')
                    else:
                        for r in client_rentals:
                            print('Rental id: ' + str(r[0]) + '; Movie: ' + str(r[1]))
                        print('Which rental do you want to resolve? (give id from above)')
                        rental_id = input('>>>')
                        try:
                            self.__serviceRental.return_movie(rental_id, client_id)
                        except ValidationError as ve:
                            print(str(ve))
                        except RepositoryError as re:
                            print(str(re))
                        except Exception as e:
                            print(str(e))
                except RepositoryError as re:
                    print(str(re))

            elif cmd == 'search movie':
                string_movie = input('>>>')
                try:
                    movies = self.__serviceMovie.search_movie(string_movie)
                    movies_str = ''
                    for m in movies:
                        movies_str += '\n' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: ' + str(m.get_description()) + '\nGenre: ' + str(m.get_genre())
                    print(movies_str)
                except RepositoryError as re:
                    print(str(re))

            elif cmd == 'search client':
                string_client = input('>>>')
                try:
                    clients = self.__serviceClient.search_client(string_client)
                    clients_str = ''
                    for c in clients:
                        clients_str += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
                    print(clients_str)
                except RepositoryError as re:
                    print(str(re))

            elif cmd == 'most rented movies':
                exception_raised = False
                stats = []
                try:
                    stats = self.__serviceRental.most_rented_movies()
                except Exception as e:
                    print(str(e))
                    exception_raised = True
                if exception_raised is False and stats == []:
                    print('No movies in list!')
                else:
                    stats_str = ''
                    for m in stats:
                        stats_str += '\n' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: ' + str(m.get_description()) + '\nGenre: ' + str(m.get_genre())
                    print(stats_str)

            elif cmd == 'most active clients':
                exception_raised = False
                stats = []
                try:
                    stats = self.__serviceRental.most_active_clients()
                except Exception as e:
                    print(str(e))
                    exception_raised = True
                if exception_raised is False and stats == []:
                    print('No clients in list!')
                else:
                    stats_str = ''
                    for c in stats:
                        stats_str += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
                    print(stats_str)

            elif cmd == 'late rentals':
                exception_raised = False
                stats = []
                try:
                    stats = self.__serviceRental.late_rentals()
                except Exception as e:
                    print(str(e))
                    exception_raised = True
                if exception_raised is False and stats == []:
                    print('No late rentals!')
                else:
                    stats_str = ''
                    for r in stats:
                        stats_str += '\nrental: ' + str(r.get_rental_id()) + ' delay: ' + str(r.get_return_delay()) + ' days'
                    print(stats_str)

            elif cmd == 'undo':
                try:
                    self.__serviceUndoRedo.undo()
                except UndoRedoError as ure:
                    print(str(ure))

            elif cmd == 'redo':
                try:
                    self.__serviceUndoRedo.redo()
                except UndoRedoError as ure:
                    print(str(ure))

            else :
                print('Your command is invalid!')
