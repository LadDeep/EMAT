import { React, useContext, useState } from "react";
import { Button, TextField, View, Text, Toast } from "react-native-ui-lib";
import { DateTimePicker } from "react-native-ui-lib/src/components/dateTimePicker";
import Icon from "react-native-vector-icons/MaterialIcons";
import { Alert, StyleSheet } from "react-native";
import { CreateExpense } from "../api/api";
import { useNavigation } from "@react-navigation/native";
import MONTHS from "../constants/constants";
import GroupContext from "../Context/GroupContext";

const RegisterExpense = ({ route }) => {
  const [description, setDescription] = useState();
  const [date, setDate] = useState(new Date());
  const [amount, setAmount] = useState()
  const { groupId } = route.params;
  const { setGroupState } = useContext(GroupContext)
  const navigation = useNavigation();

  const handleExpense = () => {
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
          text: "Add",
          onPress: () => {
            CreateExpense(
              {
                description: description,
                amount: parseFloat(amount),
                group_id: groupId,
                date,
              },
              (res) => {
                console.log(res.data.status);
                if (res.data.status) {
                  // TODO: Show toast for successfull creation
                  setGroupState(true)
                  navigation.goBack();
                }
              },
              (err) => { console.log(err) }
            );
          },
        },
      ]);
    }
  }
  console.log(groupId)
  return (
    <View flex marginV-12>
      <View center margin-24>
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
        <Text style={{ marginBottom: 16 }}>
          Paid by You and splitted equally
        </Text>
      </View>
      <Button label="Add" onPress={handleExpense} />
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
  }
});

export default RegisterExpense;
