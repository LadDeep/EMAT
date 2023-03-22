import React, { useState } from "react";
import { Avatar, TextField, View, Picker, Button } from "react-native-ui-lib";
import { StyleSheet } from "react-native";

const GroupDetailsEdit = ({route}) => {
  const {id, name, currency} = route.params
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [groupName, setGroupName] = useState("XYZ");
  const handleDetailsEdit = ()=>{
    // TODO: API call to save changes
  }
  return (
    <View flex marginH-56>
      <View flex marginV-24>
        <View row center spread>
          <View row centerH>
            <Avatar
              size={72}
              source={{ uri: "" }}
              containerStyle={{ marginRight: 8 }}
            />
            <TextField
              style={styles.input}
              value={groupName}
              placeholder={"Group Name"}
              floatingPlaceholder
              onChangeText={(text) => {
                setGroupName(text);
              }}
            />
          </View>
        </View>
        <Picker
          value={baseCurrency}
          style={styles.picker}
          placeholder={"Base Currency"}
          floatingPlaceholder
          onChange={(itemValue, itemIndex) => setBaseCurrency(itemValue)}
        >
          <Picker.Item label="USD" value="USD" />
          <Picker.Item label="EUR" value="EUR" />
          <Picker.Item label="GBP" value="GBP" />
          <Picker.Item label="INR" value="INR" />
          <Picker.Item label="JPY" value="JPY" />
        </Picker>
        <Button
          label="Save"
          onPress={() => {
            handleDetailsEdit();
          }}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    width: 200,
    height: 44,
    padding: 10,
    // marginBottom: 10,
  },
  picker: {
    width: 200,
    height: 44,
  },
});

export default GroupDetailsEdit;
