import React from "react";
import { View, Text } from "react-native-ui-lib";

const OverallExpenseDisplay = () => {
  return (
    <View>
      <Text
        style={{
          fontSize: 18,
          marginBottom: 12,
          // color: `${expense > 0 ? "red" : "green"}`,
        }}
      >
        Overall, you're owed $ x
      </Text>
      {/* iterate through overall expense standing with each and every group member and render accordingly*/}
      <View>
        <Text
          style={{
            fontSize: 16,
            paddingTop: 4,
            color: `${-300 > 0 ? "red" : "green"}`,
          }}
        >
          You're owed ${300} by someone
        </Text>
        <Text
          style={{
            fontSize: 16,
            paddingTop: 4,
            color: `${-300 > 0 ? "red" : "green"}`,
          }}
        >
          You're owed ${300} by someone
        </Text>
        <Text
          style={{
            fontSize: 16,
            paddingTop: 4,
            color: `${-300 > 0 ? "red" : "green"}`,
          }}
        >
          You're owed ${300} by someone
        </Text>
        <Text
          style={{
            fontSize: 16,
            paddingTop: 4,
            color: `${150 > 0 ? "red" : "green"}`,
          }}
        >
          You owe ${150} to someone
        </Text>
      </View>
    </View>
  );
};

export default OverallExpenseDisplay;
