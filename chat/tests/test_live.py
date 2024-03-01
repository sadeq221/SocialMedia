import time
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    staleness_of,
)

from app.models import User
from chat.models import ChatRoom, Message
from chat.serializers import ChatMessageSerializer
from rest_framework_simplejwt.tokens import AccessToken


class ChatTests(ChannelsLiveServerTestCase):
    # Subclass ChannelsLiveServerTestCase with serve_static = True in order to
    # serve static files (comparable to Django’s StaticLiveServerTestCase,
    # you don’t need to run collectstatic before or as a part of your tests setup).
    serve_static = True  # emulate StaticLiveServerTestCase

    def setUp(self):
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            self.driver = webdriver.Chrome()

            # Initialing some database objects
            # Create two different users
            self.sadeq = User.objects.create(
                first_name="Sadeq", last_name="Mousawi", email="homam.s11@gmail.com"
            )
            self.hosein = User.objects.create(
                first_name="Hosein", last_name="Gorji", email="hosein_gorji@gmail.com"
            )

            # Get access tokens for them
            self.token_sadeq = str(AccessToken.for_user(self.sadeq))
            self.token_hosein = str(AccessToken.for_user(self.hosein))

            # Sadeq creates a chatroom for the teachers (He is the admin)
            self.teachers_room = ChatRoom.objects.create(
                name="teachers", creator=self.sadeq
            )
            # Add Hosein to teachers room
            self.teachers_room.members.add(self.hosein)

            # Hosein creates a chatroom for the students (He is the admin)
            self.students_room = ChatRoom.objects.create(
                name="students", creator=self.hosein
            )
            # Add Sadeq to students room
            self.students_room.members.add(self.sadeq)

            # Saving a Message for Sadeq in teachers room (to be history recorded)
            self.message = Message.objects.create(
                thread="teachers", sender=self.sadeq, content="Hello"
            )
        except:
            self.tearDown()
            raise

    def tearDown(self):
        self.driver.quit()

    def test_greeting_is_shown(self):
        try:
            self._get_chatrooms(self.token_sadeq)

            # Wait for the element to be generated
            greet_header = WebDriverWait(self.driver, 1).until(
                presence_of_element_located((By.CSS_SELECTOR, "#greeting-header")),
                "Greeting header was not found",
            )

            WebDriverWait(self.driver, 2).until(
                lambda _: self.sadeq.full_name() in greet_header.text,
                "Name is not shown in the greeting header",
            )
        finally:
            self._close_all_new_windows()

    def test_chatrooms_are_shown(self):
        try:
            # Enter the token to get the rooms
            self._get_chatrooms(self.token_sadeq)
            alaki = presence_of_element_located((By.CSS_SELECTOR, "#teachers h3"))
            # Get the room title element
            teachers_room_title = WebDriverWait(self.driver, 1).until(
                presence_of_element_located((By.CSS_SELECTOR, "#teachers h3")),
                "Teachers room-title h3 doesn't exist",
            )
            # Check its text (showing the correct room name)
            WebDriverWait(self.driver, 1).until(
                lambda _: teachers_room_title.text == self.teachers_room.name,
                "Teachers room-title not shown",
            )

            # Get the room title element
            students_room_title = WebDriverWait(self.driver, 1).until(
                presence_of_element_located((By.CSS_SELECTOR, "#students h3")),
                "students room-title h3 doesn't exist",
            )
            # Check its text (showing the correct room name)
            WebDriverWait(self.driver, 1).until(
                lambda _: students_room_title.text == self.students_room.name,
                "Students room-title not shown",
            )
        finally:
            self._close_all_new_windows()

    def test_message_history_is_shown(self):
        try:
            # Enter the token to get the rooms
            self._get_chatrooms(self.token_sadeq)

            # Get the room title element
            teachers_room_log = WebDriverWait(self.driver, 1).until(
                presence_of_element_located((By.CSS_SELECTOR, "#teachers textarea")),
                "Teachers room-title h3 doesn't exist",
            )

            # Serialize the message object
            message = ChatMessageSerializer(self.message).data
            # Format it as expected
            formatted_message = f"{message['sender_name']}: {message['content']} {message['date_time']}\n"

            # Get the message that is shown in room
            shown_message = teachers_room_log.get_property("value")

            # Check the message (which came from database)
            WebDriverWait(self.driver, 1).until(
                lambda _: formatted_message == shown_message,
                "Message not shown",
            )
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            # Start the app for Sadeq
            self._get_chatrooms(self.token_sadeq)

            # Open a new tab
            self._open_new_tab()
            # Focus on it
            self._switch_to_window(-1)

            # Start the app for Hosein
            self._get_chatrooms(self.token_hosein)

            # Go back to Sadeq's window
            self._switch_to_window(0)

            # Sadeq sends a message in students room
            self._post_message(room="students", message="same room recieves")

            # Insure the message is recieved by Sadeq himself
            WebDriverWait(self.driver, 1).until(
                lambda _: "same room recieves" in self._get_chat_log_value("students"),
                "Sadeq himself not getting his message.",
            )

            # Go to Hosein's window
            self._switch_to_window(-1)

            # Insure the message is recieved by Hosein
            WebDriverWait(self.driver, 1).until(
                lambda _: "same room recieves" in self._get_chat_log_value("students"),
                "Hosein not getting Sadeq's message",
            )
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            # Start the app for Sadeq
            self._get_chatrooms(self.token_sadeq)

            # Open a new tab
            self._open_new_tab()
            # Focus on it
            self._switch_to_window(-1)

            # Start the app for Hosein
            self._get_chatrooms(self.token_hosein)

            # Go back to Sadeq's window
            self._switch_to_window(0)

            # Sadeq sends a message in students room
            self._post_message(room="students", message="other rooms not recieve")

            # Go to Hosein's window
            self._switch_to_window(-1)

            # Insure the message is not recieved by Hosein in "teachers" room
            WebDriverWait(self.driver, 1).until(
                lambda _: not "other rooms not recieve"
                in self._get_chat_log_value("teachers"),
                "Hosein is getting Sadeq's message from different room",
            )
        finally:
            self._close_all_new_windows()

    def test_when_leave_room_then_room_is_removed(self):
        try:
            # Start the app for Sadeq
            self._get_chatrooms(self.token_sadeq)

            # Get the leave button
            students_leave_button = self._wait_for_element("#students .leaveButton", 1)

            # Sadeq leaves students room (by pressing the button)
            ActionChains(self.driver).click(students_leave_button).perform()

            # Get Sadeq's rooms again (after reloading)
            self._get_chatrooms(self.token_sadeq)

            # Insure that students room is removed for Sadeq (leave button no longer exists)
            WebDriverWait(self.driver, 1).until(
                staleness_of(students_leave_button),
                "Students room is not removed for Sadeq after leaving.",
            )
        finally:
            self._close_all_new_windows()

    def test_when_kicked_out_then_room_is_removed(self):
        try:
            # Start the app for Sadeq
            self._get_chatrooms(self.token_sadeq)

            # Open a new tab
            self._open_new_tab()
            # Focus on it
            self._switch_to_window(-1)

            # Start the app for Hosein
            self._get_chatrooms(self.token_hosein)

            # Hosein kicks Sadeq out of students room
            self._kick_out("students", self.sadeq.id)

            # Go back to Sadeq's window
            self._switch_to_window(0)

            # Get Sadeq's rooms again (after reloading)
            self._get_chatrooms(self.token_sadeq)

            # Insure that students room is removed for Sadeq after being kicked out
            try:
                # Try to get student room
                self._wait_for_element("#students", 1)
                self.fail("Students room still exists for Sadeq after being kicked out")
            except:
                pass
        finally:
            self._close_all_new_windows()

    # === Utility ===
    # Opens the main page and enters the token (to get user's chatrooms)
    def _get_chatrooms(self, token):
        self.driver.get(f"{self.live_server_url}/chat/chatrooms")
        token_input = self._wait_for_element("#token-input", 1)
        send_button = self._wait_for_element("#token-submit", 1)
        ActionChains(self.driver).click(token_input).send_keys(token).click(
            send_button
        ).perform()

    def _open_new_tab(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, room, message):
        # Get the message input
        message_input = self._wait_for_element(f"#{room} .messageInput", 1)
        # Get the send button
        send_button = self._wait_for_element(f"#{room} .sendButton", 1)
        # Send the message
        ActionChains(self.driver).click(message_input).send_keys(message).click(
            send_button
        ).perform()

    def _kick_out(self, room, user_id):
        user_id_input = self._wait_for_element(f"#{room} .kickedUserIdInput", 1)
        kick_button = self._wait_for_element(f"#{room} .kickButton", 1)

        ActionChains(self.driver).click(user_id_input).send_keys(user_id).click(
            kick_button
        ).perform()

    def _wait_for_element(self, selector, time):
        return WebDriverWait(self.driver, time).until(
            presence_of_element_located((By.CSS_SELECTOR, selector)),
            f"{selector} element doesn't exist",
        )

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self._switch_to_window(-1)
            self.driver.execute_script("window.close();")
        if len(self.driver.window_handles) == 1:
            self._switch_to_window(0)

    def _get_chat_log_value(self, room):
        # Get chat log (textarea) of a specific room
        return (
            WebDriverWait(self.driver, 1)
            .until(
                presence_of_element_located((By.CSS_SELECTOR, f"#{room} textarea")),
                "Chat log (textarea element) doesn't exist",
            )
            .get_property("value")
        )
