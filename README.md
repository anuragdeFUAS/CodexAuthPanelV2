# Web-Authentication

## Contents

*   [API Documentation](#API-Documentation)
*   [Getting started](#getting-started)
    *   [Requirements](#requirements)
    *   [Install](#install)
    *   [Usage](#usage)


## API-Documentation
At first this is version 0.1 which is live. There will be more changes in api of later versions

<img width="896" alt="register with mostly required fileds" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/5d647edd-ae04-49b4-acc3-f9d4fac362be">

In the above way one can register with user data. There are extra fields like firstname and lastname which are not madatory. Below is a json format that should be parsed;
```
{
    "username": "TeleTest",
    "firstname": "",
    "lastname": "",
    "email": "mashnunul.huq@stud.fra-uas.de",
    "password": "human123"
}
```

<img width="849" alt="login with username and password" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/b719b1a5-7906-4dce-b594-b65a0ee408c6">

Now the above one is the login api format. This method is logging in with the username and password field.
```
{
    "username": "Mashnunul",
    "email": "mashnunul.huq@stud.fra-uas.de",
    "password": "human123"
}
```

<img width="857" alt="login with token" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/67c3c305-d14f-4914-97a4-bec4893cf81d">

This is a second method to login with registration token. This will later be changed to project login system. So it is not suggested to implement right now.

<img width="858" alt="logout with token" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/638dd8c0-9dac-4033-b301-7938e2efea63">

This is the logout API. The login token will be revoked by this.

<img width="858" alt="update profile token field" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/dd64d56e-5cad-44d6-be9b-1aee6c252e77">

For Updating user profile one needs to put login authentication token.

<img width="849" alt="update profile" src="https://github.com/javedcoding/CODEXAuthenticationPannel/assets/59325753/abec53df-1d3e-4e05-b454-0366f803ef18">

This is the API format for user profile updating.
```
{
    "first_name": "TeleTest",
    "last_name": "Test",
    "phone": "123123",
    "city": "mashnunul.huq@stud.fra-uas.de",
    "state": "uganda",
    "zip": "60422"
}
```
