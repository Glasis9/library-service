# Library Service

## Requirements:
1. Implement CRUD functionality for Books Service
* Initialize books app
* Add book model
* Implement serializer & views for all endpoints

2. Add permissions to Books Service
* Only admin users can create/update/delete books
* All users (even those not authenticated) should be able to list books
* Use JWT token authentication from users' service

3. Implement CRUD for Users Service
* Initialize users app
* Add user model with email
* Add JWT support
* For a better experience during working with the `ModHeader` 
Chrome extension - change the default `Authorization` header for 
JWT authentication to for example `Authorize` header.
Take a look at the docs on how to deal with it.
* Implement serializer & views for all endpoints

4. Implement Borrowing List & Detail endpoint
* Initialize borrowings app
* Add borrowing model with constraints for borrow_date, 
expected_return_date, and actual_return_date.
* Implement a read serializer with detailed book info
* Implement list & detail endpoints

5. Implement Create Borrowing endpoint
* Implement create a serializer
* Validate book inventory is not 0
* Decrease inventory by 1 for book
* Attach the current user to the borrowing
* Implement and create an endpoint

6. Add filtering for the Borrowings List endpoint
* Make sure all non-admins can see only their borrowings
* Make sure borrowings are available only for authenticated users
* Add the `is_active` parameter for filtering by 
active borrowings (still not returned)
* Add the `user_id` parameter for admin users, so admin can see 
all users’ borrowings, if not specified, but if specified - only for concrete user

7. Implement return Borrowing functionality
* Make sure you cannot return borrowing twice
* Add 1 to book inventory on returning
* Add an endpoint for it

8. Implement the possibility of sending notifications on each Borrowing creation
* Set up a telegram chat for notifications posting in there
* Set up a telegram bot for sending notifications
* Investigate the `sendMessage` function interface in Telegram API
* Make sure all private data is private, and never enters the 
GitHub repo (you can use the `python-dotenv` package for simple 
working with `.env` files. Make sure to add the `.env.sample` file with
the `.env` content skeleton)
* Create a helper for sending messages to the notifications chat through Telegram API
* Integrate sending notifications on new borrowing creation 
(provide info about this borrowing in the message)

9. Implement a daily-based function for checking borrowings overdue
* The function should filter all borrowings, which are overdue 
(expected_return_date is tomorrow or less, and the book is still not returned) 
and send a notification to the telegram chat about each overdue separately with 
detailed information
* It will be a scheduled task, and Django by default cannot do such tasks. 
To perform this task, you’ll have to use `Django-Celery`.
* If no borrowings are overdue for that day - 
send a “No borrowings overdue today!” notification.


### Technologies to use:
1. Use Celery as task scheduler for check of overdue borrowings and 
sending push notification in Telegram Bot.
2. Python, Django ORM, PostgreSQL.
3. All endpoints should be documented via Swagger.

### How to run:
- Copy .env_sample -> .env and populate with all required data
- `docker-compose up --build`
- Create admin user & Create schedule for check of overdue borrowings and 
sending push notification in Telegram Bot

###
![Book-Admin](https://github.com/Glasis9/library-service/blob/main/Book-Admin.jpg)
![Book-User](https://github.com/Glasis9/library-service/blob/main/Borrowing-user.jpg)
![Borrowing-Admin](https://github.com/Glasis9/library-service/blob/main/Borrowing-Admin.jpg)
![Borrowing-User](https://github.com/Glasis9/library-service/blob/main/Borrowing-user.jpg)
![Create task](https://github.com/Glasis9/library-service/blob/main/Create%20task.jpg)
![Notification in Telegram Bot](https://github.com/Glasis9/library-service/blob/main/Telegram.jpg)
