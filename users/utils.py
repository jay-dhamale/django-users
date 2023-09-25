def reset_password_message(token):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
            <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
                <h1 style="margin-top: 2.5rem;">Password Reset Request</h1>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                You have requested to reset your password. </br>  Following is your OTP </br> <h2> {token} </h2>
                </p>
                <div class="social-icons" style"
                    margin-top: 2.5rem;
                    margin-left: 1.25rem;
                ">
                <a href="https://www.facebook.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/facebook_circle-512.png" alt="Facebook" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://twitter.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.instagram.com/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.linkedin.com/company/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png" alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                </div>
                <p class="copyright" style="color: gray;">Copyright &copy; 2023 Atomic Loops Pvt. Ltd. <br/> <a href="https://www.atomicloops.com/" target="_blank" style="text-decoration: none;">atomicloops.com</a></p>
            </div>

    </body>
    </body>
    </html>
    """


# Update Password Template
def update_password_message():
    return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
            <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
                <h1 style="margin-top: 2.5rem;">Password Reset Successful</h1>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                Your password has been successfully reset. You can now login using your password.
                </p>
                <div class="social-icons" style"
                    margin-top: 2.5rem;
                    margin-left: 1.25rem;
                ">
                <a href="https://www.facebook.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/facebook_circle-512.png" alt="Facebook" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://twitter.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.instagram.com/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.linkedin.com/company/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png" alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                </div>
                <p class="copyright" style="color: gray;">Copyright &copy; 2023 Atomic Loops Pvt. Ltd. <br/> <a href="https://www.atomicloops.com/" target="_blank" style="text-decoration: none;">atomicloops.com</a></p>
            </div>

    </body>
    </body>
    </html>
    """


# Admin reset password
def admin_reset_password_message(token):
    return f"""Your reset password token is {token}"""


# Admin Update Password Template
def admin_update_password_message():
    return """Password has been updated successfully"""


# Admin Register Message
def admin_register_message():
    return """Successfully registered."""


def send_otp(token):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
            <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
                <h1 style="margin-top: 2.5rem;">OTP Request</h1>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                You have requested an OTP(One-time Password) to log in. Please enter the following code when prompted:
                </p>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                <strong>
                {token}
                </strong>
                </p>
                <div class="social-icons" style"
                    margin-top: 2.5rem;
                    margin-left: 1.25rem;
                ">
                <a href="https://www.facebook.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/facebook_circle-512.png" alt="Facebook" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://twitter.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.instagram.com/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.linkedin.com/company/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png" alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                </div>
                <p class="copyright" style="color: gray;">Copyright &copy; 2023 Atomic Loops Pvt. Ltd. <br/> <a href="https://www.atomicloops.com/" target="_blank" style="text-decoration: none;">atomicloops.com</a></p>
            </div>

    </body>
    </body>
    </html>
    """


def resend_otp(token):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
            <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
                <h1 style="margin-top: 2.5rem;">OTP Request</h1>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                You have requested an OTP(One-time Password) Again. Please enter the following code when prompted:
                </p>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                <strong>
                {token}
                </strong>
                </p>
                <div class="social-icons" style"
                    margin-top: 2.5rem;
                    margin-left: 1.25rem;
                ">
                <a href="https://www.facebook.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/facebook_circle-512.png" alt="Facebook" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://twitter.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.instagram.com/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.linkedin.com/company/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png" alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                </div>
                <p class="copyright" style="color: gray;">Copyright &copy; 2023 Atomic Loops Pvt. Ltd. <br/> <a href="https://www.atomicloops.com/" target="_blank" style="text-decoration: none;">atomicloops.com</a></p>
            </div>

    </body>
    </body>
    </html>
    """


def register_message():
    return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="
            font-family: Arial, sans-serif;
            text-align: center;
        ">
            <div class="container" style="
                max-width: 600px;
                margin: 0 auto;
            ">
                <h1 style="margin-top: 2.5rem;">Registration Successful</h1>
                <p style="
                    margin-top: 1.25rem;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                Thank you for registering with our service. Your account has been successfully created!
                </p>
                <div class="social-icons" style"
                    margin-top: 2.5rem;
                    margin-left: 1.25rem;
                ">
                <a href="https://www.facebook.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/facebook_circle-512.png" alt="Facebook" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://twitter.com/atomicloops" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.instagram.com/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/instagram_circle-512.png" alt="Instagram" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                <a href="https://www.linkedin.com/company/atomicloops/" target="_blank" style="
                    display: inline-block;
                    margin-right: 1.25rem;
                    transition: 0.2s;
                ">
                <img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/linkedin_circle-512.png" alt="LinkedIn" style="
                    height: 2rem;
                    width: 2rem;
                ">
                </a>
                </div>
                <p class="copyright" style="color: gray;">Copyright &copy; 2023 Atomic Loops Pvt. Ltd. <br/> <a href="https://www.atomicloops.com/" target="_blank" style="text-decoration: none;">atomicloops.com</a></p>
            </div>

    </body>
    </body>
    </html>
    """
