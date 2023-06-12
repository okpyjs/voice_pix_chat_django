# Vocie Pix Chat with Automatic Reply by AI

VoicePixChat - Revolutionizing Conversations with AI Magic. VPChat(Voice Pix Chat) is an innovative chat application that brings a new level of excitement and convenience to your conversations. With VPchat, you'll experience the power of artificial intelligence (AI) in real-time as it automates various aspects of your chat experience. Imagine having an intelligent chatbot by your side, seamlessly replying to messages on your behalf. VPChat's AI-powered ChatGPT engine ensures that your friends and contacts receive timely responses even when you're busy or away. This auto-reply feature saves you time and keeps the conversation flowing effortlessly. But that's not all! VPChat goes beyond text-based communication. It converts text messages into captivating speech, enabling you to enjoy a hands-free chat experience. Simply listen to the voice of your messages as they come alive, making conversations more engaging and interactive. VPChat also introduces an exciting feature where it generates new images based on AI algorithms. Surprise your friends with stunning, AI-generated images tailored to your conversations. From adorable animal illustrations to mesmerizing landscapes, these AI creations add an artistic touch to your chat threads, sparking creativity and wonder. Furthermore, VPChat recognizes the importance of emojis in modern communication. That's why we've created a platform where users can contribute their own unique emojis. Express your emotions like never before with a vast collection of custom emojis, created and shared by the VPChat community. The possibilities for personal expression are endless! With VPChat, you'll enjoy a dynamic chat experience that combines the intelligence of AI with the joy of creative expression. Stay connected, enhance conversations, and unlock a world of possibilities with VPChat - where every chat is an enchanting journey. So, join us on this exciting adventure and let VPChat transform the way you chat and connect with others. Get ready to experience a new era of communication filled with auto-replies, voice messages, AI-generated images, and a vibrant emoji community. Embrace the magic of VPChat today!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy voice_pix_chat

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd voice_pix_chat
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd voice_pix_chat
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd voice_pix_chat
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
