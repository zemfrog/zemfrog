def index():
    return "{{ '' if main_app else name + ' ' }}index page"
