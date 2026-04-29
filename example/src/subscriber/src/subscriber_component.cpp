// Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause-Clear

#include "subscriber/subscriber_component.hpp"
#include <rclcpp_components/register_node_macro.hpp>

namespace subscriber
{

SubscriberComponent::SubscriberComponent(const rclcpp::NodeOptions & options)
: Node("subscriber_node", options)
{
  // Declare and get parameters
  this->declare_parameter("is_reliable", true);
  is_reliable_ = this->get_parameter("is_reliable").as_bool();

  // Configure QoS profile
  rclcpp::QoS qos(10);
  if (is_reliable_) {
    qos.reliable();
  } else {
    qos.best_effort();
  }

  // Create subscription on /counter topic
  subscription_ = this->create_subscription<std_msgs::msg::Header>(
    "/counter",
    qos,
    std::bind(&SubscriberComponent::on_counter, this, std::placeholders::_1));

  RCLCPP_INFO(
    this->get_logger(),
    "Subscriber node initialized: reliable=%s",
    is_reliable_ ? "true" : "false");
}

void SubscriberComponent::on_counter(const std_msgs::msg::Header::SharedPtr msg)
{
}

}  // namespace subscriber

RCLCPP_COMPONENTS_REGISTER_NODE(subscriber::SubscriberComponent)
