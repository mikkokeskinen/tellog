from voluptuous import (Schema, Required, Optional)

user_schema = Schema({
    Required("id"): int,
    Required("first_name"): str,
    Optional("last_name"): str,
    Optional("username"): str,
})

chat_schema = Schema({
    Required("id"): int,
    Required("type"): str,
    Optional("title"): str,
    Optional("username"): str,
    Optional("first_name"): str,
    Optional("last_name"): str,
    Optional("all_members_are_administrators"): bool,
})

message_entity_schema = Schema({
    Required("type"): str,
    Required("offset"): int,
    Required("length"): int,
    Optional("url"): str,
    Optional("user"): user_schema,
})

audio_schema = Schema({
    Required("file_id"): str,
    Required("duration"): int,
    Optional("performer"): str,
    Optional("title"): str,
    Optional("mime_type"): str,
    Optional("file_size"): int,
})

photo_size_schema = Schema({
    Required("file_id"): str,
    Required("width"): int,
    Required("height"): int,
    Optional("file_size"): int,
})

document_schema = Schema({
    Required("file_id"): str,
    Optional("thumb"): photo_size_schema,
    Optional("file_name"): str,
    Optional("mime_type"): str,
    Optional("file_size"): int,
})

animation_schema = Schema({
    Required("file_id"): str,
    Optional("thumb"): photo_size_schema,
    Optional("file_name"): str,
    Optional("mime_type"): str,
    Optional("file_size"): int,
})

game_schema = Schema({
    Required("title"): str,
    Required("description"): str,
    Required("photo"): [photo_size_schema],
    Optional("text"): str,
    Optional("text_entities"): [message_entity_schema],
    Optional("animation"): animation_schema,
})

sticker_schema = Schema({
    Required("file_id"): str,
    Required("width"): int,
    Required("height"): int,
    Optional("thumb"): photo_size_schema,
    Optional("emoji"): str,
    Optional("file_size"): int,
})

video_schema = Schema({
    Required("file_id"): str,
    Required("width"): int,
    Required("height"): int,
    Required("duration"): int,
    Optional("thumb"): photo_size_schema,
    Optional("mime_type"): str,
    Optional("file_size"): int,
})

voice_schema = Schema({
    Required("file_id"): str,
    Required("duration"): int,
    Optional("mime_type"): str,
    Optional("file_size"): int,
})

contact_schema = Schema({
    Required("phone_number"): str,
    Required("first_name"): str,
    Optional("last_name"): str,
    Optional("user_id"): int,
})

location_schema = Schema({
    Required("latitude"): float,
    Required("longitude"): float,
})

venue_schema = Schema({
    Required("location"): location_schema,
    Required("title"): str,
    Required("address"): str,
    Optional("foursquare_id"): str,
})


def message_schema_wrapper(value):
    return message_schema(value)


message_schema = Schema({
    Required("message_id"): int,
    Optional("from"): user_schema,
    Required("date"): int,
    Required("chat"): chat_schema,
    Optional("forward_from"): user_schema,
    Optional("forward_from_chat"): chat_schema,
    Optional("forward_from_message_id"): int,
    Optional("forward_date"): int,
    Optional("reply_to_message"): message_schema_wrapper,
    Optional("edit_date"): int,
    Optional("text"): str,
    Optional("entities"): [message_entity_schema],
    Optional("audio"): audio_schema,
    Optional("document"): document_schema,
    Optional("game"): game_schema,
    Optional("photo"): [photo_size_schema],
    Optional("sticker"): sticker_schema,
    Optional("video"): video_schema,
    Optional("voice"): voice_schema,
    Optional("caption"): str,
    Optional("contact"): contact_schema,
    Optional("location"): location_schema,
    Optional("venue"): venue_schema,
    Optional("new_chat_member"): user_schema,
    Optional("new_chat_members"): [user_schema],  # Undocumented
    Optional("left_chat_member"): user_schema,
    Optional("new_chat_participant"): user_schema,  # Deprecated
    Optional("left_chat_participant"): user_schema,  # Deprecated
    Optional("new_chat_title"): str,
    Optional("new_chat_photo"): [photo_size_schema],
    Optional("delete_chat_photo"): True,
    Optional("group_chat_created"): True,
    Optional("supergroup_chat_created"): True,
    Optional("channel_chat_created"): True,
    Optional("migrate_to_chat_id"): int,
    Optional("migrate_from_chat_id"): int,
    Optional("pinned_message"): message_schema_wrapper,
})

telegram_schema = Schema({
    Required("update_id"): int,
    Optional("message"): message_schema,
    Optional("edited_message"): message_schema,
    Optional("channel_post"): message_schema,
    Optional("edited_channel_post"): message_schema,
})

