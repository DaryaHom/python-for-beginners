from wtforms import Form, StringField, DecimalField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError

from models import Category
from datetime import datetime

class SubscriptionForm(Form):
    user = StringField('Имя пользователя', validators=[DataRequired("Обязательное поле")])
    title = StringField('Название сервиса', validators=[DataRequired("Обязательное поле")])
    category = SelectField('Категория', choices=Category.choices(), validators=[DataRequired("Выберите категорию")])
    start_date = StringField('Дата начала', validators=[DataRequired("Укажите дату в формате ГГГГ-ММ-ДД")])
    end_date = StringField('Дата окончания', validators=[DataRequired("Укажите дату в формате ГГГГ-ММ-ДД")])
    price = DecimalField('Цена', validators=[Optional()])
    price_daily = DecimalField('Ежедневная цена', validators=[Optional()])
    descr = TextAreaField('Описание', validators=[Optional()])
    submit = SubmitField('Добавить подписку')

    def validate_start_date(form, field):
        try:
            datetime.strptime(field.data, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

    def validate_end_date(form, field):
        try:
            datetime.strptime(field.data, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        # Проверка: хотя бы одно из price или price_daily должно быть указано
        if self.price.data is None and self.price_daily.data is None:
            self.price.errors.append("Укажите либо общую цену, либо ежедневную")
            self.price_daily.errors.append("Укажите либо общую цену, либо ежедневную")
            return False
        return True
