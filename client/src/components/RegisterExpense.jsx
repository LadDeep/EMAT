import { React, useState } from "react";
import { Button, TextField, View, Text } from "react-native-ui-lib";
import { DateTimePicker } from "react-native-ui-lib/src/components/dateTimePicker";
import Icon from "react-native-vector-icons/MaterialIcons";
import { StyleSheet } from "react-native";

const RegisterExpense = ({ mode }) => {
  const [description, setDescription] = useState();
  const [date, setDate] = useState(new Date());
  const handleExpense = ()=>{
    // TODO: Add api call to save expense
    console.log("expense")
  }
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
          <Icon style={styles.icon} name="calendar-today" size={24} />
          <DateTimePicker
          style={styles.input}
            title={"Select date"}
            mode="date"
            value={date}
            onChange={(date) => setDate(date)}
          />
        </View>
        <Text style={{marginBottom: 16}}>Paid by you and splitted equally</Text>
        <Button label={`${mode === "Add" ? "Add" : "Save"} Expense`} onPress={handleExpense}/>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    width: "80%",
    marginHorizontal: 8,
  },
  icon:{
    paddingHorizontal: 16
  }
});

export default RegisterExpense;
