
# mix-space
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
A web app for sharing music that includes features such as creating an account with verification via email, logging in, reCAPTCHA, uploading audio files and images, liking and following.
</br>
</br>

## ⌨️How to run the app locally:
* Clone the repository.
* Download Python3.
> https://www.python.org/downloads/.
* Create virtual environment:
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
* From the main directory type in the console:
> python manage.py migrate   
> python manage.py runserver
* You can also create admin acc by:
> python manage.py createsuperuser&nbsp;&nbsp;# then follow instructions
</br>
That's it.
