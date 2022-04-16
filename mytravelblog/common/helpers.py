from datetime import datetime

BIRTH_YEAR_RANGE = [y for y in range(1920, datetime.now().year + 1)]


class BootstrapFormMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'form-control'


# class AuthUserLimitedViewMixin:
#
#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user).all()
