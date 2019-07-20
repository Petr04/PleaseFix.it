from django import template

register = template.Library()

@register.filter(name='status')
def status(prob):
	return prob.get_status_display()
