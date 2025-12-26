from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to a form field"""
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='is_checkbox')
def is_checkbox(field):
    """Check if field is a checkbox"""
    return field.field.widget.__class__.__name__ == 'CheckboxInput'

@register.filter(name='is_select')
def is_select(field):
    """Check if field is a select"""
    return field.field.widget.__class__.__name__ == 'Select'

@register.filter(name='is_textarea')
def is_textarea(field):
    """Check if field is a textarea"""
    return field.field.widget.__class__.__name__ == 'Textarea'