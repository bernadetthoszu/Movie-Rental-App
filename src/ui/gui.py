import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from src.exceptions import ValidationError, UndoRedoError, RepositoryError

class MovieRental_GUI:
    def __init__(self, serviceMovie, serviceClient, serviceRental, serviceRemove, serviceUndoRedo):
        self.__main_window = Tk()    #toplevel window, known as the root window, which serves as the main window of the application
        self.__secondary_window = None
        self.__secondary_window_frame = None
        self.__movie_client_rental_grid = None
        self.__undo_redo_exit_frame = None
        self.__commands_frame = None
        self.__srvMovie = serviceMovie
        self.__srvClient = serviceClient
        self.__srvRental = serviceRental
        self.__srvRemove = serviceRemove
        self.__srvUndoRedo = serviceUndoRedo

        self.__movie_id = None
        self.__title = None
        self.__description = None
        self.__genre = None
        self.__attribute = None
        self.__new_value = None
        self.__client_id = None
        self.__name = None
        self.__search_string = None
        self.__rental_id = None
        self.__rented_date = None
        self.__due_date = None
        self.__client_rentals = None

    def start(self):
        self.__main_window.title("Movie Rental")

        greeting = ttk.Label(text='Welcome, cinephile!')
        greeting.pack()

        commands_frame = ttk.Frame(self.__main_window)    #syntax: w = Frame ( master, option, ... )
        commands_frame.pack()
        commands_frame.anchor(CENTER)
        self.__commands_frame = commands_frame

        movie_client_rental_grid = ttk.Frame(commands_frame)
        movie_client_rental_grid.pack()
        movie_client_rental_grid.anchor(CENTER)
        self.__movie_client_rental_grid = movie_client_rental_grid

        # window.rowconfigure(0, minsize=50, weight=1)
        # window.columnconfigure([0, 1, 2], minsize=50, weight=1)

        for x in range(0, 6):
            movie_client_rental_grid.rowconfigure(x, minsize=30)

        for x in range(0, 3):
            movie_client_rental_grid.columnconfigure(x, minsize=150)

        self.btn1 = ttk.Button(movie_client_rental_grid, text='Add movie', command=self.__add_movie_pressed)
        self.btn1.grid(row=0, column=0)

        self.btn2 = ttk.Button(movie_client_rental_grid, text='Add client', command=self.__add_client_pressed)
        self.btn2.grid(row=0, column=1)

        self.btn3 = ttk.Button(movie_client_rental_grid, text='Remove movie', command=self.__remove_movie_pressed)
        self.btn3.grid(row=1, column=0)

        self.btn4 = ttk.Button(movie_client_rental_grid, text='Remove client', command=self.__remove_client_pressed)
        self.btn4.grid(row=1, column=1)

        self.btn5 = ttk.Button(movie_client_rental_grid, text='Update movie', command=self.__update_movie_pressed)
        self.btn5.grid(row=2, column=0)

        self.btn6 = ttk.Button(movie_client_rental_grid, text='Update client', command=self.__update_client_pressed)
        self.btn6.grid(row=2, column=1)

        self.btn7 = ttk.Button(movie_client_rental_grid, text='List movies', command=self.__list_movies_pressed)
        self.btn7.grid(row=3, column=0)

        self.btn8 = ttk.Button(movie_client_rental_grid, text='List clients',command=self.__list_clients_pressed)
        self.btn8.grid(row=3, column=1)

        self.btn9 = ttk.Button(movie_client_rental_grid, text='Most rented movies', command=self.__most_rented_movies_pressed)
        self.btn9.grid(row=4, column=0)

        self.btn10 = ttk.Button(movie_client_rental_grid, text='Most active clients', command=self.__most_active_clients_pressed)
        self.btn10.grid(row=4, column=1)

        self.btn11 = ttk.Button(movie_client_rental_grid, text='Search movie', command=self.__search_movie_pressed)
        self.btn11.grid(row=5, column=0)

        self.btn12 = ttk.Button(movie_client_rental_grid, text='Search client', command=self.__search_client_pressed)
        self.btn12.grid(row=5, column=1)

        self.btn13 = ttk.Button(movie_client_rental_grid, text='Rent movie', command=self.__rent_movie_pressed)
        self.btn13.grid(row=0, column=2)

        self.btn14 = ttk.Button(movie_client_rental_grid, text='Return movie', command=self.__return_movie_pressed)
        self.btn14.grid(row=1, column=2)

        self.btn15 = ttk.Button(movie_client_rental_grid, text='List rentals', command=self.__list_rentals_pressed)
        self.btn15.grid(row=2, column=2)

        self.btn16 = ttk.Button(movie_client_rental_grid, text='Late rentals', command=self.__late_rentals_pressed)
        self.btn16.grid(row=3, column=2)

        undo_redo_exit_frame = ttk.Frame(commands_frame)
        undo_redo_exit_frame.anchor(CENTER)
        undo_redo_exit_frame.pack()
        self.__undo_redo_exit_frame = undo_redo_exit_frame

        self.btn17 = ttk.Button(undo_redo_exit_frame, text='Undo', command=self.__undo_pressed)
        self.btn17.anchor(CENTER)
        self.btn17.pack()

        self.btn18 = ttk.Button(undo_redo_exit_frame, text='Redo', command=self.__redo_pressed)
        self.btn18.anchor(CENTER)
        self.btn18.pack()

        self.btn19 = ttk.Button(undo_redo_exit_frame, text='EXIT', command=self.__exit_pressed)
        self.btn19.anchor(CENTER)
        self.btn19.pack()



        self.__main_window.mainloop()



    """"
    Event handlers
    """

    def __add_movie_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Add movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Movie ID: ")
        lbl.grid(row=0, column=0)
        self.__movie_id = ttk.Entry(frame, {}, width=106)
        self.__movie_id.grid(row=0, column=1)

        lbl = ttk.Label(frame, text="Title: ")
        lbl.grid(row=1, column=0)
        self.__title = ttk.Entry(frame, {}, width=106)
        self.__title.grid(row=1, column=1)

        lbl = ttk.Label(frame, text="Description: ")
        lbl.grid(row=2, column=0)
        self.__description = Text(frame, {}, height=8)
        self.__description.grid(row=2, column=1)

        lbl = ttk.Label(frame, text="Genre: ")
        lbl.grid(row=3, column=0)
        self.__genre = ttk.Entry(frame, {}, width=106)
        self.__genre.grid(row=3, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Add movie", command=self.__call_add_movie)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_add_movie(self):
        try:
            self.__srvMovie.add_movie(self.__movie_id.get(), self.__title.get(), (self.__description.get("1.0", "8.100")).strip(), self.__genre.get())
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __add_client_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Add client")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Client ID: ")
        lbl.grid(row=0, column=0)
        self.__client_id = ttk.Entry(frame, {}, width=100)
        self.__client_id.grid(row=0, column=1)

        lbl = ttk.Label(frame, text="Name: ")
        lbl.grid(row=1, column=0)
        self.__name = ttk.Entry(frame, {}, width=100)
        self.__name.grid(row=1, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Add client", command=self.__call_add_client)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_add_client(self):
        try:
            self.__srvClient.add_client(self.__client_id.get(), self.__name.get())
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __remove_movie_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Remove movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Movie ID: ")
        lbl.grid(row=0, column=0)
        self.__movie_id = ttk.Entry(frame, {}, width=30)
        self.__movie_id.grid(row=0, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Remove movie", command=self.__call_remove_movie)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_remove_movie(self):
        try:
            self.__srvRemove.remove_movie(self.__movie_id.get())
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __remove_client_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Remove client")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Client ID: ")
        lbl.grid(row=0, column=0)
        self.__client_id = ttk.Entry(frame, {}, width=30)
        self.__client_id.grid(row=0, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Remove client", command=self.__call_remove_client)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_remove_client(self):
        try:
            self.__srvRemove.remove_client(self.__client_id.get())
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __update_movie_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Update movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Movie ID: ")
        lbl.grid(row=0, column=0)
        self.__movie_id = ttk.Entry(frame, {}, width=30)
        self.__movie_id.grid(row=0, column=1)

        lbl = ttk.Label(frame, text="Attribute: ")
        lbl.grid(row=1, column=0)
        self.__attribute = ttk.Entry(frame, {}, width=30)
        self.__attribute.grid(row=1, column=1)

        lbl = ttk.Label(frame, text="New value: ")
        lbl.grid(row=2, column=0)
        self.__new_value = Entry(frame, {}, width=30)
        self.__new_value.grid(row=2, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Update movie", command=self.__call_update_movie)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_update_movie(self):
        try:
            self.__srvMovie.update_movie(self.__movie_id.get(), self.__attribute.get(), self.__new_value.get())
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        self.__secondary_window.destroy()

    def __update_client_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Update movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Client ID: ")
        lbl.grid(row=0, column=0)
        self.__client_id = ttk.Entry(frame, {}, width=30)
        self.__client_id.grid(row=0, column=1)

        lbl = ttk.Label(frame, text="New name: ")
        lbl.grid(row=1, column=0)
        self.__new_value = ttk.Entry(frame, {}, width=30)
        self.__new_value.grid(row=1, column=1)


        execute_btn = ttk.Button(self.__secondary_window, text="Update client", command=self.__call_update_client)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_update_client(self):
        try:
            self.__srvClient.update_client(self.__client_id.get(), self.__new_value.get())
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        self.__secondary_window.destroy()

    def __list_movies_pressed(self):
        movies = self.__srvMovie.get_all_movies()  #type IterableDictionary !!!
        movies_string = ''
        if len(movies) > 0:
            for m_id in movies:
                m = movies[m_id]
                movies_string += '\n  ' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: '.ljust(13) + str(
                    m.get_description()) + '\nGenre: ' + str(m.get_genre())
            messagebox.showinfo("List movies", movies_string)
        else:
            messagebox.showinfo("List movies", 'No movies to show!')

    def __list_clients_pressed(self):
        clients = self.__srvClient.get_all_clients()
        clients_string = ''
        if len(clients) > 0:
            for c_id in clients:
                c = clients[c_id]
                clients_string += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
            messagebox.showinfo("List clients", clients_string)
        else:
            messagebox.showinfo("List clients", 'No more clients left!')

    def __search_movie_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Search movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Search: ")
        lbl.grid(row=0, column=0)
        self.__search_string = ttk.Entry(frame, {}, width=50)
        self.__search_string.grid(row=0, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Search movie", command=self.__call_search_movie)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_search_movie(self):
        try:
            movies = self.__srvMovie.search_movie(self.__search_string.get())
            movies_str = ''
            for m in movies:
                movies_str += '\n' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: ' + str(
                    m.get_description()) + '\nGenre: ' + str(m.get_genre())
            messagebox.showinfo("Found movies", movies_str)
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __search_client_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Search client")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Search: ")
        lbl.grid(row=0, column=0)
        self.__search_string = ttk.Entry(frame, {}, width=50)
        self.__search_string.grid(row=0, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Search client", command=self.__call_search_client)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_search_client(self):
        try:
            clients = self.__srvClient.search_client(self.__search_string.get())
            clients_str = ''
            for c in clients:
                clients_str += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
            messagebox.showinfo("Found clients", clients_str)
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __most_rented_movies_pressed(self):
        exception_raised = False
        stats = []
        try:
            stats = self.__srvRental.most_rented_movies()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
            exception_raised = True
        if exception_raised is False and stats == []:
            messagebox.showinfo("Most rented movies", 'No movies in list!')
        else:
            stats_str = ''
            for m in stats:
                stats_str += '\n' + str(m.get_movie_id()) + ': ' + str(m.get_title()) + '\nDescription: ' + str(
                    m.get_description()) + '\nGenre: ' + str(m.get_genre())
            messagebox.showinfo("Most rented movies", stats_str)

    def __most_active_clients_pressed(self):
        exception_raised = False
        stats = []
        try:
            stats = self.__srvRental.most_active_clients()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
            exception_raised = True
        if exception_raised is False and stats == []:
            messagebox.showinfo("Most active clients", 'No clients in list!')
        else:
            stats_str = ''
            for c in stats:
                stats_str += '\n' + str(c.get_client_id()) + ': ' + str(c.get_name())
            messagebox.showinfo("Most active clients", stats_str)

    def __rent_movie_pressed(self):
        # print('Who rents? (give client id)')
        # client_id = input('>>>')
        # print('Which movie? (give id)')
        # movie_id = input('>>>')
        # rental_id = input('Rental id: ')
        # print('Rented date: ')
        # rented_day = input('day: ')
        # rented_month = input('month: ')
        # rented_year = input('year: ')
        # rented_date = str(rented_year) + '-' + str(rented_month) + '-' + str(rented_day)
        # print('Due date: ')
        # due_day = input('day: ')
        # due_month = input('month: ')
        # due_year = input('year: ')
        # due_date = str(due_year) + '-' + str(due_month) + '-' + str(due_day)
        # try:
        #     self.__serviceRental.rent_movie(rental_id, client_id, movie_id, rented_date, due_date)
        # except ValidationError as ve:
        #     print(str(ve))
        # except RepositoryError as re:
        #     print(str(re))

        self.__secondary_window = Tk()
        self.__secondary_window.title("Rent movie")

        frame = ttk.Frame(self.__secondary_window)
        frame.pack()
        self.__secondary_window_frame = frame

        lbl = ttk.Label(frame, text="Rental ID: ")
        lbl.grid(row=0, column=0)
        self.__rental_id = ttk.Entry(frame, {}, width=106)
        self.__rental_id.grid(row=0, column=1)

        lbl = ttk.Label(frame, text="Client ID: ")
        lbl.grid(row=1, column=0)
        self.__client_id = ttk.Entry(frame, {}, width=106)
        self.__client_id.grid(row=1, column=1)

        lbl = ttk.Label(frame, text="Movie ID: ")
        lbl.grid(row=2, column=0)
        self.__movie_id = Entry(frame, {}, width=106)
        self.__movie_id.grid(row=2, column=1)

        lbl = ttk.Label(frame, text="Rented date (ISO format): ")
        lbl.grid(row=3, column=0)
        self.__rented_date = ttk.Entry(frame, {}, width=106)
        self.__rented_date.grid(row=3, column=1)

        lbl = ttk.Label(frame, text="Due date (ISO format): ")
        lbl.grid(row=4, column=0)
        self.__due_date = ttk.Entry(frame, {}, width=106)
        self.__due_date.grid(row=4, column=1)

        execute_btn = ttk.Button(self.__secondary_window, text="Rent movie", command=self.__call_rent_movie)
        execute_btn.anchor(CENTER)
        execute_btn.pack()

        self.__secondary_window.mainloop()

    def __call_rent_movie(self):
        try:
            self.__srvRental.rent_movie(self.__rental_id.get(), self.__client_id.get(), self.__movie_id.get(), self.__rented_date.get(), self.__due_date.get())
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        self.__secondary_window.destroy()

    def __return_movie_pressed(self):
        self.__secondary_window = Tk()
        self.__secondary_window.title("Return movie")

        client_frame = ttk.Frame(self.__secondary_window)
        client_frame.pack()

        lbl = ttk.Label(client_frame, text="Client ID: ")
        lbl.grid(row=0, column=0)
        self.__client_id = ttk.Entry(client_frame, {})
        self.__client_id.grid(row=0, column=1)
        self.__client_id.bind("<Return>", self.__handle_rentals_of_client)

        self.__secondary_window.mainloop()

    def __handle_rentals_of_client(self, event):
        #messagebox.showinfo("YOU DID IT!", "Tab press is handled, yay!")
        try:
            self.__srvClient.search_client(self.__client_id.get())
        except RepositoryError:
            messagebox.showinfo("Error", 'Inexisting client!')
            self.__secondary_window.destroy()
        self.__client_rentals = self.__srvRental.get_rentals_of_client_ui(self.__client_id.get())

        if self.__client_rentals == []:
            messagebox.showinfo("Return movie", 'Client has no active rentals.txt!')
            self.__secondary_window.destroy()
        else:
            frame = ttk.Frame(self.__secondary_window)
            frame.pack()
            self.__secondary_window_frame = frame

            lbl = ttk.Label(frame, text="Active rentals.txt: ")
            lbl.pack()
            txt = Text(frame, {}, width = 50, height=8)
            for r in self.__client_rentals:
                txt.insert(f"{self.__client_rentals.index(r)}.0", '\n' + 'Rental id: ' + str(r[0]) + '; Movie: ' + str(r[1]))
            txt.pack()

            lbl = ttk.Label(frame, text="Which rental do you want to resolve? (give id from above)")
            lbl.pack()
            self.__rental_id = ttk.Entry(frame, {}, width=50)
            self.__rental_id.pack()

            execute_btn = ttk.Button(frame, text="Return rental", command=self.__call_return_movie)
            execute_btn.pack()

            self.__secondary_window_frame.mainloop()

    def __call_return_movie(self):
        try:
            self.__srvRental.return_movie(self.__rental_id.get(), self.__client_id.get())
        except ValidationError as ve:
            messagebox.showinfo("Error", str(ve))
        except RepositoryError as re:
            messagebox.showinfo("Error", str(re))
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        self.__secondary_window.destroy()

    def __list_rentals_pressed(self):
        rentals = self.__srvRental.get_all_rentals()
        rentals_string = ''
        if len(rentals) > 0:
            for r_id in rentals:
                r = rentals[r_id]
                rentals_string += '\n' + str(r.get_rental_id()) + ' - ' + str(r.get_client_id()) + ' - ' + str(
                    r.get_movie_id()) + ' - ' + str(r.get_rented_date()) + ' - ' + str(r.get_due_date()) + ' - ' + str(
                    r.get_returned_date())
            messagebox.showinfo("Rentals", rentals_string)
        else:
            messagebox.showinfo("Error", 'No rentals.txt registered!')

    def __late_rentals_pressed(self):
        exception_raised = False
        stats = []
        try:
            stats = self.__srvRental.late_rentals()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
            exception_raised = True
        if exception_raised is False and stats == []:
            messagebox.showinfo("Late rentals.txt", 'No late rentals.txt!')
        else:
            stats_str = ''
            for r in stats:
                stats_str += '\nrental: ' + str(r.get_rental_id()) + ' delay: ' + str(r.get_return_delay()) + ' days'
            messagebox.showinfo("Late rentals.txt", stats_str)

    def __undo_pressed(self):
        try:
            self.__srvUndoRedo.undo()
        except UndoRedoError as ure:
            messagebox.showinfo("Error", str(ure))

    def __redo_pressed(self):
        try:
            self.__srvUndoRedo.redo()
        except UndoRedoError as ure:
            messagebox.showinfo("Error", str(ure))

    def __exit_pressed(self):
        self.__main_window.destroy()