# User Activity Track API

## Installation

To be able to use this project, First, you need to create an empty python project folder. After that, you need to copy and paste files in this repository. Then, you need to run `pip install -r requirements.txt` command in the terminal, which will install necessary packages for this project. With this, the basics of this project are ready, now we only need to complete step that necessary for connecting to database.

First of all, you need to create a MariaDB database ([see MariaDB](https://mariadb.com/)). This database needs tables (user, device, plant, etc.) and triggers (save_server_status, etc.), to create these, you need to run the `User.sql` file, which is in repository, using some database administration tool such as [`HeidiSQL`](https://www.heidisql.com/).

Secondly, you need to fill in necessary parts in `authorization.ini` file in the project folder.

After all these steps, you can test if your project works or not using, `TestRequest.py` file. Result should be something like this:

```
[{
"user_ID":  1,
"username":  "exampleUser",
"email":  null,
"password":  "examplePassword",
"session":  "exampleSession",
"Card_ID":  null,
"Company_ID":  null
}]
```
