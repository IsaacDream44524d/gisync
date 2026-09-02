from wtforms.validators import ValidationError
import re

class FormValidators:

    @staticmethod
    def schoolEmail(email, message=None):
        pass

    @staticmethod
    def classEmail(message=None):
        email_regex = r'^gis(?:/\d+/\d+|\d+)(?:@must\.ac\.mw)?$'

        def _validator(form, field):
            error_msg = message or 'Please enter your school email'

            if field.data and not re.match(email_regex, str(field.data)):
                raise ValidationError(error_msg)

        return _validator

    @staticmethod
    def parse_group_names(text):
        group_names = []
        seen = set()

        for name in text.splitlines():
            name = name.strip()

            if not name:
                continue

            key = name.lower()

            if key in seen:
                raise ValueError(f"Duplicate group name: {name}")

            seen.add(key)
            group_names.append(name)

        return group_names
