<h1>Welcome to Future Basics Company, {{ $name }}! </h1>

<p>
    You have been registered at Future Basics Company website,
</p>
<p>
 Use the link below to change your password and verify your account before you can log in.
</p>
<p>
    You can use this email: {{ $email }}
</p>
<p>
    and your current password is set to: {{ $password }}
</p>

<p>Use the link to change you password and verify your account:</p>
<a href="{{ route('change.password.get', $token) }}">change Password</a>

<p>
    Its good to have you with Us.
<p>
    Regards,
</p>
<p>
    FBC Human Resource Department
</p>
