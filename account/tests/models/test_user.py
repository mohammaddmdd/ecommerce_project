# from django.test import TestCase
# from django.test.utils import override_settings
# from django.core import mail

# from account.models import User
# # from painless.utils.decorators import disable_logging


# @override_settings(LANGUAGE_CODE='en')
# class UserModelTest(TestCase):
#     """
#     Test whether User-Model functions properly.
#     ------

#     - testing the magic methods : `__str__` and `__repr__`
#     - testing `save` method
#     - testing `verbose_name` (single & plural)
#     """

#     @classmethod
#     # @disable_logging
#     def setUpClass(cls):
#         """creating and preparing data for testing"""

#         super(UserModelTest, cls).setUpClass()
#         cls.PHONE_DIGITS_ONE = '1234567890'
#         cls.PHONE_DIGITS_TWO = '112233445566'
#         cls.user_one = User.objects.create(phone_number=cls.PHONE_DIGITS_ONE)
#         cls.user_two = User.objects.create(phone_number=cls.PHONE_DIGITS_TWO)
#         # for phone_number validation testing
#         cls.PHONE_NUMERIC = '22222⅔'
#         cls.PHONE_NOT_DIGITS = 'asd132'
#         cls.PHONE_EMPTY = ''

#     def test_str_method(self):
#         """testing str method in Cart Model"""

#         actual = str(self.user_one)
#         expected = str(self.user_one.phone_number)
#         self.assertEqual(
#             actual,
#             expected,
#             msg=f"Actual __str__ method is `{actual}` "
#             f"but expected is `{expected}`"
#             )

#     def test_repr_method(self):
#         """testing repr method in Tag Model"""

#         actual = [self.user_one, self.user_two]
#         expected = list(User.objects.all())
#         self.assertEqual(
#             actual,
#             expected,
#             msg=f"Actual __repr__ method is `{actual}` "
#             f"but expected is `{expected}`"
#             )

#     def test_verbose_name(self):
#         """testing verbose name in Tag Model"""

#         actual = User._meta.verbose_name
#         expected = "User"
#         self.assertEqual(
#             actual,
#             expected,
#             msg=f"Actual verbose_name is `{actual}` "
#             f"but expected is `{expected}`"
#             )

#         actual = User._meta.verbose_name_plural
#         expected = "Users"
#         self.assertEqual(
#             actual,
#             expected,
#             msg=f"Actual verbose_name_plural is `{actual}` "
#             f"but expected is `{expected}`"
#             )

#     def test_save_method(self):
#         """testing save method in User Model"""
#         actual_email = self.user_one.email
#         expected_email = None
#         self.assertIs(
#             actual_email,
#             expected_email,
#             msg=f"Actual email is `{actual_email}` "
#             f"but expected email is `{expected_email}`"
#             )
#         actual_first_name = self.user_one.first_name
#         expected_first_name = None
#         self.assertIs(
#             actual_first_name,
#             expected_first_name,
#             msg=f"Actual first name len is `{actual_first_name}` "
#                 f"expected first name is `{expected_first_name}`"
#         )
#         actual_last_name = self.user_one.last_name
#         expected_last_name = None
#         self.assertIs(
#             actual_last_name,
#             expected_last_name,
#             msg=f"Actual last name len is `{actual_last_name}` "
#             f"but expected last name is `{expected_last_name}`"
#             )

#     def test_send_email(self):
#         """
#         Tests Email service, copeid from docs.
#         """
#         mail.send_mail(
#             'Subject here', 'Here is the message.',
#             'from@example.com', ['to@example.com'],
#             fail_silently=False,
#         )

#         # Test that one message has been sent.
#         self.assertEqual(len(mail.outbox), 1)

#         # Verify that the subject of the first message is correct.
#         self.assertEqual(mail.outbox[0].subject, 'Subject here')
