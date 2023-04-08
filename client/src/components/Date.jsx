import React from "react";
import { Text, View } from "react-native-ui-lib";
import MONTHS from "../constants/constants";

const ExpenseDate = ({ createdOn }) => {
  const date = new Date(parseInt(createdOn));

  return (
    <View center>
      <Text>{MONTHS[date.getMonth()]}</Text>
      <Text>{date.getDate()}</Text>
    </View>
  );
};

export default ExpenseDate;
