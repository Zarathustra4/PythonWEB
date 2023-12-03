class PostDto:
    def __init__(self,
                 id,
                 title,
                 text,
                 image,
                 created,
                 enabled,
                 user_id,
                 post_type,
                 category):

        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.created = created
        self.enabled = enabled
        self.user_id = user_id
        self.post_type = post_type
        self.category = category

