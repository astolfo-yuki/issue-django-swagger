class listItemsSerializer(serializers.Serializer):
    block_item = serializers.CharField(required=False, allow_blank=True)
    never_log_item = serializers.BooleanField(required=False, default=False)
    never_learn_item = serializers.BooleanField(required=False, default=False)
    description = serializers.CharField(required=False, allow_blank=True)



class listFiltersSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    cluster = serializers.CharField(required=False, allow_blank=True)
    channel = serializers.CharField(required=False, allow_blank=True)
    partition = serializers.CharField(required=False, allow_blank=True)


class listSerializer(serializers.Serializer):
    filters = listFiltersSerializer(required=False, help_text="list of Rules filters")
    items = serializers.ListField(child=serializers.CharField(), required=True)
    selected = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    select_all = serializers.BooleanField(
        default=False,
        write_only=True,
        help_text=("Set to True to select all objects"),
    )

    def validate(self, data):
        """
        Check if either both selected_status and select_all are configured or 
        we have a list of selected entries in selected
        """
        user = get_current_user()
        if data["select_all"]:
            return data

        if data["select_all"] is False and (
            "selected" not in data or not data["selected"]
        ):
            raise serializers.ValidationError(
                "You must specify either select_all or selected"
            )

        found_count = 0
        if "selected" in data and data["selected"]:
            for d in data["selected"]:
                if Rule.objects.allowed_to_user(user).filter(pk=d).exists():
                    found_count += 1

            if found_count != len(data["selected"]):
                raise serializers.ValidationError(
                    "Some of the selected items are invalid"
                )

        return data

    def get_selected_Rules(self, queryset=None):
        if queryset is None:
            queryset = Rule.objects.all()

        if self.validated_data.get('select_all', False):
            return queryset
        else:
            return queryset.filter(pk__in=self.validated_data['selected'])


class listPostSerializer(listSerializer):
    params = listItemsSerializer(
        required=True, help_text="list of Itemss and setting to apply on selected Rules"
    )
