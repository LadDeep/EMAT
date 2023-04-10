import React, { useEffect, useState } from "react";
import { Text, TextInput, StyleSheet, ScrollView } from "react-native";
import { Picker } from "@react-native-picker/picker";
import { CreateUser, FetchDetailedCurrencyList } from '../api/api'
import { View, Slider, Image, Button } from "react-native-ui-lib";
import { useNavigation } from "@react-navigation/native";

const SignUp = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [monthlyBudget, setMonthlyBudget] = useState(10);
  const [alertValue, setAlertValue] = useState(0);
  const [currencyList, setCurrencyList] = useState()
  const navigation = useNavigation();

  useEffect(() => {
    FetchDetailedCurrencyList(
      (res) => {
        console.log(res.data.message)
        setCurrencyList(res.data.message)
      },
      (err) => {
        console.log(err);
      }
    );
  }, []);
  const handleSubmit = () => {
    let payload = {
      email: email,
      password: password,
      first_name: firstName,
      last_name: lastName,
      currency: baseCurrency,
      monthly_budget_amount: monthlyBudget,
      warning_budget_amount: alertValue,
    };
    console.log("This is payload", payload)
    CreateUser(
      payload,
      (res) => {
        console.log("This is response of registered user", res)
        alert("Registered Successfully")
        navigation.navigate("validateUser", { response: res.data.user_id })
      },
      (err) => {
        console.log(JSON.stringify(err, null, 4));
      }
    );
  };


  const handleMonthlyBudgetChange = (value) => {
    setMonthlyBudget(value);
    setAlertValue(value / 2);
  }

  const handleAlertValueChange = (val) => {
    setAlertValue(parseInt(val))
    console.log(parseInt(val))
  }

  return (
    <ScrollView style={{ flex: 1 }}>
      <View flex center marginV-24>
        <Image
          style={styles.img}
          source={require("../../assets/pict--expenses-calculation-management.png")}
        />
        <Text style={styles.title}>Register to EMAT</Text>
        <TextInput
          style={styles.input}
          placeholder="First Name"
          value={firstName}
          onChangeText={(text) => setFirstName(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Last Name"
          value={lastName}
          onChangeText={(text) => setLastName(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          keyboardType="email-address"
          onChangeText={(text) => setEmail(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          secureTextEntry={true}
          value={password}
          onChangeText={(text) => setPassword(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Phone Number"
          value={phoneNumber}
          keyboardType="phone-pad"
          onChangeText={(text) => setPhoneNumber(text)}
        />
        <Picker
          selectedValue={baseCurrency}
          style={styles.picker}
          onValueChange={(itemValue, itemIndex) => setBaseCurrency(itemValue)}
        >
          {currencyList &&
            currencyList.map((currency, index) => (
              <Picker.Item label={currency.name} value={currency.code} />
            ))}
        </Picker>
        <TextInput
          style={styles.input}
          keyboardType="numeric"
          placeholder="Monthly Budget"
          value={monthlyBudget}
          onChangeText={handleMonthlyBudgetChange}
        />

        <View style={{ width: "70%" }}>
          <Slider
            minimumValue={0}
            maximumValue={monthlyBudget}
            onValueChange={(val) => {
              handleAlertValueChange(val);
            }}
          />
          <Text style={styles.alertText}>Alert Value: {alertValue}</Text>
        </View>
        <Button label="Submit" style={styles.button} onPress={handleSubmit} />
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
    fontWeight: "bold",
    marginBottom: 20,
  },
  input: {
    // width: 200,
    width: "70%",
    height: 44,
    padding: 10,
    borderWidth: 1,
    borderColor: "black",
    marginBottom: 10,
    borderRadius: 16,
  },
  picker: {
    width: "70%",
    height: 44,
    marginBottom: 20,
  },
  slider: {
    width: "70%",
    marginBottom: 10,
  },
  img: {
    width: 90,
    height: 90,
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
    marginVertical: 24
  },
});

export default SignUp;
