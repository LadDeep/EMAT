import React from "react";
import { ListItem, Text, View } from "react-native-ui-lib";
import Date from "./Date";
import { StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";

const GroupActivitiesItem = ({groupId, activity }) => {
  const navigation = useNavigation();
  const handleExpenseDescription = ()=>{
    navigation.push("Expense", {groupId, activity});
  }
  return (
    <ListItem style={styles.listItem} onPress={handleExpenseDescription}>
      <View flex row spread centerV>
        <View row centerV>
          <Date createdOn={activity?.created_at["$date"]} />
          <View paddingL-18 paddingV-0>
            <Text style={styles.expenseDescription}>
              {activity.description}
            </Text>
            <Text>
              Spent by {activity.user_name} $
              {parseFloat(activity.amount).toFixed(2)}
            </Text>
          </View>
        </View>
        <Text
          style={{
            color: `${activity.user_name === "You" ? "green" : "red"}`,
          }}
        >
          ${parseFloat(activity.lent_or_borrowed_amount).toFixed(2)}
        </Text>
      </View>
    </ListItem>
  );
};

export default GroupActivitiesItem;

const styles = StyleSheet.create({
  listItem: {
    marginHorizontal: 8,
    justifyContent: "space-around",
    alignItems: "center",
  },
  expenseDescription: { fontWeight: "bold", fontSize: 16 },
});
