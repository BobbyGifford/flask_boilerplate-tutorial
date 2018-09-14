from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField,
                     RadioField, SelectField, TextAreaField)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'


class InfoForm(FlaskForm):
    breed = StringField("What breed are you? ")
    submit = SubmitField('Submit')


class InfoForm2(FlaskForm):
    item_name = StringField("Enter item_name here", validators=[DataRequired()])
    juicy = BooleanField("Is this juicy?")
    category = RadioField('Please choose category',
                          choices=[('choice_one', 'Good'), ('choice_two', 'Bad'), ('choice_three', 'Ugly')])
    food_choice = SelectField('Pick your favorite food:', choices=[('veg', 'Veggie'), ('meat', 'Real Food')])
    feedback = TextAreaField()
    submit = SubmitField("Submit me")


@app.route('/')
def index():
    return render_template("goose.html")


@app.route('/test')
def test():
    test_var = 'Bobby'
    test_dict = {"goose": "juice"}
    test_list = [12, 3, 45, 657, 2]
    return render_template('basic.html', passed_var=test_var, test_dict=test_dict, test_list=test_list)


@app.route('/test/<name>')
def test_variable(name):
    return 'This is a variable in url: {}'.format(name)


@app.route('/signup')
def signup():
    return render_template('signup.html', form_var="works")


@app.route('/thank_you')
def thank_you():
    first = request.args.get('first')
    last = request.args.get('last')

    return render_template('thank_you.html', first=first, last=last)


@app.route('/form_section', methods=['GET', 'POST'])
def form_section():
    breed = False
    form = InfoForm()

    if form.validate_on_submit():
        breed = form.breed.data
        form.breed.data = ''
    return render_template('form_section.html', form=form, breed=breed)


@app.route('/form_section2', methods=['GET', 'POST'])
def form_section2():
    form = InfoForm2()
    if form.validate_on_submit():
        flash("Message submitted")

        session['item_name'] = form.item_name.data
        session['juicy'] = form.juicy.data
        session['category'] = form.category.data
        session['food_choice'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        return redirect(url_for('form_section2_confirm'))
    return render_template('form_section2.html', form=form)


@app.route('/form_section2_confirm')
def form_section2_confirm():
    return render_template('form_section2_confirm.html')


if __name__ == '__main__':
    app.run(debug=True)
