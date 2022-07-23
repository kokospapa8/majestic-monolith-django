# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import mixins, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.admin_forms import AdminCacheQueryForm
from core.meta import get_default


class RetrievePatchOnlyAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView
):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateDestroyAPIView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveCreateDestroyAPIView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveCreateAPIView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BulkDataPostAPIView(GenericAPIView):
    serializer_class = None
    data_key = None

    def get_request_data(self):
        request_data = self.request.data
        return request_data if isinstance(request_data, list) else [request_data]

    def get_extra_context(self):
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.get_extra_context())
        return context

    def process_serializer(self, serializers):
        items = []
        for serializer in serializers:
            serializer.save()
            items.append(serializer.validated_data)
        return items

    def post(self, request, *args, **kwargs):
        errors = []
        serializers = []

        post_data = self.get_request_data()
        for data in post_data:
            serializer = self.get_serializer(
                data=data, context=self.get_serializer_context()
            )
            if serializer.is_valid(raise_exception=False):
                serializers.append(serializer)
            else:
                data_value = data.get(self.data_key, None)
                if data_value:
                    error_dict = {data_value: serializer.errors}
                else:
                    error_dict = serializer.errors
                errors.append(error_dict)
        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return_data = self.process_serializer(serializers)
        return Response(return_data, status=status.HTTP_200_OK)


class HealthCheckView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    _ignore_model_permissions = True

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class DMMWebView(TemplateView):
    IS_MOBILE_ONLY = False
    MOBILE_REVERSE_FOR_PC = None
    IS_MOBILE_OG_FOR_WEB = False

    def get_context_data(self, **kwargs):
        context = kwargs
        if "view" not in context:
            context["view"] = self
        meta = self.get_override_meta()
        context["meta"] = get_default(self.request, meta)
        return context

    def get_override_meta(self):
        return {}

    def redirect_to_motile_page(self):
        kwargs = {k: v for k, v in self.kwargs.iteritems() if v is not None}

        try:
            reversed_url = reverse(
                self.MOBILE_REVERSE_FOR_PC, args=self.args, kwargs=kwargs
            )
        except NoReverseMatch:
            reversed_url = self.MOBILE_REVERSE_FOR_PC.format(**kwargs)

        return HttpResponseRedirect(reversed_url)

    def get(self, request, *args, **kwargs):
        if self.IS_MOBILE_ONLY:
            if self.MOBILE_REVERSE_FOR_PC is None:
                raise NotImplementedError("please set MOBILE_REVERSE_FOR_PC")
            if not request.user_agent.is_mobile:
                self.redirect_to_motile_page()

        return super().get(request, *args, **kwargs)


@method_decorator(staff_member_required, name="dispatch")
class AdminOnlyTemplateView(TemplateView):
    pass


def control_admin_cache(request):
    if request.method == "POST":
        form = AdminCacheQueryForm(request.POST)
        if form.is_valid():
            key_prefix = form.cleaned_data["key_prefix"]
            key_list = cache.keys(f"{key_prefix}:*")
            return render(
                request, "admin/cache.html", {"key_list": key_list, "query": True}
            )

        if "key_list" in request.POST:
            key_list_str = request.POST["key_list"]
            key_list = key_list_str.split("'")
            key_list = [key for key in key_list[1::2]]
            cache.delete_many(key_list)
            return render(
                request, "admin/cache.html", {"key_list": key_list, "query": False}
            )

    form = AdminCacheQueryForm()
    return render(request, "admin/cache.html", {"form": form})
