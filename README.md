# Movie-Rental-App

This application is an assignment done for the Foundamentals of Programming course, completed in the 1st semester of my studies at Babeș Bolyai University Cluj.

## Overall description
This is an application for managing movies and clients within a movie rentals shop. CRUD operations, searching, seeing statistics (most rented movie, most active client) are provied for both categories, but some more characteristic functionality is also available, like renting, returning movies or listing the late rentals. All modifications done during a use session can be reverted and redone (undo & redo). Entities are stored in a custom data strucure (that I called IterableDictionary) and can be sorted via the Shell sort algorithm (see [source code](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/src/services/sort_filter.py)). 

The application provides unit tests with almost full coverage, file (binary & text) persistence for storing the entities and can be configured through a properties file. The user can opt for console-based UI or for a GUI developed with Tkinter. This can be set in the properties file.

The application uses layered architecture and uses concepts from the OOP paradigm.
I had to exercise feature-driven development for the realisation of this project, the work spanning on 5 assignments (5+ weeks).

## Functionalities & Requirements
1. Manage clients and movies. The user can add, remove, update, and list both clients and movies.
2. Rent or return a movie. A client can rent a movie until a given date, as long as they have no rented movies that passed their due date for return. A client can return a rented movie at any time.
3. Search for clients or movies using any one of their fields (e.g. movies can be searched for using id, title, description or genre). The search must work using case-insensitive, partial string matching, and must return all matching items.
4. Create statistics:
    - Most rented movies. This will provide the list of movies, sorted in descending order of the number of days they were rented.
    - Most active clients. This will provide the list of clients, sorted in descending order of the number of movie rental days they have (e.g. having 2 rented movies for 3 days each counts as 2 x 3 = 6 days).
    - Late rentals. All the movies that are currently rented, for which the due date for return has passed, sorted in descending order of the number of days of delay.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying).
- (Bonus possibility (0.1p)) 95% unit test code coverage for all modules except the UI (use *PyCharm Professional*, the *[coverage](https://coverage.readthedocs.io/en/coverage-5.3/)* or other modules)
- (Bonus possibility (0.2p)) Implement a graphical user interface, in addition to the required menu-driven UI. Program can be started with either UI, without changing the source code.
6. Implement persistent storage for all entities using file-based repositories. This implies implementing two additional repository sets: one using text files for storage, and one using binary files (e.g. using object serialization with [Pickle](https://docs.python.org/3.8/library/pickle.html)). The program must work the same way using in-memory repositories, text-file repositories and binary file repositories.
7. Implement a `settings.properties` file to configure your application. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file.
8. Create a Python module that contains an iterable data structure*, a sort method and a filter method, together with complete PyUnit unit tests (100% coverage). The module must be reusable in other projects. Update your previous code to use the data structure (for storing objects in the repository) and both functions (in the repository or service layer) from this module. *Study the [`__setItem__`](https://docs.python.org/3/reference/datamodel.html#object),`__getitem__`, `__delItem__`, `__next__` and `__iter__` Python methods.

## Some pics of the GUI
![main window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/main_window.png)

![add movie window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/add_movie.png)

![list movies window after add](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/list_movies.png)

![update movie window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/update_movie.png)

![list movies window after update](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/list_movies_after_update.png)

![rent movie window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/rent_movie.png)

![list rentals window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/list_rentals.png)

![return movie window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/search_movie.png)

![search movie results window](https://github.com/bernadetthoszu/Movie-Rental-App/blob/main/search_movie_results.png)
