// Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause-Clear

#ifndef SUBSCRIBER__SUBSCRIBER_COMPONENT_HPP_
#define SUBSCRIBER__SUBSCRIBER_COMPONENT_HPP_

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/header.hpp>

namespace subscriber
{

class SubscriberComponent : public rclcpp::Node
{
public:
  explicit SubscriberComponent(const rclcpp::NodeOptions & options);

private:
  void on_counter(const std_msgs::msg::Header::SharedPtr msg);

  rclcpp::Subscription<std_msgs::msg::Header>::SharedPtr subscription_;
  bool is_reliable_;
};

}  // namespace subscriber

#endif  // SUBSCRIBER__SUBSCRIBER_COMPONENT_HPP_
