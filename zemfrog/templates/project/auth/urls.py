from . import views

docs = {"tags": ["auth"]}
routes = [
    ("/user", views.user_detail, ["GET"]),
    ("/login", views.login, ["POST"]),
    ("/register", views.register, ["POST"]),
    ("/confirm/<token>", views.confirm_account, ["GET"]),
    ("/forgot-password", views.request_password_reset, ["POST"]),
    ("/password-reset/verify/<token>", views.confirm_password_reset_token, ["GET"]),
    ("/password-reset/<token>", views.password_reset, ["POST"]),
]
