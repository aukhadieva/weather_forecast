from django import forms


class TitleMixin(object):
    """
    Миксин для получения заголовка страницы.
    """

    title = None

    def get_title(self):
        """
        Возвращает заголовок страницы.
        """
        return self.title

    def get_context_data(self, **kwargs):
        """
        Добавление заголовка в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()

        return context


class StyleMixin:
    """
    Миксин для стилизации форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
