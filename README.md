# EcoSwap

EcoSwap is a web application that allows users to exchange items with other items or add money for the exchange. The application supports various categories such as vehicles, electronics, furniture, and more.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Item listing with various categories and conditions
- Exchange proposals between users
- Messaging system for exchange negotiations
- Transaction management for adding money to exchanges

## Technologies

- Django
- SQLITE3
- HTML/CSS/JavaScript

## Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Git

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Md-Mahmudur-Reza/EcoSwap
   cd EcoSwap
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv ecoswap_env
   source ecoswap_env/bin/activate  # On Windows use `ecoswap_env\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply the migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**

   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **Admin Interface:** Access the Django admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials.
- **Item Listing:** Users can list their items for exchange, specifying category, condition, and value.
- **Propose Exchange:** Users can propose exchanges with other listed items and negotiate terms.
- **Messaging:** Users can communicate through the messaging system to finalize exchange details.
- **Transactions:** Manage transactions where money is added to exchanges.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you encounter any issues or have questions, please open an issue on GitHub or contact the project maintainers.

Happy coding!
