from . import views

routes = [
    ("/login", views.login, ["POST"]),
    ("/register", views.register, ["POST"]),
    ("/confirm/<token>", views.confirm_account, ["GET"]),
    ("/forgot-password", views.request_password_reset, ["POST"]),
    ("/password-reset/<token>", views.password_reset, ["GET"]),
]
