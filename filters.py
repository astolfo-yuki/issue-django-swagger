class RESTRuleFilter(RESTFilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains", help_text="Rule name containing"
    )
    cluster = django_filters.ModelMultipleChoiceFilter(
        queryset=Cluster.objects.all()
    )
    channel = django_filters.ModelMultipleChoiceFilter(
        queryset=Channel.objects.all(), method="subfilter"
    )
    partition = django_filters.CharFilter(
        lookup_expr="icontains", help_text="Partition name containing"
    )
    enforcement_mode = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Enforcement Mode",
        help_text="Enforcement Mode  containing",
    )
    signatureset_name = django_filters.CharFilter(
        label="Rule containing a signature set matching this string",
        field_name="signatureset",
        method="subfilter",
    )

    class Meta:
        model = Rule
        fields = (
            "name",
            "cluster",
            "channel",
            "partition",
            "xxxxxxx",
            "yyyyyyy",
        )
