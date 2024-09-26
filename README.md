# Djangocon US 2024 Hackathon

Repository for the Djangocon US 2024 Hackathon by the Unveil Team

## Team Members

- [@Michael Riley](https://github.com/ErriteEpticRikez)
- [@Tim Babiy](https://github.com/yellow-grape)
- [@Jack Linke](https://github.com/jacklinke)

## Project Goals

- Create a platform for artists to share their art with the world, where the focus is on the art and not the artist.

## Infrastructure

- Flutter for the front end
- Django for the backend
- Postgres for the database
- Platform.sh for hosting
- GitHub for version control
- Slack for communication

## Implementation

- Comments are anonymized. Only the artist can see who commented.
- Images are shown 5 at a time, and the next 5 are preloaded in the background.
- The only algorithms for viewing art are *chronological* and *random*. The goal is to give all artists an equal chance to be seen.
- Option to upload art in either portrait or landscape orientation.
- Ability to create collections of art.
- Moderation tools and reporting for the artist, and for reporting artwork that violates the terms of service.

## Development

### Frontend

### Backend

## Hackathon Rules

- Did project use Django - **2 points**
- Clarity of presentation - **3 points**
- Problem statement is given and project addresses that problem - **3 points**
- Originality (this can include building off an example idea in a creative way) - **2 points**
- Ability to respond to questions - **3 points**
- Effective use of time (Use time given, but don’t go over) - **1 point**
- If working on a team: Demonstrate collaboration - **2 points**
- If working solo: Demonstrate how you overcame blocker - **2 points**


## Local Development

You can run a copy of the Postgres database in docker compose.

Copy the `.env.local` file to `.env` and update the values as needed.

```bash
docker-compose up -d
```

Then you can run the Django server.

```bash
python manage.py runserver
```
