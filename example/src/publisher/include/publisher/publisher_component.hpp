// Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause-Clear

#ifndef PUBLISHER__PUBLISHER_COMPONENT_HPP_
#define PUBLISHER__PUBLISHER_COMPONENT_HPP_

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/header.hpp>

namespace publisher
{

class PublisherComponent : public rclcpp::Node
{
public:
  explicit PublisherComponent(const rclcpp::NodeOptions & options);

private:
  void publish_counter();

  rclcpp::Publisher<std_msgs::msg::Header>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  uint64_t counter_;
  bool is_reliable_;
  double publish_rate_hz_;
};

}  // namespace publisher

#endif  // PUBLISHER__PUBLISHER_COMPONENT_HPP_
