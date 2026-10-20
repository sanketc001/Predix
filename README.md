<div align="center">
  <img src="static/images/home_cinema.svg" alt="PredixDB" height="120">

  <h3>PredixDB</h3>

  <p>
    A media-tracking web app for movies, TV series, anime and manga: keep track of what you have watched, what is on your watchlist and your favourites, and get genre-based recommendations.
    <br /><br />
    <a href="https://drive.google.com/file/d/11x-cAH6nTH0nfboQtacniusQFsTP4W9S/view?usp=sharing"><strong>Project report »</strong></a>
    ·
    Live demo (predixdb.herokuapp.com) is no longer hosted
  </p>
</div>

## Overview

PredixDB is a Django web application built as a team project. Users sign up, browse dashboards per media type, search the catalogue, add titles to personal lists, and receive recommendations based on the genres of the titles they have already added.

**Team and credits**

- **Saksham Agarwal** ([@skshamagarwal](https://github.com/skshamagarwal)): original author of the project; Django application, views, templates and front end. Upstream repository: [skshamagarwal/Predix](https://github.com/skshamagarwal/Predix).
- **Sanket Kumar Choudhary** ([@sanketc001](https://github.com/sanketc001)): database creation and recommendation logic:
  - Data-collection scripts that built the media catalogue: `movietv.py` (IMDb Top 250 movies), `tv.py` (TV series), `anime.py` and `manga.py` (MyAnimeList), each also looking up a trailer link per title. Output is the CSV seed data (`movie.csv`, `tmovie.csv`, `tv.csv`, `anime.csv`, `anime1.csv`, `manga.csv`).
  - The genre-based recommendation algorithm (prototyped in `reccomtrial.py`) used by `home/reccomendation.py`.

## Features

- Separate dashboards for **movies, TV series, anime and manga**, each with *Recommended*, *Trending* (by ranking) and *Latest releases* rows.
- Title detail pages with rating, genres, languages, release date, description and trailer link.
- Personal lists per user (**Watched**, **Watchlist**, **Favourite**) shown on the profile page.
- Search by title, excluding titles already in the user's lists.
- Email/password registration, login and logout using Django auth.

## How recommendations work

`home/reccomendation.py` holds a genre map for every title in the catalogue, keyed by IMDb or MyAnimeList ID. For a given media type, `recc(mids, type)`:

1. Collects the genres of all titles the user has added.
2. Counts genre frequency and picks the user's most frequent genre.
3. Returns every catalogue title of that type that contains this genre and is not already in the user's lists.

The dashboard uses these recommendations once the user has added at least two titles of that type; otherwise it falls back to a shuffled list from the catalogue.

## Architecture

```
Browser ── Django 3.2 (Predix/ project, home/ app)
             ├── views.py      dashboards, media page, profile, search, auth
             ├── models.py     Media, UserMedia (user ↔ title + list name)
             ├── reccomendation.py   genre-frequency recommender
             └── templates/ + static/   Bootstrap UI
                    │
                    ▼
             MongoDB (via djongo), database "PredixDB"
                    ▲
   Offline seed scripts (movietv.py, tv.py, anime.py, manga.py) → CSV → imported into MongoDB
```

## Tech stack

- Python, Django 3.2, Gunicorn
- MongoDB with `djongo` / `pymongo`
- HTML, CSS, JavaScript, Bootstrap, Boxicons
- Data collection: IMDbPY/Cinemagoer (`imdb`), MyAnimeList (`mal-api`), BeautifulSoup, `googlesearch-python`

## Quickstart

Prerequisites: Python 3.7–3.9 (the dependency set is from 2021) and a local MongoDB server on the default port.

```bash
git clone https://github.com/sanketc001/Predix.git
cd Predix
python -m venv venv
# Windows: venv\Scripts\activate    macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

### Loading the catalogue

The repository does not include a loader script. The seed CSVs follow the `Media` model columns (`mid, title, rating, ranking, type, genre, rdate, language, cover, description, trailer, released, year`) and were imported into the `home_media` collection of the `PredixDB` database. The scraping scripts can regenerate them; they need extra packages not in `requirements.txt` (`imdbpy`/`cinemagoer`, `mal-api`, `beautifulsoup4`, `lxml`, `googlesearch-python`).

## Configuration

Settings live in `Predix/settings.py`: database engine/name (`DATABASES`), `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and static/media paths. No environment variables are read at present.

## Limitations and next steps

- Built in 2021 for a course/team project and no longer deployed; dependencies are pinned to old versions and `djongo` is not maintained against current Django releases.
- `SECRET_KEY` and `DEBUG = True` are hardcoded in settings; they should come from environment variables before any deployment.
- The recommender only uses the single most frequent genre and its genre map is hardcoded; a natural next step is building it from the database and scoring titles by weighted genre overlap or embeddings.
- Some views (e.g. recommendations, search exclusion) read all users' list entries rather than only the current user's.
- No CSV-to-MongoDB import command and no automated tests.
