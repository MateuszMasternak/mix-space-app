
# mix-space
</svg>
</br>
</br>

## 🎥Demo:
![](https://j.gifs.com/gpELAk.gif)
</br>
</br>

## ⚙️Stack:
<img src="https://user-images.githubusercontent.com/113989577/195915225-f7a51108-c25f-4e79-9b4e-77e90f3e6499.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916338-aac36a28-5222-4525-84ff-223923605b2c.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916998-d016e522-302c-4890-b1ac-9e4c65ae7f03.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916567-b2272f97-6e76-4ed9-9abb-98e78ec0e92a.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195917268-9fc749f5-9a72-4375-9c7d-8520dcfa4c5f.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195917361-c0afb3bb-06c3-458c-9f64-41444f3f4300.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195927768-05a81249-e2c7-409a-8435-692b338c8d31.png" width="50">
<br>
</br>

## 📄About:
My project is an audio web app with build in simple audio player. You can there share your own music by uploading it. Others (or you) can listen your music tracks, like them and also follow you, to be up to date with your productions and mixes. It's possible to upload your avatar, which will be visible on your profile page or delete your music tracks from there. The home page is a place when you can see all user's music uploads sorted by date from the newest. The music uploads are displayed as a purple cards with all info about them in those, such as genre, date, uploader, title. There is also an option to give a like, which equals adding the track to your liked tracks list. Besides, you can click at an uploader nickname to be redirected to his profile, or on the track card to be redirected to a music player, where also is the option to give the like. The app show messages after handling log ins, log outs, uploads, or if they aren't successfull, etc. Sign up need an email confirmation before log in will be possible, and you can use the email in that, because of implemented custom user model and authentication. Mix-space also contain a search bar, which can be used to search music by a phrases, which are contained in the titles. At the end, log in and sign up forms include reCAPTCHA by Google. 
</br>
</br>

## ⌨️How to run the app locally:
* Clone the repository.
* Download Python 3.\*.\*, the project is wrote in Python 3.10.8.
> https://www.python.org/downloads/.
* Create virtual environments:
> https://docs.python.org/3/tutorial/venv.html.
* Download all dependencies:
> python -m pip install -r requirements.txt.
* Download PostgreSQL, configure it, and then create a database using pgAdmin for example:
> https://www.postgresql.org/download/.
* Create .env file in the project's main root and fill up it with DB_NAME, DB_USER, DB_PASSWORD keeping the names:
> https://pypi.org/project/python-dotenv/#file-format.
* Go to your Google account > security > turn on 2-Step Verification > App passwords > Other > type name and generate > fill up .env file with EMAIL, EMAIL_PASSWORD (generated key) same as above.
* Go to google.com/recaptcha/admin > register reCAPTCHA with v2 "I'm not a robot" Checkbox and 127.0.0.1 domain > fill up .env file with RCAP_PUBLIC (SITE KEY) and RCAP_PRIVATE (SECRET KEY) using generated keys.
* Fill up SECRET_KEY which is on the top of the mixspace/settings.py or also fill up .env file with that.
* From the main root type on the console:
> python manage.py makemigrations  
> python manage.py migrate  
> python manage.py createsuperuser&nbsp;&nbsp;# then follow instructions  
> python manage.py runserver  
</br>
That's it.
