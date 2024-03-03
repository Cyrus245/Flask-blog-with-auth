# Flask Blog

This is a simple Flask-based blog application where users can create, edit, and delete blog posts. It uses SQLite as the database backend and SQLAlchemy as the ORM. The blog posts consist of a title, subtitle, author, body, and an optional image URL.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/your_username/your_project.git
    ```

2. Navigate into the project directory:

    ```
    cd your_project
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have Python installed on your system.

2. Start the Flask application:

    ```
    python app.py
    ```

3. Access the blog application by navigating to `http://localhost:5000` in your web browser.

## Features

### 1. View All Posts

- URL: `/`
- Method: `GET`
- Description: Displays all the blog posts.

### 2. View a Single Post

- URL: `/post/<int:index>`
- Method: `GET`
- Description: Displays a single blog post identified by its index.

### 3. Create a New Post

- URL: `/create_post`
- Method: `GET` and `POST`
- Description: Allows users to create a new blog post.

### 4. Edit a Post

- URL: `/edit/<int:post_id>`
- Method: `GET` and `POST`
- Description: Allows users to edit an existing blog post.

### 5. Delete a Post

- URL: `/delete/<int:post_id>`
- Method: `GET`
- Description: Allows users to delete an existing blog post.

### 6. About Page

- URL: `/about`
- Method: `GET`
- Description: Displays information about the blog.

### 7. Contact Page

- URL: `/contact`
- Method: `GET`
- Description: Provides contact information for the blog owner.

## Database

The application uses SQLite as the database backend. The database schema includes the following fields:

- `id`: Primary key for the blog posts.
- `title`: Title of the blog post.
- `subtitle`: Subtitle or summary of the blog post.
- `date`: Date of the blog post.
- `body`: Main content of the blog post.
- `author`: Author of the blog post.
- `img_url`: URL of an optional image for the blog post.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.

