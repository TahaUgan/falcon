# User Activity Track API

## Installation

### Step 1: Setting Up the Project Directory

1. Create an empty Python project folder.
2. Copy and paste all the files from this repository into your project folder.

### Step 2: Installing Dependencies

3. Open a terminal and navigate to your project directory.
4. Run the following command to install the necessary packages for this project:
   ```sh
   pip install -r requirements.txt
   ```
   This command reads the `requirements.txt` file and installs all listed packages, ensuring that your environment is set up with all dependencies.

### Step 3: Setting Up the Database

5. Create a MariaDB database. You can find more information on setting up MariaDB [here](https://mariadb.com/).
6. This database will need specific tables (`user`, `device`, `plant`, etc.) and triggers (`save_server_status`, etc.). To set these up:
   - Use a database administration tool such as [`HeidiSQL`](https://www.heidisql.com/).
   - Run the `User.sql` file from the repository. This file contains the necessary SQL commands to create the required tables and triggers.

### Step 4: Configuring the Project

7. Locate the `authorization.ini` file in your project folder.
8. Fill in the necessary parts of this file with your database credentials and other configuration details. This will allow your project to connect to the MariaDB database correctly.

### Step 5: Testing the Project

9. To verify that your project is set up correctly and working, use the `TestRequest.py` file. This file contains test requests that you can run to check if the project is functioning as expected.
10. Run the `TestRequest.py` file and you should see an output similar to the following:

```json
[{
    "user_ID": 1,
    "username": "exampleUser",
    "email": null,
    "password": "examplePassword",
    "session": "exampleSession",
    "Card_ID": null,
    "Company_ID": null
}]
```

This output indicates that the API is returning user data correctly, confirming that your setup is complete and functional.

By following these steps, you ensure that your User Activity Track API is installed, configured, and ready for use.
