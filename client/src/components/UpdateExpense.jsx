import { React, useState } from "react";
import { Button, TextField, View, Text, Toast } from "react-native-ui-lib";
import { DateTimePicker } from "react-native-ui-lib/src/components/dateTimePicker";
import Icon from "react-native-vector-icons/MaterialIcons";
import { Alert, StyleSheet } from "react-native";
import { UpdateExpenseInfo } from "../api/api";
import { useNavigation } from "@react-navigation/native";
import MONTHS from "../constants/constants";

const UpdateExpense = ({ route }) => {
  const {groupId, activity} = route.params;
  const [description, setDescription] = useState(activity.description);
  const [date, setDate] = useState(new Date(parseInt(activity.created_at["$date"])));
  const [amount, setAmount] = useState(activity.amount)
  const navigation = useNavigation();

  const handleEditExpense = ()=>{
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
                console.log(res.data.status);
                if (res.data.status) {
                  // TODO: Show toast for successfull creation
                  navigation.goBack();
                }
              },
              (err) => {}
            );
          },
        },
      ]);
    }
  }
  console.log(groupId)
  return (
    <View flex >
      <View center margin-24>
        <View row center>
          <Icon style={styles.icon} name="receipt" size={24}/>
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
          <Icon style={styles.icon} name="attach-money" size={24}/>
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
        <Text style={{marginBottom: 16}}>Paid by You and splitted equally</Text>
        <Button label="Save" onPress={handleEditExpense}/>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    width: "80%",
    marginHorizontal: 8,
    marginVertical:0,
  },
  icon:{
    paddingHorizontal: 16
  }
});

export default UpdateExpense;
