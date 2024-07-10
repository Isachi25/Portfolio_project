Parking Spot Reservation System

Introduction
The Parking Spot Reservation System is a web-based application that allows users to reserve parking spots at various locations. The system integrates M-Pesa for secure payment processing, ensuring a seamless and reliable user experience. The application is built using Django for the backend and includes features such as reservation fee calculation, double booking prevention, and payment verification using transaction codes.

Deployed Site: Parking Spot Reservation System

Project Blog Article: Read our blog on the Parking Spot Reservation System

Author(s) LinkedIn:

Stanley Njoroge
Sharon Masiga
Installation
Clone the Repository: 

sh
Copy code
git clone https://github.com/Isachi25/Portfolio_project
cd parking-reservation-system
Create a Virtual Environment:

sh
Copy code
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install Dependencies:

sh
Copy code
pip install -r requirements.txt
Apply Migrations:

sh
Copy code
python manage.py migrate
Create a Superuser:

sh
Copy code
python manage.py createsuperuser
Run the Development Server:

sh
Copy code
python manage.py runserver
Access the Application:
Open your web browser and go to http://127.0.0.1:8000/

Configuration
Environment Variables
Create a .env file in the root directory and add the following configurations:

env
Copy code
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1, .localhost
DATABASE_URL=sqlite:///db.sqlite3  # Use PostgreSQL for production
DARJA_API_KEY=your_daraja_api_key
Payment Integration
M-Pesa: Ensure you have a Daraja API account and the API keys configured in your .env file.
Usage
Admin Panel: Access the Django admin panel at http://127.0.0.1:8000/admin/ to manage users and parking spots.
User Registration: Users can register and log in to the application.
Making Reservations:
Users select a parking spot, start time, and end time.
The system calculates the payment amount.
Users make the payment to the specified M-Pesa number and enter the transaction code.
Upon successful verification, the reservation is confirmed.
API Endpoints
Calculate Payment Amount: /calculate_payment_amount/
Verify and Reserve: /verify_and_reserve/
Contributing
Contributions are welcome! Please read the contributing guidelines first.

Related Project

License
This project is licensed under the MIT License. See the LICENSE file for details.
