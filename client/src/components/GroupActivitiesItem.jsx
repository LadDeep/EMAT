import React from "react";
import { ListItem, Text, View } from "react-native-ui-lib";
import Date from "./Date";
import { StyleSheet } from "react-native";

const GroupActivitiesItem = ({ activity }) => {
  return (
    <ListItem style={styles.listItem}>
      <View flex row spread centerV>
        <View row centerV>
          <Date createdOn={activity.created_on} />
          <View paddingL-18>
            <Text style={styles.expenseDescription}>
              {activity.description}
            </Text>
            <Text>{activity.spent_by}</Text>
          </View>
        </View>
        <Text>$ {parseFloat(activity.amount).toFixed(2)}</Text>
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
