"""Base class based views"""

from web_framework.ext.models import Engine
from web_framework.ext.responses import JSONResponse, Response, HTMLResponse
from web_framework.ext.schema import BaseRequest
from web_framework.ext.status import Status
from web_framework.ext.utils import render_html


# Для CBV используем паттерн "Шаблон"
class BaseView:
    """Base view. In case of inheritance directly you must implement post() and get() methods"""
    request = None
    collection_tag: str = None
    model = None
    request_model = BaseRequest
    engine = Engine()
    context_params = {}

    def __call__(self, request: dict):
        """Receive request, serialize, and call method"""
        self.request = self.request_model.parse_obj(request)

        handler = getattr(self, self.request.method, None)
        if not handler:
            return JSONResponse({'error': 'method not allowed'}, status=Status.HTTP_405_METHOD_NOT_ALLOWED)
        context = handler()

        if self.context_params:
            context.update(**self.context_params)

        return self.render_to_response(context)

    def get_queryset(self):
        """Method to get default queryset. Must be implemented in child class"""
        pass

    def post(self) -> dict:
        """Method to handle POST request. Must be implemented in child classes"""
        pass

    def get(self) -> dict:
        """Method to handle GET request. Must be implemented in child classes"""
        pass

    def render_to_response(self, context: dict) -> Response:
        """Render response"""
        pass


class Mixin:
    """Base class for mixins"""

    def render_to_response(self, context: dict):
        """Mixin add rendering method"""
        raise NotImplementedError


class TemplateViewMixin(Mixin):
    """Class returns HTMLResponse"""

    template: str = None

    def render_to_response(self, context: dict) -> HTMLResponse:
        """Renders HTML response"""
        if self.template is None:
            raise AttributeError("'template' variable can't be None")
        return render_html(self.template, context)


class JSONViewMixin(Mixin):
    """CLass returns JSONResponse"""

    def render_to_response(self, context: dict, status: Status = Status.HTTP_200_OK) -> JSONResponse:
        """Renders JSON response"""
        return JSONResponse(body=context, status=status)


class ListView(BaseView):
    """List view"""

    def get_queryset(self):
        return self.engine.objects.get_list(self.model)

    def get(self) -> dict:
        """Get context data"""
        return {
            self.collection_tag: self.get_queryset()
        }


class DetailView(BaseView):
    """Detail view"""

    def get_queryset(self):
        pk = self.request.params.get('id', None)
        return self.engine.objects.get_by_id(self.model, int(pk))

    def get(self) -> dict:
        return {self.collection_tag: self.get_queryset()}


class CreateView(BaseView):
    """Create view"""

    def post(self):
        instance = self.model(**self.request.body)
        self.engine.objects.create(instance)
        return JSONResponse(body={'id': instance.id}, status=Status.HTTP_200_OK)
