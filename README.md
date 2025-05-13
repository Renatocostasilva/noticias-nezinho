# Notícias - Modern News Website

A modern and responsive news website built with Django and Bootstrap CSS.

## Features

### Public Layout (Reader Area)
- Homepage with header, navigation menu, search field, featured news slider, and recent news listings
- Individual news page with social sharing and comments
- Category pages with filtered news and pagination
- Responsive design for all devices

### Admin Area (CMS)
- Secure login system
- Dashboard with overview statistics
- News management (CRUD operations)
- Category management
- Featured news configuration
- Image upload with automatic resizing

## Technologies Used
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Backend**: Django
- **Database**: SQLite (development) / PostgreSQL (production)
- **Additional**: CKEditor for WYSIWYG editing, Native comments system

## Installation

### Quick Start
The easiest way to get started is to use the provided run script:

```
python run.py
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Install all dependencies
3. Run migrations
4. Offer to create a superuser
5. Start the development server

Alternatively, you can use our all-in-one setup script:

```
python setup_project.py
```

This script will:
1. Reset the database (remove existing database and migration files)
2. Create new migrations
3. Apply migrations
4. Offer to create a superuser
5. Offer to initialize the database with sample data
6. Offer to start the development server

### Manual Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/noticias.git
cd noticias
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the website at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/

## Troubleshooting

### ModuleNotFoundError: No module named 'django.utils.six'

If you encounter this error, it's because the `django-disqus` package is trying to import `django.utils.six`, which was removed in recent Django versions. We've addressed this issue in two ways:

1. **Solution 1 (Implemented)**: We've removed the dependency on `django-disqus` and implemented a native comments system instead.

2. **Solution 2 (Alternative)**: If you still want to use Disqus, you can run the `disqus_fix.py` script to patch the package:
   ```
   python disqus_fix.py
   ```
   This script replaces the problematic import with a compatible one.

### OperationalError: no such table: news_news

If you encounter this error, it means that the database tables were not created correctly. We've provided a script to fix this issue:

```
python fix_database.py
```

This script will:
1. Remove the existing database
2. Remove all migration files
3. Create new migrations
4. Apply the migrations
5. Offer to create a superuser
6. Offer to start the server

### Initializing the Database with Sample Data

After setting up the database, you can populate it with sample data using:

```
python init_data.py
```

This script will:
1. Create sample categories (Politics, Economy, Technology, Sports, Entertainment, Health)
2. Create sample news articles with content and images
3. Add tags to the articles
4. Use the first superuser as the author for all articles

Note: You must create a superuser before running this script.

## Project Structure
- `noticias/` - Main project directory
- `news/` - News app
- `accounts/` - User authentication app
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
- `templates/` - HTML templates

## License
This project is licensed under the MIT License - see the LICENSE file for details. 