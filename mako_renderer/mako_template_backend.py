from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import SyntaxException, TemplateLookupException

from django.conf import settings
from django.utils import six

from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from django.template import TemplateDoesNotExist
from django.template.backends.base import BaseEngine


class MakoEngine(BaseEngine):
    def __init__(self, params):
        
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        
        super(MakoEngine, self).__init__(params)

        self.template_dirs = settings.MAKO_TEMPLATE_DIRS
        self.context_processors = []

        if 'context_processors' in options:
            self.context_processors = options.pop('context_processors')
        
        self.init_engine(options)

    @cached_property
    def template_context_processors(self):
        context_processors = tuple(self.context_processors)
        return tuple(import_string(path) for path in context_processors)

    def init_engine(self, options):
        encodings = {
          'input_encoding': 'utf-8',
          'output_encoding': 'utf-8',
        }
        self.lookup = TemplateLookup(directories=self.template_dirs, **encodings)

    def from_string(self, template_code):
        try:
            return ContextProcessorTemplate(self, Template(template_code))
        except SyntaxException as exc:
            six.raise_from(TemplateSyntaxError, exc)

    def get_template(self, template_name):
        try:
            lookup_template = self.lookup.get_template(template_name)
            return ContextProcessorTemplate(self, lookup_template)
        except TemplateLookupException as exc:
            six.raise_from(TemplateDoesNotExist, exc)
        except SyntaxException as exc:
            six.raise_from(TemplateSyntaxError, exc)


class ContextProcessorTemplate(object):  
    def __init__(self, engine, template):
        self.engine = engine
        self.template = template

    def render(self, context=None, request=None):
        context = context or {}
        for processor in self.engine.template_context_processors:
            context.update(processor(request))

        return self.template.render(**context)

