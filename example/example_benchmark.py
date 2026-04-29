# Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause-Clear

"""
Live benchmarking for the publisher/subscriber ROS2 pipeline.

BenchmarkMode: BenchmarkMode.LIVE

Pipeline under Test (inter-process, each node in its own process):
    1. publisher::PublisherComponent  (publisher_container)
       Publishes: /counter (std_msgs/msg/Header) at 10 Hz
       - frame_id: incrementing counter value (as string)
       - stamp: publish timestamp (used for E2E latency measurement)

    2. subscriber::SubscriberComponent  (subscriber_container)
       Subscribes: /counter
       Logs received counter values

E2E latency is measured from publisher timestamp (header.stamp) to
receipt at the MonitorNode co-located with the subscriber.

The MonitorNode watches /counter to capture throughput and latency metrics.

Dependency packages (must be built and sourced before running):
    - publisher
    - subscriber

Usage:
    launch_test /path/to/example_benchmark.py
"""

from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

from ros2_benchmark import (
    ROS2BenchmarkConfig,
    ROS2BenchmarkTest,
    BasicPerformanceCalculator,
    BenchmarkMode,
    MonitorPerformanceCalculatorsInfo,
)


def launch_setup(container_prefix, container_sigterm_timeout):
    """Launch publisher and subscriber containers plus a MonitorNode on /counter."""

    # ------------------------------------------------------------------
    # Publisher node (own process)
    # Publishes std_msgs/msg/Header on /counter at 10 Hz.
    # header.stamp is set to the publish time for latency measurement.
    # ------------------------------------------------------------------
    publisher_container = ComposableNodeContainer(
        name='publisher_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        sigterm_timeout=container_sigterm_timeout,
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

    # ------------------------------------------------------------------
    # Subscriber node + MonitorNode (own process)
    # The MonitorNode watches /counter to capture E2E latency metrics.
    # message_key_match=True enables per-message latency tracking using
    # the header.stamp set by the publisher node.
    # ------------------------------------------------------------------
    subscriber_monitor_container = ComposableNodeContainer(
        name='subscriber_monitor_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        sigterm_timeout=container_sigterm_timeout,
        prefix=container_prefix,
        composable_node_descriptions=[
            ComposableNode(
                package='subscriber',
                plugin='subscriber::SubscriberComponent',
                name='subscriber',
                parameters=[{
                    'is_reliable': True,
                }],
            ),
            ComposableNode(
                name='MonitorNode',
                namespace=TestPubSubPipeline.generate_namespace(),
                package='ros2_benchmark',
                plugin='ros2_benchmark::MonitorNode',
                parameters=[{
                    'monitor_index': 1,
                    'monitor_data_format': 'std_msgs/msg/Header',
                }],
                remappings=[('output', '/counter')],
            ),
        ],
        output='screen',
    )

    return [
        publisher_container,
        subscriber_monitor_container,
    ]


def generate_test_description():
    return TestPubSubPipeline.generate_test_description_with_nsys(launch_setup)


class TestPubSubPipeline(ROS2BenchmarkTest):
    """
    Live E2E performance benchmark for the publisher/subscriber ROS2 pipeline.

    Measures end-to-end latency from publisher timestamp to /counter receipt
    at the MonitorNode, throughput of the counter topic, and CPU utilization.
    """

    config = ROS2BenchmarkConfig(
        benchmark_name='Publisher/Subscriber Pipeline E2E Benchmark',

        # LIVE mode: pipeline nodes generate data themselves (no rosbag replay)
        benchmark_mode=BenchmarkMode.LIVE,

        # Run each benchmark iteration for 30 seconds to capture stable metrics
        benchmark_duration=30,

        # Number of benchmark iterations to average
        test_iterations=3,

        # Use monitor timestamps as start time for latency calculation
        collect_start_timestamps_from_monitors=True,

        # Monitor node configuration: watch /counter for E2E latency
        monitor_info_list=[
            MonitorPerformanceCalculatorsInfo(
                'monitor_node1',
                [BasicPerformanceCalculator({
                    'report_prefix': 'pubsub_pipeline',
                    # message_key_match=True: match messages by header.stamp
                    # for accurate per-message E2E latency measurement
                    'message_key_match': True,
                })]
            )
        ],

        custom_report_info={
            'pipeline': 'publisher-subscriber',
            'topic': '/counter',
            'message_type': 'std_msgs/msg/Header',
            'publish_rate_hz': 10.0,
            'e2e_path': 'publisher → /counter → subscriber',
        },
    )

    def test_benchmark(self):
        self.run_benchmark()
