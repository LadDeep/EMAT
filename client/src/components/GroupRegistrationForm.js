import React, { useState, useEffect } from "react";
import { useNavigation } from "@react-navigation/native";
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
import {  RegisterGroup } from "../api/api";
import { FetchDetailedCurrencyList } from "../api/api";
import { getValueFor } from "../secureStore";

export const GroupRegistrationForm = () => {
  const [membersList, setMembersList] = useState([]);
  const [email, setEmail] = useState("");
  const [groupName, setGroupName] = useState("");
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [isTemporary, setIsTemporary] = useState(false);
  const [destructionDate, setDestructionDate] = useState(new Date());
  const [currencyList, setCurrencyList] = useState(null);
  const chipInputRef = React.createRef();
  const navigation = useNavigation();

  useEffect(() => {
    FetchDetailedCurrencyList(
      (res) => {
        console.log(res.data.message)
        setCurrencyList(res.data.message)
      },
      (err) => {
        console.log(err);
        // TODO: Add message based on api response
      }
    );
  },[]);

  const addEmail = (event) => {
      let member=chipInputRef.current.state.value?.split('\n')
      console.log("member:",member)
      setMembersList([
        ...membersList,
        { label:  member[member.length-1]},
      ]);
      setEmail("")
      console.log(chipInputRef.current.state.value)
    // }
  };
  const handleRegistration = () => {
    if (groupName.length === 0) {
      alert("Group Name cannot be empty");
    } else if (membersList.length === 0) {
      alert("Members cannot be empty");
    } else {
      let userEmail;
      let mList = membersList.map((value, index)=>{return value.label})
      //TODO: send email of creater as well
      RegisterGroup(
        {
          group_name: groupName,
          group_currency: baseCurrency,
          participants: mList,
        },
        (response) => {
          alert("Registration successfull")
          console.log(response);
          navigation.navigate("GroupsTab")
        },
        (erorr) => {
          console.log(erorr);
          //TODO: Show error on user already exists
        }
      );
    }
  };
  console.log("email",email)

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
            onKeyPress={(event) => {
              if (event.nativeEvent.key === "Enter") {
                addEmail(event);
              }
            }}
            validate={["email"]}
          />
          <Picker
            style={styles.picker}
            value={baseCurrency}
            onChange={(itemValue, itemIndex) => {
              setBaseCurrency(itemValue);
            }}
          >
            {currencyList &&
              currencyList.map((currency, index) => (
                <Picker.Item label={currency.name} value={currency.code} />
              ))}
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
