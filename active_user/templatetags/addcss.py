from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class": css})

@register.filter(name='addcolor')
def addcolor(field, color):
   return field.as_widget(attrs={"style": "color:"+color+";"})
