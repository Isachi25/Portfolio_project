# Parking Spot Reservation System

## Introduction
The Parking Spot Reservation System is a web-based application designed to help users conveniently reserve parking spots at various locations. The system integrates with M-Pesa for secure payment processing, ensuring a seamless and reliable user experience.

### Links
- **Deployed Site**: [Parking Spot Reservation System]()
- **Project Blog Article**: [Read our blog on the Parking Spot Reservation System](https://www.linkedin.com/pulse/designing-launching-my-smart-parking-solution-stanley-njoroge-bhrnf/)
- **Author(s) LinkedIn**: 
  - [Stanley Njoroge](https://www.linkedin.com/in/stanley-njoroge/)
  - [Sharon Masiga](https://www.linkedin.com/in/sharonmasiga)

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/Isachi25/Portfolio_project
    cd parking-reservation-system
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply Migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the Development Server**:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Navigate to the Deployed Site**:
    Visit  to access the application.

2. **Reserve a Parking Spot**:
    - Select a location and parking spot type.
    - Choose a start and end time for your reservation.
    - Calculate the payment amount and make the payment via M-Pesa.
    - Enter the 3-letter M-Pesa transaction code to verify the payment.
    - Confirm the reservation.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**:
    Click the 'Fork' button at the top right of this repository page.

2. **Clone Your Fork**:
    ```sh
    git clone https://github.com/Isachi25/Portfolio_project
    cd parking-reservation-system
    ```

3. **Create a New Branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**:
    Implement your changes and commit them with clear and descriptive messages.

5. **Push to Your Branch**:
    ```sh
    git push origin feature/your-feature-name
    ```

6. **Create a Pull Request**:
    Open a pull request on the original repository with a clear description of your changes.

## Related Projects


## Licensing

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
