from wtforms import Form, StringField, DecimalField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, ValidationError

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
    submit = SubmitField('Сохранить')

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
        
        # Проверка согласованности цен
        if self.price.data and self.price_daily.data:
            try:
                start_date = datetime.strptime(self.start_date.data, "%Y-%m-%d")
                end_date = datetime.strptime(self.end_date.data, "%Y-%m-%d")
                days_diff = (end_date - start_date).days
                
                if days_diff < 0:
                    self.start_date.errors.append("Дата начала подписки не может быть позже даты окончания")
                    return False
                
                expected_price = self.price_daily.data * days_diff
                
                # Сравниваем с введенной ценой
                if abs(self.price.data - expected_price) > 0.01:  # допуск 0.01 рубля
                    error_msg = f"Ежедневная цена не совпадает с итоговой. Проверьте правильность ввода"
                    self.price.errors.append(error_msg)
                    self.price_daily.errors.append(error_msg)
                    return False
            except (ValueError, AttributeError, TypeError):
                # Если есть ошибки в датах, пропускаем эту проверку
                pass
        return True
