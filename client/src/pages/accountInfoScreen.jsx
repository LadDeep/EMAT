import React, { useState, useEffect } from 'react';
import { Text, Image, TextInput, StyleSheet } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';
import { View, Button, Slider } from "react-native-ui-lib";
import { UpdateUser, UserDetails } from '../api/api';

const AccountInfoScreen = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [monthlyBudget, setMonthlyBudget] = useState(10);
  const [alertValue, setAlertValue] = useState(0);


  useEffect(() => {
    UserDetails(
      (res) => {
        if (res.data.status) {
          setFirstName(res.data.message.first_name)
          setLastName(res.data.message.last_name)
          setEmail(res.data.message.email)
          setMonthlyBudget(res.data.message.monthly_budget_amount)
          setAlertValue(res.data.message.warning_budget_amount)
          console.log(res)

        }
      },
      (err) => {
        console.log(err)
      })
  }, [])


  const handleSave = () => {
    let payload = {
      first_name: firstName,
      last_name: lastName,
      monthly_budget_amount: monthlyBudget,
      warning_budget_amount: alertValue,
    }
    console.log("This is the payload", payload)
    UpdateUser(
      payload,
      (res) => {
        console.log(res)
      },
      (err) => {
        console.log(err);
      }
    )
  }
  const handleMonthlyBudgetChange = (value) => {
    setMonthlyBudget(value);
    setAlertValue(value / 2);
  }

  const handleAlertValueChange = (val) => {
    setAlertValue(parseInt(val))
    console.log(parseInt(val))
  }


  return (
    <ScrollView>

    <View margin-24 style={styles.container}>
      <Image
        source={require('../../assets/group/1.png')}
        style={styles.profileImage}
      />
      <Text style={styles.title}>Account Information</Text>
      <View style={styles.inputContainer}>
        <Text style={styles.label}>First Name:</Text>
        <TextInput
          style={styles.input}
          value={firstName}
          onChangeText={setFirstName}
          placeholder="Enter your name"
        />
      </View>
      <View style={styles.inputContainer}>
        <Text style={styles.label}>Last Name:</Text>
        <TextInput
          style={styles.input}
          value={lastName}
          onChangeText={setLastName}
          placeholder="Enter your name"
        />
      </View>
      <View style={styles.inputContainer}>
        <Text style={styles.label}>Email:</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          placeholder="Enter your email"
        />
      </View>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          keyboardType='numeric'
          placeholder='Monthly Budget'
          value={monthlyBudget}
          onChangeText={handleMonthlyBudgetChange}
        />
        <Slider
          minimumValue={0}
          maximumValue={monthlyBudget}
          onValueChange={(val) => { handleAlertValueChange(val) }}
        />

        <Text style={styles.alertText}>Alert Value: {alertValue}</Text>
      </View>
      <Button label="Save" style={styles.button} onPress={handleSave} />
    </View>
    </ScrollView>

  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding: 16,
  },
  profileImage: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  inputContainer: {
    width: '100%',
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 16,
    padding: 10,
    fontSize: 16,
    width: '100%',
    
  },
  button: {
    backgroundColor: "blue",
    padding: 12,
    width: "50%",
  },
});

export default AccountInfoScreen;
