## mako-renderer
This is a simple template rendering engine that integrated mako templates into a django (1.8+) project

### Dependencies

1. [Django 1.8+](https://www.djangoproject.com/download/)
2. [Mako](http://www.makotemplates.org/)

### settings.py

```
MAKO_TEMPLATE_DIRS = [] #Path to mako templates directories
```

Also, append the following to your `TEMPLATES`' backends. Example:

```
TEMPLATES += [
    {  
        'BACKEND': 'mako_renderer.mako_template_backend.MakoEngine',
        'APP_DIRS': False,
        'DIRS': [os.path.join(ROOT_TEMPLATE_DIR, 'mako')], #MAKO_TEMPLATE_PATH,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        }
    }
]
```

Rename `ROOT_TEMPLATE_DIR` with your template root

##TODO

1. Add unit tests
2. Add support for templates in APP_DIRS
