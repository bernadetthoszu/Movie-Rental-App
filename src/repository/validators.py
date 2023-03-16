import datetime
from src.exceptions import ValidationError

class ValidMovie :

    def validate(self, movie):
        """"
        Checks if ID is a digit and genre is from the list ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation']
        Raises ValidationError if not so
        """
        errors = ''
        if not movie.get_movie_id().isdigit() :
            errors += 'Invalid id! '
        if movie.get_genre() not in ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation'] :
            errors += 'Invalid genre! '
        if len(errors) > 0 :
            raise ValidationError(errors)

    def validate_movie_id(self, movie_id):
        """"
        Checks if ID is a digit
        Raises ValidationError if not so
        """
        if not movie_id.isdigit() :
            raise ValidationError('Invalid movie id!')

    def validate_update(self, attribute, new_value):
        """"
        Checks if attribute is from ['description', 'genre'] and if it is genre checks if new_value is from ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation']
        Raises ValidationError if not so
        """
        if attribute not in ['description', 'genre'] :
            raise ValidationError('Invalid attribute!')
        elif attribute == 'genre' and new_value not in ['Action', 'Horror', 'Romance', 'Drama', 'Thriller', 'Comedy', 'Science fiction', 'Western', 'Documentary', 'Musical', 'Animation'] :
            raise ValidationError('Invalid genre!')

class ValidClient :

    def validate_client_id(self, client_id):
        """"
        Checks if ID is a digit
        Raises ValidationError if not so
        """
        if not client_id.isdigit() :
            raise ValidationError('Invalid client id!')

class ValidRental(ValidMovie, ValidClient) :

     def validate_rental_id(self, rental_id):
         if not rental_id.isdigit():
             raise ValidationError('Invalid rental id!')

     def validate(self, rental_id, client_id, movie_id, rented_date, due_date):

         #TODO - You can add a rental which has rented_date before the rented_date of an already existing rental of the client...Not ok
         #TODO - Normally a rental should have the rented_date the day of the rental (datetime.date.today()) - file implementation
         errors = ''

         if not rental_id.isdigit() :
             errors += 'Invalid rental id! '

         try:
             self.validate_client_id(client_id)
         except ValidationError as ve:
            errors += str(ve) + ' '

         try:
            self.validate_movie_id(movie_id)
         except ValidationError as ve:
            errors += str(ve) + ' '

         year, month, day = str(due_date).split("-")
         due_date_iso_string = year + '-' + month + '-' + day
         try:
             due_date = datetime.date.fromisoformat(due_date_iso_string)
         except ValueError:
             errors += 'Invalid due date! '

         #today = datetime.date.today()

         # date1 < date2   -->    date1 is considered less than date2 when date1 precedes date2 in time.
         # In other words, date1 < date2 if and only if date1.toordinal() < date2.toordinal().

         #if due_date < today :
             #errors += 'Invalid date!'

         year, month, day = str(rented_date).split("-")
         rented_date_iso_string = year + '-' + month + '-' + day
         try:
             rented_date = datetime.date.fromisoformat(rented_date_iso_string)
         except ValueError:
             errors += 'Invalid rented date! '

         #Python String find() method returns the lowest index of the substring if it is found in a given string. If it is not found then it returns -1.
         if errors.find('Invalid due date!') >= 0 or errors.find('Invalid rented date!') >= 0:
             raise ValidationError(errors)

         if due_date < rented_date:
             errors += 'Invalid dates! - Due date is before rented date'

         # if not year.isdigit():
         #     errors += 'Invalid year! '
         # if not month in ['01', '1', '02', '2', '03', '3', '04', '4', '05', '5', '06', '6', '07', '7', '08', '8', '09', '9', '10', '11', '12', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
         #     errors += 'Invalid month! '
         # if not day.isdigit():
         #     errors += 'Invalid day! '
         # elif int(day) == 0 or int(day) > 31:
         #     errors += 'Invalid day! '
         # elif month in ['02', '2', 'February', 'february'] and int(day) == 0 or int(day)>29:
         #     errors += 'Invalid day! '
         # elif month in ['02', '2', 'February', 'february'] and not ((int(year)%100 != 0 and int(year)%4 == 0) or (int(year)%400 == 0)) and day == '29':
         #     #To be a leap year, the year number must be divisible by four – except for end-of-century years, which must be divisible by 400. This means that the year 2000 was a leap year, although 1900 was not.
         #     #Only in leap years does February 29th exist...
         #     errors += 'Invalid day! '
         # elif month in ['02', '2', 'February', 'february', '04', '4', 'April', 'april', '06', '6', 'June', 'june', '09', '9', 'September', 'september', '11', 'November', 'november'] and day == '31':
         #     errors += 'Invalid day! '

         if len(errors) > 0 :
             raise ValidationError(errors)
