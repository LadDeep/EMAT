import React from "react";
import { Text, View } from "react-native-ui-lib";

const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const ExpenseDate = ({ createdOn }) => {
  const date = new Date(parseInt(createdOn));

  return (
    <View center>
      <Text>{MONTHS[date.getMonth()]}</Text>
      <Text>{date.getDate()}</Text>
      <Text>{date.getDay()}</Text>
    </View>
  );
};

export default ExpenseDate;
