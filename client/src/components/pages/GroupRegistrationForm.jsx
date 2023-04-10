import React, { useState, useEffect, useContext } from "react";
import { useNavigation } from "@react-navigation/native";
import {
  TextInput, StyleSheet, ScrollView, TouchableOpacity, Text,ActivityIndicator
} from "react-native";
// import ReactChipsInput from 'react-native-chips';
import {
  Avatar,
  Button,
  Picker,
  Checkbox,
  DateTimePicker,
  View
} from "react-native-ui-lib";
import { RegisterGroup, UserDetails } from "../../api/api";
import { FetchDetailedCurrencyList } from "../../api/api";
import GroupContext from "../../Context/GroupContext";
export const GroupRegistrationForm = () => {
  const [emails, setEmails] = useState([]);
  const [emailInput, setEmailInput] = useState('');
  const [membersList, setMembersList] = useState();
  const [groupName, setGroupName] = useState("");
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [isTemporary, setIsTemporary] = useState(false);
  const [destructionDate, setDestructionDate] = useState(new Date());
  const [currencyList, setCurrencyList] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const { setGroupState } = useContext(GroupContext);
  const navigation = useNavigation();
  useEffect(() => {

    FetchDetailedCurrencyList(
      (res) => {
        console.log(res.data.message)
        setCurrencyList(res.data.message)
        setIsLoading(false);
      },
      (err) => {
        console.log(err);
      }
    );
  }, []);

  const handleAddEmail = () => {
    if (emailInput.trim() !== '' && validateEmail(emailInput)) {
      setEmails([...emails, emailInput.trim()]);
      setEmailInput('');
    }
  };

  const handleRemoveEmail = (index) => {
    const newEmails = [...emails];
    newEmails.splice(index, 1);
    setEmails(newEmails);
  };

  const validateEmail = (email) => {
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    return emailRegex.test(email);
  };



  const handleRegistration = () => {
    setGroupState(true)
    if (groupName.length === 0) {
      alert("Group Name cannot be empty");
    } else if (emails.length === 0) {
      alert("Members cannot be empty");
    } else {
      let payload = {
        group_name: groupName,
        group_currency: baseCurrency && baseCurrency.value ? baseCurrency.value : "USD",
        participants: emails
      }
      console.log("EMAILS", emails)
      console.log("This is the payload of group Registration", payload)
      RegisterGroup(
        payload,
        (response) => {
          alert("Registration successfull")
          console.log(response);
          navigation.navigate("GroupsTab")
        },
        (error) => {
          console.log(error);
          //TODO: Show error on user already exists
        }
      );
    }
  };
  console.log("baseCurrency", baseCurrency)

  if(isLoading){
    return (
      <View flex center>
        <ActivityIndicator size="large" color="blue"/>
      </View>
    )
  }

  return (
    <ScrollView>
      <View style={{ padding: 60 }}>
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

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Group Name"
            onChangeText={(text) => setGroupName(text)}
            value={groupName}
            textContentType="none"
            activeUnderlineColor="blue"
          />
        </View>
        {/* ???? */}
        {/* <ReactChipsInput
            label="Enter Email" initialChips={membersList}

            onChangeChips={(chips) => setMembersList(chips)}
            alertRequired={true}
            chipStyle={{ borderColor: 'blue', backgroundColor: 'grey' }}
            inputStyle={{ fontSize: 17 }}
            labelStyle={{ color: 'blue' }}
            labelOnBlur={{ color: '#666' }} /> */}
        <View style={styles.container}>
          <View style={styles.chipsContainer}>
            {emails?.map((email, index) => (
              <TouchableOpacity
                key={index}
                style={styles.chip}
                onPress={() => handleRemoveEmail(index)}
              >
                <Text style={styles.chipText}>{email}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Enter email address"
              value={emailInput}
              onChangeText={setEmailInput}
              blurOnSubmit={false}
              keyboardType="email-address"
            />
            <TouchableOpacity style={styles.addButton} onPress={handleAddEmail}>
              <Text style={styles.addButtonText}>Add</Text>
            </TouchableOpacity>
          </View>
        </View>
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
        <View centerH>
          <Button
            style={styles.button}
            label={"Done"}
            onPress={handleRegistration}
          />
        </View>
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
    textAlign: "center"
  },

  button: {
    backgroundColor: "blue",
    padding: 12,
    // width: "80%",
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
  container: {
    flex: 1,
    padding: 10,
    marginTop: 30,
  },
  chipsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    marginBottom: 10,
  },
  chip: {
    backgroundColor: '#e1e1e1',
    borderRadius: 20,
    padding: 10,
    margin: 5,
  },
  chipText: {
    color: '#333',
  },
  inputContainer: {
    flexDirection: 'row',
    justifyContent: "space-between"
  },
  input: {
    flex: 1,
    borderWidth: 1,
    backgroundColor: '#f2f2f2',
    borderRadius: 20,
    padding: 10,
    // marginBottom: 16,
  },
  addButton: {
    backgroundColor: 'blue',
    borderRadius: 20,
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  addButtonText: {
    color: '#fff',
  },
});
