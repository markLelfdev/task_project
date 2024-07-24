add
                # print(f'{config_option_data = }')
                # print(f'{instance = }')
                ConfigulationOption.objects.create(config_item=instance, **config_option_data)
                # ConfigulationOptionSerializer(context=self.context).create(validated_data=config_option_data)
                # options_serializer =  ConfigulationOptionSerializer(data=config_option_data, context=self.context)
                # options_serializer.is_valid(raise_exception=True)
                # options_serializer.save()


                {
    "id": 3,
    "index": 1,
    "title": "test_update",
    "field": "update_now",
    "config_type": "Options",
    "required": true,
    "description": "new description",
    "created_at": "2024-07-24T02:59:41.031811Z",
    "updated_at": "2024-07-24T02:59:41.031821Z",
    "options": [
        {
            "id": 2,
            "created_at": "2024-07-24T09:59:41.046006+07:00",
            "updated_at": "2024-07-24T09:59:41.046030+07:00",
            "index": 1,
            "title": "data",
            "value": 101.25
        },
        {
            "id": 3,
            "created_at": "2024-07-24T09:59:41.046151+07:00",
            "updated_at": "2024-07-24T09:59:41.046164+07:00",
            "index": 2,
            "title": "normal",
            "value": 76.0
        }
    ]
}
