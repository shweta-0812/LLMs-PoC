def create_data(wclient):
    # Create an object
    object_uuid = wclient.data_object.create(
        data_object={
            'question': "Leonardo da Vinci was born in this country.",
            'answer': "Italy",
            'category': "Culture"
        },
        class_name="Question"
    )
    return object_uuid


def read_data(wclient, object_uuid, with_vector=False):
    data_object = wclient.data_object.get_by_id(object_uuid, class_name="Question", with_vector=with_vector)
    return data_object


def update_data(wclient, object_uuid, data_object_filter=None):
    if data_object_filter is None:
        data_object = data_object = wclient.data_object.get_by_id(
            object_uuid,
            class_name='Question',
        )
    else:
        data_object = wclient.data_object.update(
            uuid=object_uuid,
            class_name="Question",
            data_object={
                'answer': "Florence, Italy"
            })

    return data_object


def delete_data(wclient, object_uuid):
    return wclient.data_object.delete(uuid=object_uuid, class_name="Question")


def count(wclient):
    return wclient.query.aggregate("Question").with_meta_count().do()


def get_vectors(wclient):
    # write a query to extract the vector for a sample question
    return (wclient.query
                           .get("questions", ["category", "question", "answer"])
                           .with_additional("vector")
                           .with_limit(1)
                           .do())