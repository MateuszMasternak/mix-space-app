
# mix-space
<br>

## 🎥Demo:
![](https://j.gifs.com/gpELAk.gif)
</br>
</br>

## ⚙️Stack:
<img src="https://user-images.githubusercontent.com/113989577/195915225-f7a51108-c25f-4e79-9b4e-77e90f3e6499.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916338-aac36a28-5222-4525-84ff-223923605b2c.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916998-d016e522-302c-4890-b1ac-9e4c65ae7f03.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195916567-b2272f97-6e76-4ed9-9abb-98e78ec0e92a.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195917268-9fc749f5-9a72-4375-9c7d-8520dcfa4c5f.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195917361-c0afb3bb-06c3-458c-9f64-41444f3f4300.png" width="50"> <img src="https://user-images.githubusercontent.com/113989577/195927768-05a81249-e2c7-409a-8435-692b338c8d31.png" width="50">
<br>
<br>

## 📄About:
The application initially created as the final project of the course: CS50's Web Programming with Python and JavaScript.

Includes the following features:

1. User Authentication: It includes login and registration system. Users can register for an account, and their registration is confirmed via email.

2. reCAPTCHA Integration: It implements reCAPTCHA to prevent bots.

3. Media Upload Forms: Allows users to upload audio files in WAV format and images for user's avatars.

4. Likes and Follows System: Enables users to interact with each other through likes and follows on favorite artists or tracks.

5. Audio Conversion: Provides a hidden WAV to MP3 converter, allowing to reduce the size of uploaded audio files.

6. Simple Audio Player: Offers a basic audio player that allows users to listen to uploaded tracks directly on the platform.
<br>
<br>

## ⌨️How to run the app:
1. Create .env file in the root directory:
> DB_NAME='postgres'  
> DB_USER='postgres'  
> DB_PASSWORD='abc123'
> 
> EMAIL='' # Optional email for sending account verification emails. You can manually set "Is active" in the database or admin panel. 
> EMAIL_PASSWORD='' # To set up email functionality: Google account > Security > Turn on 2-Step Verification > App passwords > Other                                                                
>
> RCAP_PUBLIC='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' # reCAPTCHA public key for testing purposes.
> RCAP_PRIVATE='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe' # reCAPTCHA private key for testing purposes. <br>
> \# You can change them for your own (v2) keys: https://developers.google.com/recaptcha/docs/settings
> 
> SECRET_KEY='' # Place your secret key here.
 
2. Build and run docker images: 
> docker compose up -d --build

3. Go to 'localhost:8000' in your web browser.
</br>

That's it.
