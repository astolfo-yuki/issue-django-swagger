class ActionAPIView(generics.GenericAPIView):
    """
    Base class for all Action views so the filtering is automatically inserted

    """
    filter_class = RESTRuleFilter

    def get_queryset(self):
        return Rule.objects.allowed_to_user(self.request.user)

    def filter_queryset(self, queryset):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            if 'filter' in serializer.validated_data:
                filter = RESTRuleFilter(serializer.validated_data['filter'], queryset=queryset)
                return filter.qs

        return queryset

    def get_serializer(self, *args, **kwargs):
        return listSerializer(*args, **kwargs)


class listItemsApi(ActionAPIView):
    """
    post:
        add one or more Items to selected Rule list

    delete:
        remove one or more Items to selected Rule list

    """
    def get_queryset(self):
        return Rule.objects.allowed_to_user(self.request.user)

    def get_serializer(self, *args, **kwargs):
        return listPostSerializer(*args, **kwargs)

    def get_delete_serializer(self, *args, **kwargs):
        return listSerializer(*args, **kwargs)

    def get_channel(self, list_id):
        bu_list = []
        for i in list_id:
            bu = Channel.objects.allowed_to_user(self.request.user).get(
                pk=i
            )
            bu_list.append({"pk": bu.id, "name": bu.name})

        return bu_list


    
    @swagger_auto_schema(responses={200: listResponseSerializer()})
    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            selected_Rules = serializer.get_selected_Rules(queryset)
            bu_ids, cluster_list, Rules_id = self.build_sets(selected_Rules)
            bu = self.get_channel(bu_ids)

            task_id, timestamp = "sample_task_001"


            response = {
                "channels": bu,
                "task_id": task_id,
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
