import { React, useContext, useState } from "react";
import { Button, TextField, View, Text, Toast } from "react-native-ui-lib";
import { DateTimePicker } from "react-native-ui-lib/src/components/dateTimePicker";
import Icon from "react-native-vector-icons/MaterialIcons";
import { Alert, StyleSheet } from "react-native";
import { UpdateExpenseInfo } from "../api/api";
import { useNavigation } from "@react-navigation/native";
import GroupContext from "../Context/GroupContext";
import {MONTHS} from "../constants/constants";

const UpdateExpense = ({ route }) => {
  const { groupId, activity, userId } = route.params;
  const [description, setDescription] = useState(activity.description);
  const [date, setDate] = useState(new Date(parseInt(activity.created_at["$date"])));
  const [amount, setAmount] = useState(activity.amount)
  const { setGroupState } = useContext(GroupContext)
  const navigation = useNavigation();
  console.log("This is Activity", activity)

  const handleEditExpense = () => {
    if (description !== "" && amount !== undefined) {
      let creationDate =
        date.getDate() +
        " " +
        MONTHS[date.getMonth()] +
        " " +
        date.getFullYear();

      let alertTitle = "Are you sure?";
      let alertMessage = "You paid $" + amount + " for " + description + " on " + creationDate;
      Alert.alert(alertTitle, alertMessage, [
        {
          text: "Cancel",
        },
        {
          text: "Save",
          onPress: () => {
            UpdateExpenseInfo(
              {
                expense_id: activity.expense_id,
                group_id: groupId,
                description: description,
                amount: parseFloat(amount),
                created_at: date,
              },
              (res) => {
                console.log(res.data);
                if (res.data.status) {
                  // TODO: Show toast for successfull creation
                  console.log("response of Update List Page", res)
                  let updatedActivity = {
                    ...activity,
                    description: description,
                    amount: parseFloat(amount),
                    created_at: {
                      '$date': date.getTime(),
                    },
                  }
                  setGroupState(!groupState)
                  console.log("OLD ACTIVITY", activity)
                  console.log("UPDATED ACTIVITY+++++++++++++++++++++++++++", updatedActivity)

                  navigation.navigate("Expense", { groupId, activity: updatedActivity, userId });
                }
              },
              (err) => { console.log("err", err) }
            );
          },
        },
      ]);
    }
  }
  return (
    <View flex>
      <View center margin-24>
        <Text style={styles.fontTitle}>Customize Expense</Text>
        <View row center>
          <Icon style={styles.icon} name="receipt" size={24} />
          <TextField
            style={styles.input}
            value={description}
            placeholder={"Description"}
            floatingPlaceholder
            onChangeText={(text) => {
              setDescription(text);
            }}
          />
        </View>
        <View row center>
          <Icon style={styles.icon} name="attach-money" size={24} />
          <TextField
            style={styles.input}
            value={amount}
            placeholder={"Amount"}
            floatingPlaceholder
            inputType={"numeric"}
            keyboardType={"numeric"}
            onChangeText={(text) => {
              setAmount(text);
            }}
          />
        </View>
        <View row center>
          <Icon style={styles.icon} name="calendar-today" size={24} />
          <DateTimePicker
            style={styles.input}
            title={"Select date"}
            mode="date"
            value={date}
            onChange={(date) => setDate(date)}
          />
        </View>
        <View row center>
          <Text style={styles.body}>Paid by </Text>
          <Text style={styles.bodyBold}>
            {userId === activity.spent_by ? "You" : activity.user_name}
          </Text>
          <Text style={styles.body}> and splitted equally</Text>
        </View>
        <Button
          label="Save"
          style={styles.button}
          onPress={handleEditExpense}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    width: "80%",
    marginHorizontal: 8,
    marginVertical: 0,
  },
  icon: {
    paddingHorizontal: 16
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
  },
  fontTitle: { fontWeight: "bold", fontSize: 24, marginVertical: 12 },
  body:{
    fontSize: 18,
    marginVertical: 8,
  },
  bodyBold:{
    fontWeight: "bold",
    fontSize: 18,
    marginVertical: 8,
  }
});

export default UpdateExpense;
