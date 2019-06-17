schema_view = get_schema_view(
    openapi.Info(
        title="WAF Management Portal API",
        default_version="v1",
        description="REST api for interaction between Frontend and Backend.",
        contact=openapi.Contact(email="xxx@email.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "rule/", ruleListAPIView.as_view(), name="rule_list_view_api"
    ),
    path(
        "rules/list/", listItemsApi.as_view(), name="list_api"
    ),
    
]
