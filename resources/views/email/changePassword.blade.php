<h1>Future Basics registration link?</h1>

<p>
    {{-- Your current password is: {{ $phone_number }} --}}
</p>

<p>Use the link to change you password and verify your account:</p>
<a href="{{ route('change.password.get', $token) }}">change Password</a>
