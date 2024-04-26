# CMS App

This Django app provides functionality for managing content such as blogs, comments, likes, views, and tags.

## Installation

To install the CMS app, follow these steps:

1. Add `'cms'` to your `INSTALLED_APPS` setting.
2. Ensure you have the necessary dependencies installed, such as `Pillow` for image processing.

## Models Documentation

### CommonInfoMixin

- `title`: CharField for the title of the content.
- `slug`: SlugField for generating a unique slug based on the title.
- `status`: ChoiceField for defining the status of the content (public, unpublished, draft).
- `created_at`: DateTimeField for storing the creation date of the content.
- `updated_at`: DateTimeField for storing the last update date of the content.
- `site`: ForeignKey to the Site model, representing the site where the content is hosted.
- `author`: ForeignKey to the User model, representing the author of the content.
- `main_image`: ImageField for storing the main image associated with the content.
- `thumbnail_image`: ImageField for storing the thumbnail image associated with the content.

### TaggingMixin

- `tags`: ManyToManyField for associating tags with content.

### LikeViewCountMixin

- `likes`: GenericRelation for associating likes with content.
- `views`: GenericRelation for associating views with content.
- `increment_view_count()`: Method to increment the view count of the content.
- `add_like(user)`: Method to add a like to the content for a specific user.
  - **Usage**: Call this method with the `user` parameter to add a like to the content.
- `remove_like(user)`: Method to remove a like from the content for a specific user.
  - **Usage**: Call this method with the `user` parameter to remove a like from the content.

### CommentMixin

- `comments`: GenericRelation for associating comments with content.
- `add_comment(author, body)`: Method to add a comment to the content.
  - **Usage**: Call this method with the `author` and `body` parameters to add a comment to the content.
- `remove_comment(comment_id)`: Method to remove a comment from the content.
  - **Usage**: Call this method with the `comment_id` parameter to remove a comment from the content.

### Tag

- `name`: CharField for the name of the tag.

### Like

- `user`: ForeignKey to the User model, representing the user who liked the content.
- `content_type`: ForeignKey to the ContentType model, representing the type of content liked.
- `object_id`: PositiveIntegerField representing the ID of the content liked.
- `content_object`: GenericForeignKey to the content liked.
- `created_at`: DateTimeField for storing the date and time when the like was created.

### View

- `content_type`: ForeignKey to the ContentType model, representing the type of content viewed.
- `object_id`: PositiveIntegerField representing the ID of the content viewed.
- `content_object`: GenericForeignKey to the content viewed.
- `count`: PositiveIntegerField for storing the count of views.
- `last_viewed`: DateTimeField for storing the date and time of the last view.

### Comment

- `body`: TextField for the body/content of the comment.
- `content_type`: ForeignKey to the ContentType model, representing the type of content commented on.
- `object_id`: PositiveIntegerField representing the ID of the content commented on.
- `content_object`: GenericForeignKey to the content commented on.
- `author`: ForeignKey to the User model, representing the author of the comment.
- `created_at`: DateTimeField for storing the date and time when the comment was created.

### Blog

- Inherits from `CommonInfoMixin`, `TaggingMixin`, `CommentMixin`, and `LikeViewCountMixin`.
- `category`: ForeignKey to the Category model, representing the category of the blog.

### Category

- `name`: CharField for the name of the category.
- `description`: TextField for the description of the category.

## Usage

To use the models provided by the CMS app:

1. **Model Inheritance**: Inherit from the appropriate mixins (`CommonInfoMixin`, `TaggingMixin`, `CommentMixin`, `LikeViewCountMixin`) based on your content requirements.
2. **Custom Methods**: Utilize the provided methods such as `add_comment`, `remove_comment`, `increment_view_count`, `add_like`, and `remove_like` as needed. Refer to the detailed usage instructions provided for each method.
3. **Customization**: Customize field attributes and behavior as per your project's requirements.

Refer to the individual model documentation for detailed information on each model's fields and methods.
