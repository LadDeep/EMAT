import React, { useState } from "react";
import { TextInput, StyleSheet, ScrollView } from "react-native";
import {
  Avatar,
  Button,
  ChipsInput,
  Text,
  View,
  Picker,
  Checkbox,
  DateTimePicker,
} from "react-native-ui-lib";

export const GroupRegistrationForm = () => {
  const [membersList, setMembersList] = useState([]);
  const [email, setEmail] = useState("");
  const [groupName, setGroupName] = useState("");
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [isTemporary, setIsTemporary] = useState(false);
  const [destructionDate, setDestructionDate] = useState(new Date());
  const chipInputRef = React.createRef();

  const addEmail = (event) => {
    if (event.nativeEvent.key == "Enter") {
      setMembersList([...membersList, { label: email }]);
    }
  };
  const handleRegistration = () => {
    if (groupName.length === 0) {
      alert("Group Name cannot be empty");
    } else if (membersList.length === 0) {
      alert("Members cannot be empty");
    }
  };

  return (
    <ScrollView>
      <View center>
        <View>
          <Text style={styles.title}>Create a Group</Text>
          <Avatar
            source={{
              uri: "https://lh3.googleusercontent.com/-cw77lUnOvmI/AAAAAAAAAAI/AAAAAAAAAAA/WMNck32dKbc/s181-c/104220521160525129167.jpg",
            }}
            containerStyle={{
              alignSelf: "center",
              marginHorizontal: 16,
              marginTop: 12,
              marginBottom: 12,
            }}
            onPress={() => console.log("Select image from users device")}
            size={96}
          />
        </View>
        <View paddingL-24 paddingR-24>
          <View>
            <TextInput
              style={styles.input}
              placeholder="Group Name"
              onChangeText={(text) => setGroupName(text)}
              value={groupName}
              textContentType="none"
              activeUnderlineColor="blue"
            />
          </View>
          <ChipsInput
            style={styles.input}
            placeholder="Add Members"
            chips={membersList}
            value={membersList}
            ref={chipInputRef}
            multiline
            keyboardType="email-address"
            onChangeText={(text) => {
              setEmail(text);
            }}
            onKeyPress={(event) => addEmail(event)}
          />
          <Picker
            style={styles.picker}
            value={baseCurrency}
            onChange={(itemValue, itemIndex) => {
              setBaseCurrency(itemValue);
            }}
          >
            <Picker.Item label="USD" value="USD" />
            <Picker.Item label="EUR" value="EUR" />
            <Picker.Item label="GBP" value="GBP" />
            <Picker.Item label="INR" value="INR" />
            <Picker.Item label="JPY" value="JPY" />
          </Picker>
          <Checkbox
            label="Temporary"
            value={isTemporary}
            onValueChange={(value) => setIsTemporary(value)}
            marginV-12
          />
          {isTemporary && (
            <DateTimePicker
              title={"Select destruction date"}
              mode="date"
              value={destructionDate}
              minimumDate={new Date()}
              onChange={(date) => setDestructionDate(date)}
            />
          )}
        </View>

        <Button
          style={styles.button}
          label={"Done"}
          onPress={handleRegistration}
        />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    fontSize: 24,
    marginTop: 16,
    marginBottom: 16,
  },
  input: {
    height: 40,
    borderBottomWidth: 1,
    borderColor: "lightgrey",
    padding: 8,
    marginBottom: 16,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "80%",
  },
  buttonText: {
    color: "white",
    fontSize: 18,
    textAlign: "center",
  },
  picker: {
    width: 200,
    height: 44,
    marginBottom: 4,
  },
});
