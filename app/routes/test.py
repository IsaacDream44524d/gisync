from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/test')
def vite_test():
    return render_template('admin/test.html')