from django import template

register = template.Library()

@register.filter(name='fixer')
def fixer(prob):
	return prob.fixer
