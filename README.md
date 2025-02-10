
![Zrzut ekranu 2025-02-10 021508](https://github.com/user-attachments/assets/e75c5410-10ff-4558-8e5a-d51470fa618f)

# Online Banking Application

This project is an online banking application that allows users to perform basic banking operations. Users can register, log in, and manage their accounts conveniently and securely.

## Live Demo

You can access and test the application here: [Online Banking Application](https://app.markbank-privateproject.com/)

### How to Use
1. **Register**: Create a new account by providing your personal details.
2. **Check Your Email**: After registration, check your email for your unique **User ID**.
3. **Log In**:
   - Enter the **User ID** you received in your email.
   - Provide the password you set during registration.
4. **Explore Features**:
   - View account balance.
   - Deposit or withdraw funds.
   - Make transfers to other accounts.
   - Change your password or update your personal information.

## Features

- **User Registration**: Users can register by providing personal information. Each user receives a unique identifier sent directly to their email.
- **Login and Authentication**: A secure login system protects user data.
- **Account Management**:
  - Checking account balance.
  - Viewing transaction history.
  - Making online transfers to other registered users.
- **Transaction History**: Every transaction is recorded and displayed in the user's history.
- **Error Handling**: The application provides appropriate feedback in case of invalid data or operations.

## In Progress: Upcoming Features

The application is actively being developed, and the following features are in progress:
- **Multi-currency Accounts**: Users will be able to hold balances in multiple currencies within the same account.
- **Currency Exchange**: The application will enable users to exchange their current balance into other currencies at real-time exchange rates.
- **Loan Services**: Users will be able to apply for loans directly from the application, with tailored repayment options and interest rates.

Stay tuned for updates!

## Cloud Infrastructure

This application is hosted on **AWS Cloud** and utilizes the following services:
- **EC2**: Virtual machine hosting the application with Docker and Nginx for serving content.
- **RDS**: Managed PostgreSQL database for secure and scalable data storage.
- **Route 53**: DNS management and domain routing.
- **VPC**: Isolated network for secure communication between application components.
- **Nginx**: Reverse proxy for handling HTTP/HTTPS traffic and load balancing.
- **SSL Certificate**: The application is secured with an SSL certificate to ensure encrypted communication.

## Technologies and Libraries

- **Backend**: 
  - Programming Language: Python
  - Framework: Flask
- **Frontend**:
  - HTML, CSS, JavaScript
- **Database**:
  - PostgreSQL
- **Libraries**:
  - `Flask` 
  - `psycopg2` 
  - `pytest` 
  - `email-validator` 
  - `bcrypt` 
  - `requests` 
- **Other Technologies**:
  - Docker 
  - Kubernetes 

## Application Structure

The project is divided into several modules to ensure clarity and maintainability:

- **Backend**: Handles application logic, including user management, transactions, and data validation.
- **Frontend**: Provides a clean and responsive user interface.
- **Database**: Securely stores user data, transaction history, and other essential information.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for more details.
