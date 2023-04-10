import { useNavigation } from "@react-navigation/native";
import React from "react";
import { Text, Button, View } from "react-native-ui-lib";
import Icon from "react-native-vector-icons/MaterialIcons";
import { MONTHS } from "../constants/constants";
import { StyleSheet } from "react-native";

const ExpenseDisplay = ({ route }) => {
  const navigation = useNavigation();
  const { groupId, userId, activity } = route.params;
  const handleEdit = () => {
    navigation.push("Edit Expense", { groupId, userId, activity });
  };
  const date = new Date(parseInt(activity?.created_at["$date"]));
  return (
    <View flex>
      <View margin-48>
        <Text style={{ fontWeight: "bold", fontSize: 24 }}>
          Expense Details
        </Text>
        <View row centerV marginV-8 style={{ justifyContent: "flex-start" }}>
          <Icon style={styles.icon} name="receipt" size={24} />
          <Text style={styles.body}>{activity?.description}</Text>
        </View>
        <View row centerV marginV-8 style={{ justifyContent: "flex-start" }}>
          <Icon style={styles.icon} name="attach-money" size={24} />

          <Text style={styles.body}>{activity?.amount}</Text>
        </View>
        <View row centerV marginV-8 style={{ justifyContent: "flex-start" }}>
          <Icon style={styles.icon} name="calendar-today" size={24} />
          <Text style={styles.body}>
            {date.getDate() +
              " " +
              MONTHS[date.getMonth()] +
              " " +
              date.getFullYear()}
          </Text>
        </View>
        <Text style={styles.bodyBold}>
          Added by {userId === activity?.spent_by ? "You" : activity?.user_name}
        </Text>
        <View center>
          <Button label="Edit" style={styles.button} onPress={handleEdit} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  icon: {
    paddingHorizontal: 16,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
  },
  body: {
    fontSize: 18,
    marginVertical: 8,
  },
  bodyBold: {
    fontWeight: "bold",
    fontSize: 18,
    marginVertical: 8,
  },
});

export default ExpenseDisplay;
