from typing_extensions import Optional
from typing import Callable

# from rclpy.qos import QoSProfile, ReliabilityPolicy
import rclpy

from tmc_voice_msgs.msg import Voice
from ..ros.ros2.publisher import create_publisher

import logging
logger = logging.getLogger(__name__)


import rclpy
from tmc_voice_msgs.msg import Voice
from ..ros.ros2.publisher import create_publisher
from rclpy.qos import QoSProfile, ReliabilityPolicy

class TextToSpeechPublisher:
    def __init__(self, node_name="tts", topic_name="/talk_request"):
        self.node = rclpy.create_node(node_name)
        qos = QoSProfile(depth=2, reliability=ReliabilityPolicy.RELIABLE)
        self.pub = create_publisher(topic_name, Voice, self.node, qos)

    def say(self, content: str):
        msg = Voice()
        msg.language = 1
        msg.sentence = content or ""
        self.pub.publish(msg)


class TextToSpeechPublisher:

    # Surprise its' initializations
    is_init = False
    rclpy.init()
    tts_node = rclpy.create_node("tts")
    # qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE), would replace queue size
    tts_pub = create_publisher("/talk_request", Voice, tts_node, 2)

    @staticmethod
    def init_talk_interface(func: Callable) -> Callable:
        """Ensures initialization of the navigation interface before function execution."""

        def wrapper(*args, **kwargs):
            # Check if the interface is already initialized
            if TextToSpeechPublisher.is_init:
                return func(*args, **kwargs)
            try:
                from tmc_voice_msgs.msg import Voice        # This import is only needed if you intend to use voice
            except ImportError:
                logger.warning("Failed to import tmc_voice_msgs - package may not be installed")
                return None
            TextToSpeechPublisher.is_init = True
            logger.info("Successfully initialized tmc interface")

            return func(*args, **kwargs)
        return wrapper

    @init_talk_interface
    def say(self, content : Optional[str] = ""):
        """

        :param content: The message to be spoken
        :return:
        """

        talk_pub = TextToSpeechPublisher.tts_pub
        msg = Voice()

        msg.language = 1
        msg.sentence = content

        talk_pub.publish(msg)
        return