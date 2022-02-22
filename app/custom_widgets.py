from wtforms.widgets import html_params


def select_multi_checkbox(field, ul_class='dropdown-menu', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = ['<ul %s aria-labelledby="dropdownMenu1">' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = '%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append('<li><input %s /> ' % html_params(**options))
        html.append('<label for="%s">%s</label></li>' % (field_id, label))
    html.append('</ul>')
    return ''.join(html)
