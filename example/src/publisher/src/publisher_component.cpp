// Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause-Clear

#include "publisher/publisher_component.hpp"
#include <rclcpp_components/register_node_macro.hpp>

namespace publisher
{

PublisherComponent::PublisherComponent(const rclcpp::NodeOptions & options)
: Node("publisher_node", options), counter_(0)
{
  // Declare and get parameters
  this->declare_parameter("is_reliable", true);
  this->declare_parameter("publish_rate_hz", 10.0);
  is_reliable_ = this->get_parameter("is_reliable").as_bool();
  publish_rate_hz_ = this->get_parameter("publish_rate_hz").as_double();

  // Configure QoS profile
  rclcpp::QoS qos(10);
  if (is_reliable_) {
    qos.reliable();
  } else {
    qos.best_effort();
  }

  // Create publisher on /counter topic
  publisher_ = this->create_publisher<std_msgs::msg::Header>("/counter", qos);

  // Create timer based on publish rate
  auto period_ms = std::chrono::milliseconds(
    static_cast<int>(1000.0 / publish_rate_hz_));
  timer_ = this->create_wall_timer(
    period_ms,
    std::bind(&PublisherComponent::publish_counter, this));

  RCLCPP_INFO(
    this->get_logger(),
    "Publisher node initialized: rate=%.1f Hz, reliable=%s",
    publish_rate_hz_, is_reliable_ ? "true" : "false");
}

void PublisherComponent::publish_counter()
{
  auto msg = std::make_unique<std_msgs::msg::Header>();
  msg->stamp = this->now();
  msg->frame_id = std::to_string(counter_);

  publisher_->publish(std::move(msg));
  counter_++;
}

}  // namespace publisher

RCLCPP_COMPONENTS_REGISTER_NODE(publisher::PublisherComponent)
