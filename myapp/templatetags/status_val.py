from django import template

register = template.Library()

@register.filter(name='status_val')
def status_val(prob):
	return prob.status
