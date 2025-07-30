from django.test import TestCase
from adverts.templatetags.round import round_filter


class TestRoundTemplateTag(TestCase):
    def test__round_filter_templatetag__returns_int(self):
        self.assertEqual(round_filter(5.3), 5)