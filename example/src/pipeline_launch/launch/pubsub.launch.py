# Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause-Clear

"""
Launch file for the publisher/subscriber pipeline.

Pipeline structure:
- publisher node runs in its own process (publisher_container)
- subscriber node runs in its own process (subscriber_container)

The publisher publishes an incrementing counter on /counter at 10 Hz.
The subscriber receives and logs the counter values.
"""

from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    # Publisher runs in its own process
    publisher_container = ComposableNodeContainer(
        name='publisher_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='publisher',
                plugin='publisher::PublisherComponent',
                name='publisher',
                parameters=[{
                    'is_reliable': True,
                    'publish_rate_hz': 10.0,
                }],
            ),
        ],
        output='screen',
    )

    # Subscriber runs in its own process
    subscriber_container = ComposableNodeContainer(
        name='subscriber_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='subscriber',
                plugin='subscriber::SubscriberComponent',
                name='subscriber',
                parameters=[{
                    'is_reliable': True,
                }],
            ),
        ],
        output='screen',
    )

    return LaunchDescription([
        publisher_container,
        subscriber_container,
    ])
