from rest_framework.renderers import BrowsableAPIRenderer


class ReadBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render_form_for_serializer(self, serializer):
        return ""
